Guilogger
=========
We describe a scheme for systematically testing the operation of a graphical user interface. The
scheme provides a capability for generating event logs, which are recordings of a user session with
the interface. These logs can be annotated with assertion statements, comparing reference test
data with data retrieved by introspection on the GUI elements. Such an annotated log forms a
test case, suitable for incorporation into a regression test suite.

Description
===========
It is well established among software developers that systematic testing of software,
whether against a formal design specification or against a less formal case-by-case asses-
ment of correct functionality, is a critical part of the software development cycle, and crucial
to the production of high-quality software.

Much formal testing methodology revolves around viewing software products as essen-
tially functions, in the mathematical sense, abstractly taking a single input from some large
domain, performing a computation, and producing a single output. Increases in both the
raw power of computers and in the power and scope of software development tools have lead
to increasing complexity in software. Presenting this complexity to the user in a compre-
hensible way demands a graphical user interface, which has its own complexity, and makes
the software a stateful, interactive machine. While it is still true that the software can
be thought of as a function, now the inputs and outputs have to be considered to be the
full state of the program and its GUI. This complicates the application of traditional test-
ing methods. At the same time, the GUI raises the bar for the expected reliability — it
allows users more rapid access to potentially-overlooked corner cases, and encourages the
expectation that all aspects of the program will “just work”.

Contact with formal testing methodology can be restored by the introduction of system-
atic ways of testing of a graphical user interface. In this article, we take a step in that
direction, describing the construction of a testing kit, that allows a user session with a GUI
to be recorded and played back, and that allows the state of the GUI widgets to be queried
at repeatable locations within the session, ensuring both correctness and consistency of the
__GUI__ state.

For our example, we use the __GIMP Tool Kit__ (__GTK__) widget set1, specifically __gtk+__, version
2.6 or later, and its Python wrappers, __PyGTK2__ . We have created a Python module, called
gtklogger, which can be used to record, replay, and test a program with a __PyGTK__ user
interface. gtklogger was developed specifically to test the OOF3 project at __NIST__, but can
easily be applied to other __PyGTK__ programs. This paper includes instructions for extending
__gtklogger__ to handle __PyGTK__ objects that were not used in __OOF__.

__NOTE__: The full technical report can be found in the references.

Contributors
============
This project is meant to share the concept developed by the __OOF team__ at the __National Institute
of Standards and technology__ (__NIST__). The __OOF GUI__ benefited a lot from the first implementation
of that concept for __GTK__.

We encourage you to contribute to that project, since it is providing a different way of designing 
your __GUI__ tests suite as you have glenced from the description and probably understood from the 
technical report if you have got to read it.

The __gtklogger__ is there for anybody coding a __GUI__ based __GTK__ app. So use it and let us know what you
think about it. If you want to add some features or fix some issues that you encountered, please
feel free to contact us.

We also motivate the implementation of this concept for other GUI toolkits. We are thinking of:
__Qt__, __Glui__, __Juce__, __gladexml__, __jqueryUI__, __capuccino__, etc...
For each case the namming standard will be [toolkit-name]logger as you see '__gtklogger__'.


References
==========
[Gtklogger NIST internal publication paper as a model](gui_testing.pdf)

[OOF website](http://www.ctcms.nist.gov/oof/)