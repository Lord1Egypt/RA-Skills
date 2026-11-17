"""Private offline recording and explicit, preview-first launchd management."""

import argparse
from contextlib import contextmanager, ExitStack
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import plistlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


MANIFEST = Path(__file__).with_name("cli-release.json")
LOCAL_AGENTS = ("codex", "claude", "openclaw", "hermes", "opencode", "deepseek", "workbuddy", "workbuddy-ai")
AGENTS = LOCAL_AGENTS + ("trae-cn", "all")
LABEL = "com.baijian.ai-token-ayalysis"
SNAPSHOT = re.compile(r"token-stats-(?:" + "|".join(AGENTS) + r")-\d{4}-\d{2}-\d{2}-[0-9a-f]{32}\.json\Z")
LEGACY_SNAPSHOT = re.compile(r"(?:" + "|".join(AGENTS) + r")-\d{4}-\d{2}-\d{2}-\d{8}T\d{6}[+-]\d{4}\.json\Z")


class SafetyError(Exception):
    pass


def absolute(value):
    path = Path(value).expanduser()
    if ".." in path.parts or "\x00" in str(path):
        raise SafetyError("Parent traversal is not allowed")
    return Path(os.path.abspath(path))


def file_info(fd, name, private=True):
    try:
        info = os.stat(name, dir_fd=fd, follow_symlinks=False)
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_nlink != 1:
        raise SafetyError("Expected an owned, regular, single-link file")
    if private and stat.S_IMODE(info.st_mode) != 0o600:
        raise SafetyError("Existing file is not private; explicit permission repair is required")
    return info


@contextmanager
def directory(path, create=False, private=True, repair=False, validate_only=False):
    """Walk via held directory descriptors; never follow output-path symlinks."""
    path = absolute(path)
    if private and path in (Path("/"), Path.home()):
        raise SafetyError("A dedicated private directory is required")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for index, part in enumerate(path.parts[1:]):
            if create:
                try:
                    os.mkdir(part, 0o700, dir_fd=fd)
                except FileExistsError:
                    pass
            new_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = new_fd
            info = os.fstat(fd)
            leaf = index == len(path.parts) - 2
            if leaf and private:
                if info.st_uid != os.getuid():
                    raise SafetyError("Private directory must belong to the current user")
                if stat.S_IMODE(info.st_mode) != 0o700:
                    if not repair:
                        raise SafetyError("Existing directory is not 0700; use --repair-permissions with confirmation")
                    if not validate_only:
                        os.fchmod(fd, 0o700)
            else:
                sticky_root = info.st_uid == 0 and bool(info.st_mode & stat.S_ISVTX)
                if info.st_uid not in (0, os.getuid()) or (info.st_mode & 0o022 and not sticky_root):
                    raise SafetyError("Output path has an untrusted writable ancestor")
        yield fd
    finally:
        os.close(fd)


def preflight(path, private=True, repair=False):
    try:
        with directory(path, private=private, repair=repair, validate_only=True):
            pass
    except FileNotFoundError:
        pass


def read_file(fd, name, private=False):
    info = file_info(fd, name, private=private)
    if info is None:
        return None
    if info.st_mode & 0o022:
        raise SafetyError("Refusing to read a configuration writable by other users")
    file_fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
    with os.fdopen(file_fd, "rb") as stream:
        return stream.read()


def atomic_write(fd, name, content, repair=False):
    if "/" in name or name in (".", ".."):
        raise SafetyError("Invalid output filename")
    file_info(fd, name, private=not repair)
    temp = ".token-stats-" + uuid.uuid4().hex + ".tmp"
    raw_fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
    try:
        with os.fdopen(raw_fd, "wb") as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, name, src_dir_fd=fd, dst_dir_fd=fd)
        os.fsync(fd)
    finally:
        try:
            os.unlink(temp, dir_fd=fd)
        except FileNotFoundError:
            pass


@contextmanager
def job_lock(fd, label):
    name = "." + label + ".lock"
    file_info(fd, name)
    lock_fd = os.open(name, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600, dir_fd=fd)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        os.close(lock_fd)


