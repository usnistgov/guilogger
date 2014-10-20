# -*- python -*-
# $RCSfile: gtkloggerdemo.py,v $
# $Revision: 1.1 $
# $Author: langer $
# $Date: 2007-08-27 20:02:37 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

## This is a demo program for gtklogger.  It doesn't otherwise do
## anything useful.

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import shapes

import getopt
import os
import string
import sys

import gtklogger

class ShapeDemo:
    def __init__(self):
        # This program's goal in life is to manage and display this
        # list of Shape objects.
        self.shapelist = gtk.ListStore(gobject.TYPE_PYOBJECT)
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        ## New top-level widgets (mostly windows) must be given a name
        ## by calling newTopLevelWidget.  No two top-level widgets can
        ## have the same name.
        gtklogger.newTopLevelWidget(self.window, 'ShapeDemo')
        ## All gtk.connect calls must be replaced with
        ## gtklogger.connect calls, if the action that triggers the
        ## callback needs to be logged.
        gtklogger.connect(self.window, 'delete-event', self.deleteEvent)
        ## Use connect_passive for actions that need to be logged, but
        ## don't have callbacks.  This line logs window resize events:
        gtklogger.connect_passive(self.window, 'configure-event')


        ## Widgets that don't do anything don't need to be named, even
        ## if they contain other widgets that do have to be logged.
        bigbox = gtk.VBox()
        self.window.add(bigbox)

        ## MenuItems and MenuBars must have names assigned with
        ## gtklogger.setWidgetName if any of the items they contain
        ## are to be logged.
        menubar = gtk.MenuBar()
        gtklogger.setWidgetName(menubar, 'menubar')
        bigbox.pack_start(menubar, expand=0, fill=0)
        filemenuitem = gtk.MenuItem('File')
        gtklogger.setWidgetName(filemenuitem, 'File')
        menubar.append(filemenuitem)
        filemenu = gtk.Menu()
        ## submenus must be assigned with gtklogger.set_submenu
        ## instead of gtk.MenuItem.set_submenu.
        gtklogger.set_submenu(filemenuitem, filemenu)

        quititem = gtk.MenuItem("Quit")
        filemenu.append(quititem)
        gtklogger.setWidgetName(quititem, 'Quit')
        gtklogger.connect(quititem, 'activate', self.quit)

        ## Keyboard accelerators don't need any special treatment for
        ## logging:
        accelgrp = gtk.AccelGroup()
        self.window.add_accel_group(accelgrp)
        quititem.add_accelerator('activate', accelgrp, ord('Q'),
                                 gtk.gdk.CONTROL_MASK,
                                 gtk.ACCEL_VISIBLE)

        ## The main part of the window is a Frame containing a VPaned.
        ## The Frame doesn't need a gtklogger name, since it doesn't
        ## have any signals associated with it.
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_OUT)
        frame.set_border_width(2)
        bigbox.pack_start(frame, expand=1, fill=1)

        pane = gtk.VPaned()
        frame.add(pane)
        ## Panes need names if motion of the divider is to be logged.
        gtklogger.setWidgetName(pane, "pane")
        gtklogger.connect_passive(pane, 'notify::position')

        ## The bottom half of the VPaned contains a button box.  We're
        ## doing the bottom half first because it's simpler.
        buttonframe = gtk.Frame()
        buttonframe.set_shadow_type(gtk.SHADOW_IN)
        pane.pack2(buttonframe, resize=False, shrink=False)

        buttonbox = gtk.HButtonBox()
        buttonframe.add(buttonbox)

        ## Widgets that actually do something need to be connected
        ## with gtklogger.connect.  They also must have names assigned
        ## with gtklogger.setWidgetName.
        addbutton = gtk.Button("Add")
        buttonbox.pack_start(addbutton, expand=1, fill=1)
        gtklogger.setWidgetName(addbutton, "AddButton")
        gtklogger.connect(addbutton, 'clicked', self.addButton)

        self.deletebutton = gtk.Button("Delete")
        buttonbox.pack_start(self.deletebutton, expand=1, fill=1)
        gtklogger.setWidgetName(self.deletebutton, "DeleteButton")
        gtklogger.connect(self.deletebutton, 'clicked', self.deleteButton)

        ## The top pane contains a scrollable list of shapes inside a
        ## decorative Frame.
        
        listframe = gtk.Frame("Shapes")
        listframe.set_shadow_type(gtk.SHADOW_IN)
        pane.pack1(listframe, resize=True, shrink=True)
        
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        listframe.add(scroll)
        ## gtklogger contains a utility function, logScrollBars, which
        ## can be used to log the scroll bars on a ScrolledWindow.  We
        ## don't use it here so that we can have an explicit example
        ## of using adoptGObject.
        ##
        ## We want to log scroll events that emit the 'value-changed'
        ## signal from the scrollbar's gtk.Adjustment object.  This
        ## object isn't a gtk.Widget, so it can't be located by
        ## traversing names in the Widget tree rooted at the main
        ## window.  Therefore the Adjustment has to be 'adopted' by a
        ## Widget, in this case the ScrolledWindow itself.  First, the
        ## ScrolledWindow needs a name:
        gtklogger.setWidgetName(scroll, 'scrollwindow')
        ## Then the adjustment is adopted.  The third Argument tells
        ## the logger how to find the Adjustment once it has located
        ## the parent.
        gtklogger.adoptGObject(scroll.get_vadjustment(), scroll,
                               access_method=scroll.get_vadjustment)
        ## connect_passive is used to log the signal, without
        ## connecting it to an explicit callback function.
        gtklogger.connect_passive(scroll.get_vadjustment(), 'value-changed')

        self.treeview = gtk.TreeView(self.shapelist)
        scroll.add(self.treeview)
        self.treeview.set_property("headers-visible", 0)
        self.tvcol = gtk.TreeViewColumn("")
        self.treeview.append_column(self.tvcol)
        cell = gtk.CellRendererText()
        self.tvcol.pack_start(cell, True)
        self.tvcol.set_cell_data_func(cell, self.cell_layout_data_func)

        ## We want to log selection events in the TreeView, but those
        ## events actually take place in the TreeView's TreeSelection,
        ## which isn't a Widget.  Therefore we have to use
        ## adoptGObject again.
        selection = self.treeview.get_selection()
        gtklogger.setWidgetName(self.treeview, 'ShapeList')
        gtklogger.adoptGObject(selection, self.treeview,
                               access_method=self.treeview.get_selection)
        self.selectsignal = gtklogger.connect(selection, 'changed',
                                              self.selectionChanged)


        ## Pop up a menu when the right mouse button is pressed in the
        ## TreeView.
        gtklogger.connect(self.treeview, 'button-press-event', self.tvbuttonCB)
        self.buildPopup()
        
        self.sensitize()
        
    def cell_layout_data_func(self, cell_view, cell_renderer, model, iter):
        idx = model.get_path(iter)[0]
        shape = model.get_value(iter, 0)
        cell_renderer.set_property('text', repr(shape))

    def show(self):
        self.window.show_all()

    def sensitize(self):
        ## Sensitize the delete button if there is a selected shape.
        selection = self.treeview.get_selection()
        model, iterator = selection.get_selected()
        self.deletebutton.set_sensitive(iterator is not None)

    def deleteEvent(self, *args):       # main window callback
        gtk.main_quit()

    def quit(self, *args):              # quit menu item
	#self.window.destroy()
        gtk.main_quit()

    def selectionChanged(self, treeselection):
        # gtk callback from list of shapes
        self.sensitize()

    def addButton(self, button):
        dialog = AddShapeDialog(self)
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            self.shapelist.append([dialog.shape()])
            self.sensitize()
        dialog.destroy()

    def deleteButton(self, button): # callback for the Delete button
        ## The Delete button is insensitive if there is no selection,
        ## so we don't have to check for a null selection.
        selection = self.treeview.get_selection()
        model, iterator = selection.get_selected()
        model.remove(iterator)

    def tvbuttonCB(self, gtkobj, event):
        ## Popup a menu when the right mouse button is pressed in the treeview.
        if event.button == 3:
            self.popupmenu.popup(None, None, None, event.button, event.time)
            return True
        return False

    def buildPopup(self):
        self.popupmenu = gtk.Menu()
        ## The menu is a top level widget.
        gtklogger.newTopLevelWidget(self.popupmenu, 'PopUpMenu')
        self.popupmenu.set_screen(self.treeview.get_screen())
        gtklogger.connect_passive(self.popupmenu, 'deactivate')
        ## Add menu items.  Each must be named and connected.
        for itemname in ("ready", "set", "go"):
            menuitem = gtk.MenuItem(itemname, False)
            gtklogger.setWidgetName(menuitem, itemname)
            gtklogger.connect(menuitem, 'activate', self.menuitemCB,
                              itemname)
            self.popupmenu.append(menuitem)
        ## Add a submenu...
        submenu = gtk.Menu()
        submenuitem = gtk.MenuItem('submenu')
        gtklogger.setWidgetName(submenuitem, 'submenu')
        gtklogger.set_submenu(submenuitem, submenu)
        self.popupmenu.append(submenuitem)
        for itemname in ("one", "two", "three"):
            menuitem = gtk.MenuItem(itemname, False)
            gtklogger.setWidgetName(menuitem, itemname)
            gtklogger.connect(menuitem, 'activate', self.menuitemCB,
                              itemname)
            submenu.append(menuitem)

        self.popupmenu.show_all()

    def menuitemCB(self, menuitemobj, itemname): # callback for popup menu items
        print itemname



