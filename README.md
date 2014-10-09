Guilogger
=========
Guilogger started from __gtklogger__, which is a Python module for recording (capturing) and
replaying a session of a program with a __GUI__ written with __PyGTK__. It can be used with any
__PyGTK__ similarily in spirit to __PyUseCase__, but aiming GUI tests suite design. After testing
__gtklogger__ on __OOF2__ and the newly released __OOF3D__ it became obvious to us that the
concept of __recording__ plus __instrumenting__ and __replaying__ for __GUI__ is very conveniant. 
That is why we decided  to create this __guilogger__ to introduce the idea being in play but also
 collaborate with contributors to spread it to more GUI toolkits.


Description
===========
A __guilogger__ is a module that suites your __GUI__ __toolkit__ and that you import in your project.
It will then enable a test suite to be written for the __UI__ of your __GUI__ __toolkit__ based program.
The progam that imports a guilogger should probably be adapted (replacing some widgets and calls)
to be able to record a user session (interactions with the __Graphical__ __Interface__) in a __log__ file.
Some tests (__asserts__, ...) can then be added to the __log__ file and replayed by the program. If the 
program successfully play the __log__ file, it has then passed the __GUI__ __Test__ __Case__. This is in
principle how the __guilogger__ works.

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