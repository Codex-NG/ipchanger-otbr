#!/usr/bin/env python
from ptrace.debugger.debugger import PtraceDebugger
from ptrace.debugger.child import createChild
from ptrace.tools import locateProgram
from sys import stderr, argv, exit

def playWithProcess(process):
    # Do anything you want with the process here...
    print("Dumping address")
    print process.readBytes(0x841f000 + 0x1638E0, 17)
    print("Continue process execution")
    process.cont()

def traceProgram(arguments):
    # Copy the environment variables
    env = None

    # Get the full path of the program
    arguments[0] = locateProgram(arguments[0])

    # Create the child process
    return createChild(arguments, False, env)

def main():
    # Check the command line
    if len(argv) < 2:
        print("usage: %s program [arg1 arg2 ...]" % argv[0])
        print("   or: %s pid" % argv[0])
        exit(1)

    # Get the process identifier
    is_attached = False
    has_pid = False
    if len(argv) == 2:
        try:
            # User asked to attach a process
            pid = int(argv[1])
            has_pid = True
        except ValueError:
            pass

    if not has_pid:
        # User asked to create a new program and trace it
        arguments = argv[1:]
        pid = traceProgram(arguments)
        is_attached = True

    # Create the debugger and attach the process
    dbg = PtraceDebugger()
    process = dbg.addProcess(pid, is_attached)

    # Play with the process and then quit
    playWithProcess(process)
    dbg.quit()

if __name__ == "__main__":
    main()