## gtklogger.Dialog must be used instead of gtk.Dialog.  It's derived
## from gtk.Dialog, though.
class AddShapeDialog(gtklogger.Dialog):
    def __init__(self, mainwindow):
        gtklogger.Dialog.__init__(self, title="Add Shape",
                                  parent=mainwindow.window,
                                  flags=gtk.DIALOG_MODAL)
        ## A dialog box is a top level widget, and must be declared as
        ## such in order for its components to be logged.
        gtklogger.newTopLevelWidget(self, "AddShape")
        ## The gtk.Dialog.add_button is redefined in gtklogger.Dialog
        ## so that the buttons will be named and logged.
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        ## Create the list of shape types to display
        shapenames = gtk.ListStore(gobject.TYPE_STRING)
        for shapeclass in shapes.allShapeClasses:
            shapenames.append([shapeclass.__name__])
        ## Create a combobox for choosing which type of shape to select.
        self.combobox = gtk.ComboBox(shapenames)
        gtklogger.setWidgetName(self.combobox, "shapetypechooser")
        self.vbox.pack_start(self.combobox, expand=0, fill=0)
        cell = gtk.CellRendererText()
        self.combobox.pack_start(cell, True)
        self.combobox.add_attribute(cell, 'text', 0)
        self.combobox.set_active(0)
        gtklogger.connect(self.combobox, 'changed', self.comboChanged)

        ##  paramWidget is the gtk widget for setting the parameters
        ##  that define the particular Shape subclass.  It has to be
        ##  built by the Shape's factory class, which is invoked by
        ##  buildParamWidgets.
        self.paramWidget = None
        self.shapefactory = None
        self.buildParamWidgets(0)
        
        self.vbox.show_all()
    def comboChanged(self, combobox):   # ComboBox callback
        index = combobox.get_active()
        self.buildParamWidgets(index)
    def buildParamWidgets(self, which):
        ## Build the widgets for the parameters of the given shape class.
        shapeclass = shapes.allShapeClasses[which]
        if self.paramWidget:
            self.paramWidget.destroy()
        self.shapefactory = shapeclass.factory()
        self.paramWidget = self.shapefactory.gui()
        self.vbox.pack_start(self.paramWidget, expand=1, fill=1)
        self.paramWidget.show_all()
    def shape(self):
        return self.shapefactory.createShape()

def usage():
    print >> sys.stderr, """\
Usage: python shapedemo.py [options]
Choose at most one of the following options:
      --record=<logfile>
      --replay=<logfile>
      --rerecord=<logfile>"""
    
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["record=", "replay=",
                                                      "rerecord="])
    except getopt.GetoptError, exc:
        print >> sys.stderr, exc
        usage()
        sys.exit(1)
    if len(opts) > 1:
        usage()
        sys.exit(1)

    w = ShapeDemo()

    opt = None
    if len(opts) == 1:
        opt, filename = opts[0]

        if opt=='--record':
            gtklogger.start(filename, debugLevel=2,
                            suppress_motion_events=False)

        elif opt=='--replay':
            print "Replaying", filename
            gtklogger.replay(filename, threaded=False)

        elif opt=='--rerecord':
            print "Re-recording", filename
            backupfile = filename + ".bak"
            if os.path.exists(backupfile):
                os.remove(backupfile)
            os.rename(filename, backupfile)
            gtklogger.replay(backupfile, threaded=False, rerecord=filename)

    w.show()
    gtk.main()

    if opt=='--record':
        gtklogger.stop()