def trusted_binary(value):
    found = shutil.which(value) if "/" not in value else str(absolute(value))
    if not found:
        raise SafetyError("CLI missing; explicitly install the pinned release first")
    path = Path(found).resolve(strict=True)
    with directory(path.parent, private=False):
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, "rb") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid not in (0, os.getuid()) or info.st_mode & 0o022:
                raise SafetyError("CLI must be a trusted-owner, non-writable-by-others regular file")
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    architecture = {"aarch64": "arm64", "x86_64": "amd64"}.get(platform.machine().lower(), platform.machine().lower())
    target = platform.system().lower() + "_" + architecture
    manifest = json.loads(MANIFEST.read_text())
    expected = manifest["artifacts"].get(target, {}).get("binary_sha256")
    if digest.hexdigest() != expected:
        raise SafetyError("CLI SHA-256 does not match the pinned release; no execution performed")
    if not os.access(path, os.X_OK):
        raise SafetyError("Verified CLI is not executable")
    return str(path), expected


def record_options(env):
    agent = env.get("AI_TOKEN_AGENT") or "codex"
    day = env.get("AI_TOKEN_DAY") or dt.date.today().isoformat()
    if agent not in AGENTS or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise SafetyError("Invalid agent or calendar day")
    dt.date.fromisoformat(day)
    retention = int(env.get("AI_TOKEN_RETENTION_DAYS") or "0")
    if not 0 <= retention <= 3650:
        raise SafetyError("Retention must be 0 (disabled) or 1-3650 days")
    run_dir = absolute(env["AI_TOKEN_RUN_DIR"]) if env.get("AI_TOKEN_RUN_DIR") else None
    if retention and run_dir is None:
        raise SafetyError("Retention requires an explicit snapshot directory")
    data_dir = absolute(env.get("AI_TOKEN_DATA_DIR") or str(Path.home() / ".local/data/cycling-health-cli/token-usage"))
    status_file = absolute(env["AI_TOKEN_STATUS_FILE"]) if env.get("AI_TOKEN_STATUS_FILE") else None
    mode = env.get("AI_TOKEN_OUTPUT") or "json"
    if mode not in ("json", "summary", "quiet"):
        raise SafetyError("Output must be json, summary, or quiet")
    return agent, day, retention, run_dir, data_dir, status_file, mode


def prune_snapshots(fd, days):
    if not days:
        return
    cutoff = dt.datetime.now().timestamp() - days * 86400
    candidates = []
    for name in os.listdir(fd):
        if SNAPSHOT.fullmatch(name):
            info = file_info(fd, name)
            if info.st_mtime < cutoff:
                candidates.append(name)
    for name in candidates:
        os.unlink(name, dir_fd=fd)


def record(env):
    agent, day, retention, run_dir, data_dir, status_file, mode = record_options(env)
    binary, _ = trusted_binary(env.get("TOKEN_STATS_BIN") or env.get("AI_TOKEN_STATS_BIN") or "token-stats")
    for path in (data_dir, data_dir / agent, run_dir, status_file.parent if status_file else None):
        if path is not None:
            preflight(path)
    args = [binary, "usage", "--agent", agent, "--day", day, "--refresh", "--output", "json", "--data-dir", str(data_dir)]
    for source in LOCAL_AGENTS:
        home = env.get("AI_TOKEN_" + source.upper().replace("-", "_") + "_HOME")
        if home:
            args.extend(["--" + source + "-home", str(absolute(home))])
    with ExitStack() as stack:
        stack.enter_context(directory(data_dir, create=True))
        agent_fd = stack.enter_context(directory(data_dir / agent, create=True))
        file_info(agent_fd, day + ".json")
        run_fd = stack.enter_context(directory(run_dir, create=True)) if run_dir else None
        status_fd = stack.enter_context(directory(status_file.parent, create=True)) if status_file else None
        if status_fd is not None:
            file_info(status_fd, status_file.name)
        with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
            result = subprocess.run(args, stdout=output, stderr=errors, env=env, check=False)
            if result.returncode:
                raise SafetyError("CLI collection failed; raw stderr was not persisted")
            output.seek(0)
            report = json.load(output)
        if not isinstance(report, dict) or report.get("agent") != agent or report.get("day") != day or not isinstance(report.get("total"), dict):
            raise SafetyError("Unexpected CLI report; no snapshot saved")
        total = report["total"].get("totalTokens")
        warnings = report.get("warnings") or []
        if type(total) is not int or total < 0 or not isinstance(warnings, list):
            raise SafetyError("Unexpected CLI counters or warnings; no snapshot saved")
        summary = {"agent": agent, "day": day, "recordedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
                   "status": "ok", "totalTokens": total, "warningCount": len(warnings)}
        if run_fd is not None:
            name = "token-stats-" + agent + "-" + day + "-" + uuid.uuid4().hex + ".json"
            atomic_write(run_fd, name, (json.dumps(report) + "\n").encode())
            prune_snapshots(run_fd, retention)
        if status_fd is not None:
            atomic_write(status_fd, status_file.name, (json.dumps(summary) + "\n").encode())
        if mode != "quiet":
            print(json.dumps(report if mode == "json" else summary))


