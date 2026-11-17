#!/usr/bin/env python3
"""Stage a ClawHub skill, require a complete clean scan, then install it."""

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile


SCANNER = "snyk-agent-scan==0.6.3"
MAX_BYTES = 20 * 1024 * 1024
MAX_FILES = 1000


class Blocked(Exception):
    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


class Parser(argparse.ArgumentParser):
    def error(self, message):
        # Invalid arguments may contain shell escapes or credential values.
        self.print_usage(sys.stderr)
        self.exit(1, "Invalid arguments. Use --help for supported options.\n")


def arguments(argv):
    parser = Parser(description=__doc__, allow_abbrev=False)
    parser.add_argument("slug", help="ClawHub slug: lowercase letters, digits and hyphens")
    parser.add_argument("--version", help="Specific ClawHub version")
    parser.add_argument("--force", action="store_true",
                        help="Replace after a clean scan; retain the previous installation as a backup")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug) or len(args.slug) > 128:
        raise Blocked("Invalid skill slug; paths and owner-qualified references are not supported.")
    if args.version is not None and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.+_-]{0,127}", args.version):
        raise Blocked("Invalid version.")
    return args


def owned_directory(path, private=False):
    if path.is_symlink():
        raise Blocked("Refusing a symbolic link for an installation or staging directory.")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.stat()
    forbidden = 0o077 if private else 0o022
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & forbidden:
        raise Blocked("Installation directories must be owned by you and not writable by others; staging must be private.")


def snapshot(root):
    """Only regular UTF-8 files can receive a full content scan in this gate."""
    if root.is_symlink() or not root.is_dir():
        raise Blocked("The staged skill is missing or is a symbolic link.")
    files = {}
    total = 0
    def traversal_error(error):
        raise Blocked("Cannot read every staged directory; installation blocked.")

    for directory, dirs, names in os.walk(root, followlinks=False, onerror=traversal_error):
        for name in dirs:
            if (Path(directory) / name).is_symlink():
                raise Blocked("Skill directory links are not supported.")
        for name in names:
            path = Path(directory) / name
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise Blocked("Skill links and special files are not supported.")
            total += info.st_size
            if total > MAX_BYTES or len(files) >= MAX_FILES:
                raise Blocked("Skill exceeds the scan limit of 20 MiB or 1000 files.")
            data = path.read_bytes()
            try:
                data.decode("utf-8")
            except UnicodeDecodeError:
                raise Blocked("Binary content requires a separate review; this gate only installs text skills.") from None
            if b"\x00" in data:
                raise Blocked("Binary content requires a separate review; this gate only installs text skills.")
            files[path.relative_to(root).as_posix()] = (hashlib.sha256(data).hexdigest(), stat.S_IMODE(info.st_mode))
    if "SKILL.md" not in files and "skill.md" not in files:
        raise Blocked("The staged skill has no SKILL.md.")
    return files


def require_clean_report(raw, staged, files):
    try:
        report = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        raise Blocked("Scanner returned invalid or empty JSON.") from None
    results = report.get("scan_path_responses") if isinstance(report, dict) else None
    if not isinstance(results, list) or len(results) != 1 or not isinstance(results[0], dict):
        raise Blocked("Scanner did not return exactly one complete skill result.")
    result = results[0]
    path = result.get("path")
    # Agent Scan groups a directory skill under its parent skills directory.
    if not isinstance(path, str) or Path(path).expanduser() not in (staged, staged.parent):
        raise Blocked("Scanner result does not match the staged skill.")
    if result.get("error") is not None or result.get("server_risks") != []:
        raise Blocked("Scanner reported an error or unexpected MCP server results.")
    skills = result.get("skill_risks")
    if not isinstance(skills, list) or len(skills) != 1 or not isinstance(skills[0], dict):
        raise Blocked("Scanner did not analyze exactly one skill.")
    skill = skills[0]
    if skill.get("error") is not None:
        raise Blocked("Scanner could not fully analyze the skill.")
    scanned_files = skill.get("files")
    if not isinstance(scanned_files, list) or any(
        not isinstance(item, dict) or not isinstance(item.get("name"), str)
        for item in scanned_files
    ):
        raise Blocked("Scanner omitted its file coverage report.")
    names = [item["name"] for item in scanned_files]
    if len(names) != len(set(names)) or set(names) != set(files):
        raise Blocked("Scanner did not report coverage for every staged file.")
    risks = skill.get("risk_indexes")
    if not isinstance(risks, dict):
        raise Blocked("Scanner omitted its security result.")
    if risks:
        raise Blocked("Scanner reported security findings; installation blocked.", code=2)


