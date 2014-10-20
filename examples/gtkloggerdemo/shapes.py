# -*- python -*-
# $RCSfile: shapes.py,v $
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

## This file defines the Shape classes that the ShapeDemo uses.  The
## only point of the Shape classes is to define a bunch of objects
## that can be created.  Each type of object is created in a different
## way, so the user interface will vary depending on which type of
## object is being built.
##
## For each type of shape, we must define a subclass of Shape that
## represents the shape itself, and a subclass of ShapeFactory, that
## describes how to create the shape.  The Shape subclasses defined
## here are trivial, only containing a list of corner points (tuples
## of floats).  Concrete Shape subclasses contain a class data member
## called 'factory' indicating the ShapeFactory class that builds
## them.  The concrete shape classes are listed in the allShapeClasses
## list, which the GUI uses when presenting choices.  Construction of
## the allShapeClasses list is handled automatically by
## ShapeMetaClass.
##
## ShapeFactory subclasses must have two member functions, gui and
## createShape, which take no arguments other than self.  gui returns
## a gtk widget that can be placed in the user interface, and contains
## widgets for setting all of the parameters needed to construct a
## Shape.  createShape uses those widgets to create and return an
## instance of a concrete Shape.


import gtk
import string
import math

# When distributed, this line should just be "import gtklogger".
# However, while debugging both the demo program and the gtklogger
# module, it's convenient to piggyback on the oof2 installation.
import gtklogger

## List of all *concrete* Shape classes.  Concrete classes have a
## 'factory' data member.  factory is a ShapeFactory subclass, which
## can be used to build the GUI that creates the Shape object.
allShapeClasses = []

class ShapeMetaClass(type):
    def __init__(cls, name, bases, dict):
        super(ShapeMetaClass, cls).__init__(name, bases, dict)
        if dict.has_key('factory'):
            allShapeClasses.append(cls)

class Shape(object):
    __metaclass__ = ShapeMetaClass
    
class Triangle(Shape):
    def __init__(self, point1, point2, point3):
        self.points = (point1, point2, point3)
    def __repr__(self):
        return "%s %s %s %s" % ((self.__class__.__name__,) + self.points)

class Rectangle(Shape):
    def __init__(self, p1, p2, p3, p4):
        self.points = (p1, p2, p3, p4)
    def __repr__(self):
        return "%s %s %s %s %s" % ((self.__class__.__name__,) + self.points)

class ShapeFactory:
    ## Subclasses must override all methods, except maybe __init__.
    ## The stubs are listed here just to have a place to document the
    ## arguments and return values.
    def __init__(self):
        pass
    def gui(self):
        ## returns a gtk widget that can be placed in the
        ## AddShapeDialog.  References to the widget should be kept in
        ## the ShapeFactory so that createShape can use it.
        pass
    def createShape(self):
        ## extracts data from the gtk widget and returns a Shape
        ## instance.
        pass

class EquilateralTriangleFactory(ShapeFactory):
    def gui(self):
        box = gtk.HBox()
        gtklogger.setWidgetName(box, 'Equilateral')
        label = gtk.Label('side length')
        box.pack_start(label, expand=0, fill=0)
        self.entry = gtk.Entry()
        box.pack_start(self.entry, expand=1, fill=1)
        gtklogger.setWidgetName(self.entry, 'entry')
        gtklogger.connect_passive(self.entry, 'changed')
        return box
    def createShape(self):
        side = string.atof(self.entry.get_text())
        return EquilateralTriangle((0,0), (side, 0),
                                   (0.5*side, math.sqrt(3)*side/2.))
        
class EquilateralTriangle(Triangle):
    factory = EquilateralTriangleFactory