def failed_status(env):
    if not env.get("AI_TOKEN_STATUS_FILE"):
        return
    path = absolute(env["AI_TOKEN_STATUS_FILE"])
    with directory(path.parent) as fd:
        atomic_write(fd, path.name, json.dumps({"status": "failed", "recordedAt": dt.datetime.now(dt.timezone.utc).isoformat()}).encode())


def launchctl(*args):
    return subprocess.run(["/bin/launchctl", *args], capture_output=True, text=True, check=False)


def loaded(label):
    result = launchctl("print", "gui/" + str(os.getuid()) + "/" + label)
    if result.returncode == 0:
        return True
    if "Could not find service" in result.stderr:
        return False
    raise SafetyError("Cannot determine launchd state; no job change attempted")


def service_call(*args):
    if launchctl(*args).returncode:
        raise SafetyError("launchctl operation failed: " + args[0])


def owned_plist(raw, label):
    value = plistlib.loads(raw)
    if not isinstance(value, dict) or value.get("Label") != label:
        raise SafetyError("Existing plist has a different label")
    marker = value.get("TokenStatsSkillRecorder")
    arguments = value.get("ProgramArguments")
    runtime = str(Path.home() / ".local/state/token-stats-skill" / label)
    managed = (marker == 1 and isinstance(arguments, list) and len(arguments) == 4
               and arguments[1] == "-I" and arguments[3] == "record"
               and isinstance(arguments[2], str)
               and re.fullmatch(re.escape(runtime) + r"/[0-9a-f]{20}/token_recorder\.py", arguments[2]))
    legacy = arguments == ["/bin/sh", str(Path(__file__).with_name("record-token-usage.sh"))]
    if not managed and not legacy:
        raise SafetyError("Refusing to manage a plist not owned by this recorder")
    return value


def repair_files(fd, logs, reports):
    names = []
    for name in os.listdir(fd):
        allowed = logs and (name in ("stdout.log", "stderr.log") or re.fullmatch(r"[A-Za-z0-9.-]+\.status\.json", name))
        allowed = allowed or (reports and (SNAPSHOT.fullmatch(name) or LEGACY_SNAPSHOT.fullmatch(name)
                                          or re.fullmatch(r"\d{4}-\d{2}-\d{2}\.json", name)))
        if allowed:
            file_info(fd, name, private=False)
            names.append(name)
    for name in names:
        child = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
        try:
            os.fchmod(child, 0o600)
        finally:
            os.close(child)