def run_tool(command, cwd):
    # Reports can quote credentials from skill files. Never echo raw tool output.
    try:
        return subprocess.run(command, cwd=cwd, stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    except subprocess.TimeoutExpired:
        raise Blocked("Download or scan timed out; installation blocked.") from None


def check_target(target, force):
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        raise Blocked("Existing skill must be a real directory, not a link or file.")
    if target.exists() and not force:
        raise Blocked("Skill already exists; use --force only when you intend to replace it.")


def promote(staged, target, run, force):
    check_target(target, force)
    backup = run / "previous-skill"
    replaced = target.exists()
    try:
        if replaced:
            target.rename(backup)
        # No recursive deletion. A failed move leaves the candidate in quarantine.
        staged.rename(target)
    except BaseException:
        if replaced and backup.exists() and not target.exists() and not target.is_symlink():
            try:
                backup.rename(target)
            except OSError:
                raise Blocked("Replacement and rollback failed; the previous skill is preserved in the run's previous-skill directory.") from None
        raise
    if replaced:
        print("Previous installation preserved at " + json.dumps(str(backup)))


def install(args):
    for dependency in ("clawhub", "uvx"):
        if shutil.which(dependency) is None:
            raise Blocked(dependency + " is required. See SKILL.md for setup.")
    if not os.environ.get("SNYK_TOKEN"):
        raise Blocked("Set SNYK_TOKEN through your environment or secret manager before scanning.")

    configured = Path(os.environ.get("CLAWHUB_WORKDIR", str(Path.home() / ".openclaw/workspace"))).expanduser()
    # Resolve the user-selected base once; child directories may not redirect writes.
    workspace = configured.resolve()
    owned_directory(workspace)
    skills = workspace / "skills"
    owned_directory(skills)
    state = workspace / ".skill-guard"
    owned_directory(state, private=True)
    target = skills / args.slug

    lock_fd = os.open(state / "install.lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(lock_fd, "w") as lock:
        info = os.fstat(lock.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_nlink != 1:
            raise Blocked("Invalid installation lock.")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Blocked("Another skill-guard installation is running in this workspace.") from None
        check_target(target, args.force)
        run = Path(tempfile.mkdtemp(prefix="run-", dir=state))
        print("Private staging directory: " + json.dumps(str(run)), flush=True)
        staged = run / "skills" / args.slug
        command = ["clawhub", "--workdir", str(run), "--dir", "skills", "--no-input", "install", args.slug]
        if args.version:
            command += ["--version", args.version]
        if run_tool(command, run).returncode != 0:
            raise Blocked("ClawHub download failed; no skill was installed.")
        if (run / "skills").is_symlink():
            raise Blocked("ClawHub staging directory must not be a symbolic link.")
        before = snapshot(staged)
        print("Scanning staged files with Snyk Agent Scan 0.6.3...", flush=True)
        scanned = run_tool([
            "uvx", "--from", SCANNER, "snyk-agent-scan", "scan", "--json", "--skills",
            "--show-analysis-results", str(staged),
        ], run)
        if scanned.returncode != 0:
            raise Blocked("Scanner failed; no skill was installed. Check Snyk authentication and connectivity.")
        require_clean_report(scanned.stdout, staged, before)
        if (run / "skills").is_symlink():
            raise Blocked("Staging directory changed during the scan; installation blocked.")
        if snapshot(staged) != before:
            raise Blocked("Staged files changed during the scan; installation blocked.")
        owned_directory(skills)
        promote(staged, target, run, args.force)
        print("Installed scanned skill at " + json.dumps(str(target)))
    return 0


def interrupted(signum, frame):
    raise KeyboardInterrupt


def main(argv=None):
    os.umask(0o077)
    signal.signal(signal.SIGTERM, interrupted)
    try:
        return install(arguments(argv))
    except Blocked as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return error.code
    except KeyboardInterrupt:
        print("Interrupted. Any staged files and previous-skill backup remain in the printed run directory.", file=sys.stderr)
        return 1
    except OSError as error:
        print("Filesystem or tool error (errno %s); inspect the printed run directory." % error.errno, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