class IsoscelesTriangleFactory(ShapeFactory):
    def gui(self):
        table = gtk.Table(rows=2, columns=2)
        gtklogger.setWidgetName(table, 'Isosceles')
        table.attach(gtk.Label('height'), 0,1, 0,1, xoptions=gtk.FILL,
                     xpadding=2)
        self.heightentry = gtk.Entry()
        gtklogger.setWidgetName(self.heightentry, "height")
        gtklogger.connect_passive(self.heightentry, 'changed')
        table.attach(self.heightentry, 1,2, 0,1, xoptions=gtk.EXPAND|gtk.FILL,
                     xpadding=2)
        table.attach(gtk.Label('width'), 0,1, 1,2, xoptions=gtk.FILL,
                     xpadding=2)
        self.widthentry = gtk.Entry()
        gtklogger.setWidgetName(self.widthentry, "width")
        gtklogger.connect_passive(self.widthentry, 'changed')
        table.attach(self.widthentry, 1,2, 1,2, xoptions=gtk.EXPAND|gtk.FILL,
                     xpadding=2)
        return table
    def createShape(self):
        height = string.atof(self.heightentry.get_text())
        width = string.atof(self.widthentry.get_text())
        return IsoscelesTriangle((0, 0), (width, 0), (width/2., height))

class IsoscelesTriangle(Triangle):
    factory = IsoscelesTriangleFactory

class RightTriangleFactory(ShapeFactory):
    def gui(self):
        table = gtk.Table(rows=2, columns=2)
        gtklogger.setWidgetName(table, 'Right')
        # The length of the base comes from a gtk.Entry
        table.attach(gtk.Label('base'), 0,1, 0,1,
                     xoptions=gtk.FILL, xpadding=2)
        self.baseentry = gtk.Entry()
        self.baseentry.set_text('1.0')
        gtklogger.setWidgetName(self.baseentry, 'base')
        gtklogger.connect_passive(self.baseentry, 'changed')
        table.attach(self.baseentry, 1,2, 0,1,
                     xoptions=gtk.EXPAND|gtk.FILL, xpadding=2)

        # One of the acute angles comes from a gtk.HScale
        table.attach(gtk.Label('angle'), 0,1, 1,2,
                     xoptions=gtk.FILL, xpadding=2)
        self.adjustment = gtk.Adjustment(value=45.0, lower=0.0, upper=90.0,
                                         step_incr=0.01, page_incr=0.01)
        self.angleslider = gtk.HScale(self.adjustment)
        gtklogger.setWidgetName(self.angleslider, 'angle')
        ## The Adjustment is the object that emits a signal, but it's
        ## not a Widget, so it has to be "adopted" before it can be
        ## logged.  Otherwise it can't be located by name within the
        ## Widget tree.
        gtklogger.adoptGObject(self.adjustment, self.angleslider,
                               access_method=self.angleslider.get_adjustment)
        gtklogger.connect_passive(self.adjustment, 'value-changed')
        table.attach(self.angleslider, 1,2, 1,2,
                     xoptions=gtk.EXPAND|gtk.FILL, xpadding=2)
        return table
    def createShape(self):
        base = string.atof(self.baseentry.get_text())
        angle = self.adjustment.get_value()
        return RightTriangle((0,0), (base, 0),
                             (0, base*math.tan(angle*math.pi/180.)))

class RightTriangle(Triangle):
    factory = RightTriangleFactory

class SquareFactory(ShapeFactory):
    def gui(self):
        box = gtk.HBox()
        gtklogger.setWidgetName(box, 'Square')
        label = gtk.Label('side length')
        box.pack_start(label, expand=0, fill=0)
        self.entry = gtk.Entry()
        box.pack_start(self.entry, expand=1, fill=1)
        gtklogger.setWidgetName(self.entry, 'entry')
        gtklogger.connect_passive(self.entry, 'changed')
        return box
    def createShape(self):
        side = string.atof(self.entry.get_text())
        return Square((0,0), (side, 0), (side, side), (0, side))

class Square(Rectangle):
    factory = SquareFactory
                                  
        
