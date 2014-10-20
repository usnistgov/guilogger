Overview
========

This project aims to provide tools for constructing graphical user
interfaces (GUIs) that are easily testable.  A testable GUI is one in
which a user session can be recorded in a log file, after which the
log file can be instrumented and replayed to ensure that the GUI is
performing correctly.  The goal is not to test the widget toolkit
itself, but to ensure that the program using the toolkit is
interacting correctly with the GUI.  For example, the tests could
check that when a button is pressed the correct routine is executed,
or that when the state of an object changes, that change is reflected
in the GUI.

The OOF materials modeling project at NIST uses a GUI constructed from
the PyGTK toolkit.  OOF has a computational back end that interacts
via scriptable commands with the GUI.  The back end has a text based
regression suite, but changes in the back end or the GUI often
resulted in errors in the GUI that could not be caught by the
regression tests.  __gtklogger__ was written to enable GUI tests for
OOF.  It is designed to be non-invasive: although the programmer has
to replace many PyGTK function calls with gtklogger functions,
gtklogger imposes virtually no computational overhead during normal
operation of a program, is invisible to the end-user, and does not
limit the operation of PyGTK.

Alternatives
============

gtklogger is similar in some ways to PyUseCase, although it has
independent origins.  [Add description of differences here?]

Guilogger
=========

Github is both a way of distributing gtklogger and (we hope) a
way of encouraging equivalent tools to be developed for other GUI
toolkits.

The philosophy behind the Guilogger applied here to __pygtk__ can be
applied to any GUI toolkit in some sense. But a guilogger should
follow a certain scheme to allow incremental contributions because 
it doesn't really need to be completed but will be more usefull if all
the widgets are covered.

A __guilogger__ is a module that suites your __GUI__ __toolkit__ and
that you import in your project. It will then enable a test suite to 
be written for the __UI__ of your __GUI__ __toolkit__ based program.
The progam that imports a guilogger should probably be adapted (replacing some widgets and calls)
to be able to record a user session (interactions with the __Graphical__ __Interface__) in a __log__ file.
Some tests (__asserts__, ...) can then be added to the __log__ file and replayed by the program. If the 
program successfully play the __log__ file, it has then passed the __GUI__ __Test__ __Case__. This is in
principle how the __guilogger__ works.

To provide a guilogger recordable/replayable widget, you should deliver two main
things. The first one is to override the originial widget to log the widget call into the 
log file when the events and callbacks are being executed. The trace should
be the full instance of the widget and its callback with the parameters values. How this
instance is beeing found is the second thing that need to be delivered. There
is a process of finding widget that you provided guilogger widget should follow
in order to be found. This way all the instances are being identified and their calls 
being recorded and replayed consistently. Those main changes are really straight forward.

For the specific case of __gtklogger__, you can find in this repository the module to import and inside
the folder examples you will find the project __gtkloggerdemo__ as an application of what has been presented
here for __gtklogger__.

For more informations about the work that has already been done with __gtklogger__, please follow the 
references.


Contributors
============
This project is meant to share the concept developed by the __OOF team__ at the __National Institute
of Standards and technology__ (__NIST__). The __OOF GUI__ benefited a lot from the first implementation
of that concept for __GTK__.

We encourage you to contribute to that project, since it is providing a different way of designing 
your __GUI__ tests suite.

The __gtklogger__ is there for anybody coding a __GUI__ based __GTK__ app. So use it and let us know what you
think about it. If you want to add some features or fix some issues that you encountered, please
feel free to contact us.

We also motivate the implementation of this concept for other GUI toolkits. We are thinking of:
__Qt__, __Glui__, __Juce__, __gladexml__, __jqueryUI__, __capuccino__, etc...
For each case the namming standard will be [toolkit-name]logger as you see '__gtklogger__'.


Install & Test
==================

Gtklogger
---------
Check if you have a version of pygtk make sure it is a 2.x where is should be greater or equal to 6.
To install __gtklogger__, go inside the folder and type: *python setup.py install*. Yet if you do not have root
privileges you add '--user' as the following: *python setup.py install --user* to install it locally.

To test the __gtklogger__, please take a look at the examples folder. There is a __gtkloggerdemo__ project in it.
It is a simple GTK UI app to manage the creation of some geometric shapes. Please look carefully how it
integrates __gtklogger__ to be able to enable the recording /replaying.

To simply run the app type: *python gtkloggerdemo.py*.

To record a session in 'log.py', do: *python gtkloggerdemo.py --record=log.py*.
From there you can instrument the log file with some tests.

To replay the log file (instrumented or not) type: *python gtkloggerdemo.py --replay=log.py*.

__NOTE__: When you start a recording, there is another GUI that appears alon with your app. It is the 
guilogger UI for GTK. It allows you to view the events recoded in the log file and also be able to add
 some comments as the recording goes.


References
==========

[Gtklogger Web docs](http://www.ctcms.nist.gov/oof/gtklogger/#docs)

[Gtklogger NIST internal publication paper as a model](gui_testing.pdf)

[OOF website](http://www.ctcms.nist.gov/oof/)
