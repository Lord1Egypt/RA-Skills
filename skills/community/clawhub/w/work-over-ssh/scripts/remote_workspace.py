#!/usr/bin/env python3
"""Dependency-free SSH helper for the work-over-ssh agent skill."""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys
from typing import NoReturn


HOST_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@%+\-\[\]]*$")
SSH_BASE = (
    "ssh",
    "-o",
    "BatchMode=yes",
    "-o",
    "ConnectTimeout=10",
)


def fail(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def validate_host(value: str) -> str:
    if not HOST_RE.fullmatch(value):
        fail("HOST must be a concrete SSH alias or destination without whitespace")
    return value


def validate_root(value: str) -> str:
    if "\x00" in value or "\n" in value or "\r" in value:
        fail("remote project path contains invalid characters")
    path = PurePosixPath(value)
    if not path.is_absolute():
        fail("remote project path must be absolute")
    return str(path)


def validate_relative_path(value: str) -> str:
    if "\x00" in value or "\n" in value or "\r" in value:
        fail("remote file path contains invalid characters")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or str(path) in ("", "."):
        fail("remote file path must be a non-empty path relative to the project")
    return str(path)


def validate_environment_path(value: str) -> str:
    if "\x00" in value or "\n" in value or "\r" in value:
        fail("environment path contains invalid characters")
    path = PurePosixPath(value)
    if str(path) in ("", ".") or (not path.is_absolute() and ".." in path.parts):
        fail("environment path must be absolute or safely relative to the project")
    return str(path)


def validate_name(value: str) -> str:
    if not value or "\x00" in value or "\n" in value or "\r" in value:
        fail("environment name contains invalid characters")
    return value


def validate_executable(value: str) -> str:
    if (
        not value
        or value.startswith("-")
        or "\x00" in value
        or "\n" in value
        or "\r" in value
    ):
        fail("executable must be a command name or absolute path")
    return value


def remote_in_root(root: str, argv: list[str]) -> str:
    return f"cd {shlex.quote(root)} && {shlex.join(argv)}"


def run_ssh(
    host: str,
    remote_command: str,
    *,
    stdin: bytes | None = None,
    capture: bool = False,
) -> subprocess.CompletedProcess[bytes]:
    command = [*SSH_BASE, host, remote_command]
    return subprocess.run(
        command,
        input=stdin,
        check=False,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def cmd_check(args: argparse.Namespace) -> int:
    command = remote_in_root(
        args.root,
        [
            "sh",
            "-c",
            "printf 'connected\\n'; printf 'host='; hostname; "
            "printf 'cwd='; pwd; "
            "printf 'git='; "
            "if git rev-parse --show-toplevel >/dev/null 2>&1; "
            "then git rev-parse --show-toplevel; else printf 'not-a-repository\\n'; fi",
        ],
    )
    return run_ssh(args.host, command).returncode


def cmd_exec(args: argparse.Namespace) -> int:
    if not args.command:
        fail("provide a command after --")

    command = args.command
    if args.venv:
        environment = PurePosixPath(args.venv)
        if not environment.is_absolute():
            environment = PurePosixPath(args.root) / environment
        environment_text = str(environment)
        script = (
            f"venv={shlex.quote(environment_text)}; "
            'if test ! -x "$venv/bin/python"; then '
            'printf "virtualenv Python is not executable: %s\\n" '
            '"$venv/bin/python" >&2; exit 2; fi; '
            'export VIRTUAL_ENV="$venv"; '
            'export PATH="$venv/bin:$PATH"; '
            "unset PYTHONHOME; "
            f"exec {shlex.join(command)}"
        )
        remote_command = remote_in_root(args.root, ["sh", "-c", script])
    elif args.conda_name or args.conda_prefix:
        selector = (
            ["-n", args.conda_name]
            if args.conda_name
            else ["-p", args.conda_prefix]
        )
        environment_command = [
            args.conda_executable,
            "run",
            "--no-capture-output",
            *selector,
            *command,
        ]
        remote_command = remote_in_root(args.root, environment_command)
    else:
        remote_command = remote_in_root(args.root, command)

    return run_ssh(args.host, remote_command).returncode


def cmd_read(args: argparse.Namespace) -> int:
    if args.start < 1 or args.end < args.start:
        fail("line range must satisfy 1 <= start <= end")
    remote_path = f"./{args.path}"
    command = remote_in_root(
        args.root,
        ["sed", "-n", f"{args.start},{args.end}p", remote_path],
    )
    return run_ssh(args.host, command).returncode


def cmd_apply_patch(args: argparse.Namespace) -> int:
    patch_path = Path(args.patch).expanduser()
    if not patch_path.is_file():
        fail(f"patch file does not exist: {patch_path}")
    patch = patch_path.read_bytes()
    if not patch:
        fail("patch file is empty")
    if len(patch) > args.max_bytes:
        fail(f"patch exceeds --max-bytes ({args.max_bytes})")

    script = (
        "set -eu; "
        "umask 077; "
        "p=$(mktemp \"${TMPDIR:-/tmp}/codex-ssh-patch.XXXXXX\"); "
        "trap 'rm -f \"$p\"' EXIT HUP INT TERM; "
        "cat >\"$p\"; "
        "git apply --check \"$p\"; "
        "git apply \"$p\""
    )
    command = remote_in_root(args.root, ["sh", "-c", script])
    return run_ssh(args.host, command, stdin=patch).returncode


def add_target(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("host", type=validate_host, help="SSH config alias or destination")
    parser.add_argument("root", type=validate_root, help="absolute remote project path")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect and patch a remote project through local OpenSSH."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    check = subparsers.add_parser("check", help="verify SSH, path, host, and Git root")
    add_target(check)
    check.set_defaults(handler=cmd_check)

    execute = subparsers.add_parser(
        "exec",
        help="run a command in the remote project, optionally in venv or Conda",
    )
    environment = execute.add_mutually_exclusive_group()
    environment.add_argument(
        "--venv",
        type=validate_environment_path,
        metavar="PATH",
        help="virtualenv path, absolute or relative to the project",
    )
    environment.add_argument(
        "--conda-name",
        type=validate_name,
        metavar="NAME",
        help="Conda environment name",
    )
    environment.add_argument(
        "--conda-prefix",
        type=validate_root,
        metavar="PATH",
        help="absolute Conda environment prefix",
    )
    execute.add_argument(
        "--conda-executable",
        type=validate_executable,
        default="conda",
        metavar="PATH",
        help="Conda executable name or absolute path (default: conda)",
    )
    add_target(execute)
    execute.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="command and arguments, normally placed after --",
    )
    execute.set_defaults(handler=cmd_exec)

    read = subparsers.add_parser("read", help="print a bounded line range from a file")
    add_target(read)
    read.add_argument("path", type=validate_relative_path)
    read.add_argument("--start", type=int, default=1)
    read.add_argument("--end", type=int, default=240)
    read.set_defaults(handler=cmd_read)

    apply_patch = subparsers.add_parser(
        "apply-patch",
        help="check and apply a local Git patch to the remote project",
    )
    add_target(apply_patch)
    apply_patch.add_argument("patch", help="local patch file")
    apply_patch.add_argument(
        "--max-bytes",
        type=int,
        default=10 * 1024 * 1024,
        help="maximum patch size (default: 10 MiB)",
    )
    apply_patch.set_defaults(handler=cmd_apply_patch)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