def manage(args):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]{0,127}", args.label):
        raise SafetyError("Label must contain only letters, digits, dots, and hyphens")
    if args.interval < 60 or args.interval > 2147483647:
        raise SafetyError("Interval must be 60-2147483647 seconds")
    if args.retention_days < 0 or args.retention_days > 3650 or (args.retention_days and not args.run_dir):
        raise SafetyError("Retention requires --run-dir and 1-3650 days")
    if args.timezone:
        try:
            ZoneInfo(args.timezone)
        except (ZoneInfoNotFoundError, ValueError):
            raise SafetyError("Timezone must be an installed IANA timezone name") from None
    launch_dir = absolute(Path.home() / "Library/LaunchAgents")
    plist_path = launch_dir / (args.label + ".plist")
    raw = None
    try:
        with directory(launch_dir, private=False) as fd:
            raw = read_file(fd, plist_path.name)
    except FileNotFoundError:
        pass
    previous = owned_plist(raw, args.label) if raw else None
    plan = {"action": args.action, "label": args.label, "plist": str(plist_path), "existing": bool(raw), "confirmed": args.confirm}
    if args.action == "status":
        plan["loaded"] = loaded(args.label)
        plan["statusFile"] = str(Path.home() / "Library/Logs/ai-token-ayalysis" / (args.label + ".status.json"))
        print(json.dumps(plan, indent=2))
        return
    if args.action == "install":
        binary, binary_hash = trusted_binary(args.bin)
        helper_bytes = Path(__file__).read_bytes()
        manifest_bytes = MANIFEST.read_bytes()
        generation = hashlib.sha256(helper_bytes + manifest_bytes).hexdigest()[:20]
        runtime = absolute(Path.home() / ".local/state/token-stats-skill" / args.label / generation)
        log_dir = absolute(Path.home() / "Library/Logs/ai-token-ayalysis")
        data_dir = absolute(args.data_dir or str(Path.home() / ".local/data/cycling-health-cli/token-usage"))
        run_dir = absolute(args.run_dir) if args.run_dir else None
        for path in (runtime, log_dir, data_dir, data_dir / args.agent, run_dir):
            if path is not None:
                preflight(path, repair=args.repair_permissions)
        env = {"HOME": str(Path.home()), "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "TOKEN_STATS_BIN": binary,
               "AI_TOKEN_AGENT": args.agent, "AI_TOKEN_DATA_DIR": str(data_dir), "AI_TOKEN_OUTPUT": "quiet",
               "AI_TOKEN_STATUS_FILE": str(log_dir / (args.label + ".status.json"))}
        if args.timezone:
            env["TZ"] = args.timezone
        if run_dir:
            env.update(AI_TOKEN_RUN_DIR=str(run_dir), AI_TOKEN_RETENTION_DAYS=str(args.retention_days))
        for source in LOCAL_AGENTS:
            home = getattr(args, source.replace("-", "_") + "_home")
            if home:
                env["AI_TOKEN_" + source.upper().replace("-", "_") + "_HOME"] = str(absolute(home))
        value = {"Label": args.label, "TokenStatsSkillRecorder": 1,
                 "ProgramArguments": [str(Path(sys.executable).resolve()), "-I", str(runtime / "token_recorder.py"), "record"],
                 "EnvironmentVariables": env, "StartInterval": args.interval, "RunAtLoad": False, "Umask": 0o077,
                 "StandardOutPath": "/dev/null", "StandardErrorPath": "/dev/null"}
        payload = plistlib.dumps(value)
        plan.update(binary=binary, binarySha256=binary_hash, agent=args.agent, interval=args.interval,
                    dataDirectory=str(data_dir), snapshotDirectory=str(run_dir) if run_dir else None,
                    retentionDays=args.retention_days, statusFile=env["AI_TOKEN_STATUS_FILE"],
                    sourceOverrides={key: item for key, item in env.items() if key.endswith("_HOME")},
                    runtimeDirectory=str(runtime), startNow=args.start_now, replace=args.replace,
                    repairPermissions=args.repair_permissions, timezone=args.timezone or "system local",
                    networkSync=False)
    if not args.confirm:
        print(json.dumps(plan, indent=2))
        return
    if platform.system() != "Darwin":
        raise SafetyError("launchd management is supported only on macOS")
    if args.action == "install" and raw and not args.replace:
        raise SafetyError("Existing task requires --replace as well as --confirm")
    if args.action != "install" and previous is None:
        raise SafetyError("No owned recorder plist found")
    with directory(launch_dir, create=True, private=False) as fd, job_lock(fd, args.label):
        if read_file(fd, plist_path.name) != raw:
            raise SafetyError("Task changed since preview; inspect it again")
        was_loaded = loaded(args.label)
        if args.action == "install" and was_loaded and previous is None:
            raise SafetyError("An unrelated loaded job already uses this label")
        if args.action != "install":
            if was_loaded:
                service_call("bootout", "gui/" + str(os.getuid()) + "/" + args.label)
            if args.action == "uninstall":
                file_info(fd, plist_path.name, private=False)
                os.unlink(plist_path.name, dir_fd=fd)
            print(json.dumps(dict(plan, result="done", historyPreserved=True)))
            return
        with ExitStack() as stack:
            for path in (log_dir, data_dir, data_dir / args.agent, run_dir):
                if path is not None:
                    private_fd = stack.enter_context(directory(path, create=True, repair=args.repair_permissions))
                    if args.repair_permissions:
                        repair_files(private_fd, path == log_dir, path in (data_dir / args.agent, run_dir))
            runtime_fd = stack.enter_context(directory(runtime, create=True))
            atomic_write(runtime_fd, "token_recorder.py", helper_bytes)
            atomic_write(runtime_fd, "cli-release.json", manifest_bytes)
            with directory(log_dir) as status_fd:
                atomic_write(status_fd, Path(env["AI_TOKEN_STATUS_FILE"]).name, b'{"status":"not-run"}\n', repair=args.repair_permissions)
        if was_loaded:
            service_call("bootout", "gui/" + str(os.getuid()) + "/" + args.label)
        try:
            atomic_write(fd, plist_path.name, payload, repair=True)
            service_call("bootstrap", "gui/" + str(os.getuid()), str(plist_path))
            if args.start_now:
                service_call("kickstart", "gui/" + str(os.getuid()) + "/" + args.label)
        except (OSError, SafetyError):
            # Restore the previous registration after an unsuccessful replacement.
            if loaded(args.label):
                service_call("bootout", "gui/" + str(os.getuid()) + "/" + args.label)
            if raw:
                atomic_write(fd, plist_path.name, raw, repair=True)
                if was_loaded:
                    service_call("bootstrap", "gui/" + str(os.getuid()), str(plist_path))
            elif file_info(fd, plist_path.name) is not None:
                os.unlink(plist_path.name, dir_fd=fd)
            raise
    print(json.dumps(dict(plan, result="installed"), indent=2))


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("record", help="Offline collection; options come from AI_TOKEN_* environment variables")
    verify = commands.add_parser("verify", help="Verify the pinned CLI without executing it")
    verify.add_argument("--bin", default="token-stats")
    install = commands.add_parser("install", help="Preview first; --confirm is required for service changes")
    install.add_argument("--action", choices=("install", "status", "stop", "uninstall"), default="install")
    install.add_argument("--label", default=LABEL)
    install.add_argument("--agent", choices=AGENTS, default="codex")
    install.add_argument("--interval", type=int, default=1800)
    install.add_argument("--bin", default=os.environ.get("TOKEN_STATS_BIN") or os.environ.get("AI_TOKEN_STATS_BIN") or "token-stats")
    install.add_argument("--data-dir")
    install.add_argument("--timezone", help="Explicit IANA timezone, e.g. Asia/Shanghai; otherwise system local")
    install.add_argument("--run-dir", help="Opt in to per-run snapshots")
    install.add_argument("--retention-days", type=int, default=0, help="Opt-in deletion of this recorder's snapshots only; 0 disables deletion")
    install.add_argument("--confirm", action="store_true")
    install.add_argument("--replace", action="store_true")
    install.add_argument("--start-now", action="store_true")
    install.add_argument("--repair-permissions", action="store_true", help="Repair only owned dedicated output directories and recognized files")
    for source in LOCAL_AGENTS:
        install.add_argument("--" + source + "-home")
    return root


def main():
    os.umask(0o077)
    args = parser().parse_args()
    try:
        if args.command == "record":
            record(dict(os.environ))
        elif args.command == "verify":
            binary, digest = trusted_binary(args.bin)
            print(json.dumps({"binary": binary, "sha256": digest, "verified": True}))
        else:
            manage(args)
    except (SafetyError, OSError, ValueError, KeyError, plistlib.InvalidFileException) as error:
        if args.command == "record":
            try:
                failed_status(os.environ)
            except (SafetyError, OSError, ValueError):
                pass
        message = str(error) if isinstance(error, SafetyError) else "Invalid data, permissions, or filesystem operation"
        print("token-stats recorder: " + message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
