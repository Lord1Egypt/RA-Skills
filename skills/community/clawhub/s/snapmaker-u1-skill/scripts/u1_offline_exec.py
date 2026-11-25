#!/usr/bin/env python3
"""Run a Python script with IP socket/DNS operations blocked in this process.

AF_UNIX IPC remains available. This is a Python API guard, not an OS-wide
network sandbox: native code and independently spawned processes are outside
its complete enforcement scope.
"""
from pathlib import Path
import runpy
import socket
import sys


def install_network_guard():
    def blocked(*args, **kwargs):
        raise PermissionError('Local runtime: Python IP networking and DNS are disabled.')

    def guard_method(original):
        def guarded(connection, *args, **kwargs):
            if connection.family in (socket.AF_INET, socket.AF_INET6):
                return blocked()
            return original(connection, *args, **kwargs)
        return guarded

    for name in ('connect', 'connect_ex', 'sendto', 'send', 'sendall', 'sendmsg'):
        if hasattr(socket.socket, name):
            setattr(socket.socket, name, guard_method(getattr(socket.socket, name)))
    for name in ('getaddrinfo', 'gethostbyname', 'gethostbyname_ex', 'gethostbyaddr', 'getnameinfo'):
        setattr(socket, name, blocked)


def main():
    arguments = sys.argv[1:]
    if arguments and arguments[0] == '--':
        arguments = arguments[1:]
    if not arguments:
        raise SystemExit('Usage: u1_offline_exec.py -- /absolute/local_script.py [arguments]')
    target = Path(arguments[0]).expanduser().resolve()
    if not target.is_file():
        raise SystemExit('Target Python script does not exist.')
    install_network_guard()
    sys.argv = [str(target), *arguments[1:]]
    sys.path.insert(0, str(target.parent))
    runpy.run_path(str(target), run_name='__main__')


if __name__ == '__main__':
    main()
