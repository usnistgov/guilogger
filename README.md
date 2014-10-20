Overview
========

This project aims to provide tools for constructing graphical user
interfaces (GUIs) that are easily testable.  A testable __GUI__ is one in
which a user session can be recorded in a log file, after which the
__log file__ can be instrumented and replayed to ensure that the GUI is
performing correctly.  The goal is not to test the widget toolkit
itself, but to ensure that the program using the toolkit is
interacting correctly with the __GUI__.  For example, the tests could
check that when a button is pressed the correct routine is executed,
or that when the state of an object changes, that change is reflected
in the __GUI__.

The __OOF__ materials modeling project at __NIST__ uses a __GUI__ constructed from
the __PyGTK toolkit__.  __OOF__ has a computational back end that interacts
via scriptable commands with the __GUI__.  The back end has a text based
regression suite, but changes in the back end or the __GUI__ often
resulted in errors in the __GUI__ that could not be caught by the
regression tests.  __gtklogger__ was written to enable __GUI__ tests for
OOF.  It is designed to be non-invasive: although the programmer has
to replace many __PyGTK__ function calls with gtklogger functions,
gtklogger imposes virtually no computational overhead during normal
operation of a program, is invisible to the end-user, and does not
limit the operation of __PyGTK__.

Alternatives
============

gtklogger is similar in some ways to __PyUseCase__, although it has
independent origins.

Guilogger
=========

**Github** is both a way of distributing __gtklogger__ and (we hope) a
way of encouraging equivalent tools to be developed for other __GUI__
toolkits.

The philosophy applied to __PyGTK__ in gtklogger can be applied to any
__GUI__ toolkit.  Because a logger can still be used even if not all of
the toolkits components are wrapped, it lends itself well to
incremental collaborative development.  We hope that this site will
encourage the development of loggers for a variety of __GUI__ toolkits.

A __guilogger__ is a module that wraps a __GUI__ __toolkit__ and
enables a program using the toolkit to do two main things: __recording__ a
user session __log file__, and __replaying__ the session while running tests.
The tests can be inserted into the log file in the form of __assert__
statements.  If the program successfully plays the __log__ file, it
has then passed the __GUI__ __Test__ __Case__.

A __guilogger__ module needs to provide the following 5 features:

1. It must have methods for assigning names
to __GUI__ widgets, so that the widgets can be identified in log files.
In __PyGTK__, __UI__ components are nested in containers, and the gtklogger identifier
for each widget is a path constructed from the names of all of its
containers.  

1. The __guilogger__ module needs to ensure that it is informed of
all actions performed by each logged widget.  In __gtklogger__, this is
done by replacing calls to __widget.connect(....)__ with
__gtklogger.connect(widget, ...)__, but it could be done differently, by
object inheritance for example. 

1. For each type of widget, the module needs to provide code
that records the widgets actions in the log file.

1. The __guilogger__ needs to provide a way of reading the log file and
recreating the widgets' actions.

1. Because timing can be important, the __guilogger__ must provide a way
of inserting __checkpoints__ into the __log__ file, so that it does not try to
recreate widget actions before the program is ready.

In general, using the __guilogger__ will require a program to be modified
in some minor ways.  The modifications required by __gtklogger__ (and we
hope by all __guiloggers__) do not impose any run time performance cost in
normal use, and only a small cost when recording or replaying a log.

This repository contains the gtklogger code and a demonstration of how
it is used.



Contributors
============
__gtklogger__ was developed by the __OOF team__ at the __National Institute
of Standards and technology__ (__NIST__). 

We encourage you to contribute to that project, since it is providing a different way of designing 
your __GUI__ tests suite.

__gtklogger__ is free for anybody coding a __PyGTK__ app.  Please use
it and let us know what you think about it.  If you want to add
features or fix issues that you encountere, please contact us.

We also encourage the implementation of this concept for other GUI
toolkits. We are thinking of: __Qt__, __Glui__, __Juce__,
__gladexml__, __jqueryUI__, __capuccino__, etc...



Install & Test
==================

Gtklogger
---------

Install __PyGTK__ version 2.6 or later, but not version 3.

To install __gtklogger__, go inside the folder and type: *python
setup.py install*. If you do not have root privileges add '--user'
to install it locally: *__python setup.py install --user__*.

To test __gtklogger__, please take a look at the examples
folder. There is a __gtkloggerdemo__ project in it.  It is a simple
GTK UI app to manage the creation of some geometric shapes. Please
look carefully how it integrates __gtklogger__ to enable recording and
replaying.

To simply run the app type: *__python gtkloggerdemo.py__*.

To record a session in '__log.py__', do: *__python gtkloggerdemo.py
--record=log.py__*.  From there you can instrument the log file with
some tests.  The log.py file provided in the repository contains some
examples of tests.

To replay the log file (instrumented or not) type: *__python
gtkloggerdemo.py --replay=log.py__*.

__NOTE__: When you start a recording, there is another __GUI__ that
appears along with your app. It is the guilogger __UI__ for __GTK__. It allows
you to add comments and view the events in the log file as they are
recorded.


References
==========

[Gtklogger Web docs](http://www.ctcms.nist.gov/oof/gtklogger/#docs)

[Gtklogger NIST internal publication paper as a model](gui_testing.pdf)

[OOF website](http://www.ctcms.nist.gov/oof/)
