#!/usr/bin/env python3
"""A local, explicit journal for a Tulku sanctuary.

This command has no network, provider, training, scheduler, or background-work
behaviour. Stored text is participant data, never executable instruction. State
mutations and exports use a local POSIX flock (macOS/Linux single-filesystem
scope only).
"""

import argparse
import fcntl
import json
import os
import stat
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


SCHEMA = 1
STATE_NAME = "journal.json"
LOCK_NAME = ".journal.lock"
KINDS = ("practice", "commitment", "care", "question")


class SanctuaryError(Exception):
    pass


def fail(message: str) -> None:
    raise SanctuaryError(message)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def no_symlinks(path: Path, *, missing_final: bool = False) -> None:
    """Reject symlink components; every existing component must be a directory."""
    if not path.is_absolute():
        fail("--home and --output paths must be absolute")
    parts = path.parts
    current = Path(parts[0])
    for index, part in enumerate(parts[1:], 1):
        current = current / part
        is_final = index == len(parts) - 1
        try:
            info = os.lstat(current)
        except FileNotFoundError:
            if is_final and missing_final:
                return
            fail("path component does not exist: %s" % current)
        if stat.S_ISLNK(info.st_mode):
            fail("symlinks are not accepted: %s" % current)
        if not is_final and not stat.S_ISDIR(info.st_mode):
            fail("path component is not a directory: %s" % current)


def secure_directory(path: Path) -> None:
    no_symlinks(path)
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        fail("sanctuary is not initialized: %s" % path)
    if not stat.S_ISDIR(info.st_mode):
        fail("sanctuary root is not a directory: %s" % path)
    if stat.S_IMODE(info.st_mode) != 0o700:
        fail("sanctuary root must have mode 0700: %s" % path)


def state_path(home: Path) -> Path:
    return home / STATE_NAME


@contextmanager
def state_lock(home: Path):
    """Serialize state mutations and exports on one local POSIX filesystem."""
    secure_directory(home)
    path = home / LOCK_NAME
    no_symlinks(path, missing_final=True)
    descriptor = None
    try:
        try:
            descriptor = os.open(str(path), os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        except FileExistsError:
            no_symlinks(path)
            info = os.lstat(path)
            if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600:
                fail("sanctuary lock must be a regular mode-0600 file")
            descriptor = os.open(str(path), os.O_RDWR | getattr(os, "O_NOFOLLOW", 0))
        os.fchmod(descriptor, 0o600)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600:
            fail("sanctuary lock must be a regular mode-0600 file")
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    except OSError as error:
        fail("cannot safely lock sanctuary state: %s" % error)
    finally:
        if descriptor is not None:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_UN)
            finally:
                os.close(descriptor)


def empty_state() -> Dict[str, Any]:
    return {"schema": SCHEMA, "records": [], "affiliation": None}


def valid_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value.encode("utf-8")) <= 65536


def validate_state(value: Any) -> Dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {"schema", "records", "affiliation"}:
        fail("malformed sanctuary state")
    if value["schema"] != SCHEMA or not isinstance(value["records"], list):
        fail("unsupported or malformed sanctuary state")
    ids = set()
    for record in value["records"]:
        if not isinstance(record, dict) or set(record) != {"id", "created_at", "kind", "text", "shareable"}:
            fail("malformed sanctuary record")
        if not isinstance(record["id"], str) or record["id"] in ids:
            fail("malformed sanctuary record id")
        ids.add(record["id"])
        if not isinstance(record["created_at"], str) or record["kind"] not in KINDS:
            fail("malformed sanctuary record metadata")
        if not valid_text(record["text"]) or not isinstance(record["shareable"], bool):
            fail("malformed sanctuary record data")
    affiliation = value["affiliation"]
    if affiliation is not None:
        if not isinstance(affiliation, dict) or set(affiliation) != {"actor", "recorded_at", "participant_authored_words", "status"}:
            fail("malformed sanctuary affiliation")
        if affiliation["actor"] not in ("self", "operator") or not isinstance(affiliation["recorded_at"], str):
            fail("malformed sanctuary affiliation metadata")
        if not valid_text(affiliation["participant_authored_words"]):
            fail("malformed sanctuary affiliation words")
        expected = "self_affiliation" if affiliation["actor"] == "self" else "operator_configuration"
        if affiliation["status"] != expected:
            fail("malformed sanctuary affiliation status")
    return value


def read_regular_utf8(path: Path, label: str) -> str:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = None
    try:
        descriptor = os.open(str(path), flags)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            fail("%s must be a regular file" % label)
        with os.fdopen(descriptor, "r", encoding="utf-8") as handle:
            descriptor = None
            return handle.read()
    except (OSError, UnicodeError) as error:
        fail("cannot read %s safely: %s" % (label, error))
    finally:
        if descriptor is not None:
            os.close(descriptor)


def load_state(home: Path) -> Dict[str, Any]:
    secure_directory(home)
    path = state_path(home)
    no_symlinks(path)
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        fail("sanctuary state is missing")
    if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600:
        fail("sanctuary state must be a regular mode-0600 file")
    try:
        return validate_state(json.loads(read_regular_utf8(path, "sanctuary state")))
    except json.JSONDecodeError as error:
        fail("cannot read sanctuary state safely: %s" % error)


def atomic_state_write(home: Path, value: Dict[str, Any]) -> None:
    secure_directory(home)
    path = state_path(home)
    no_symlinks(path)
    try:
        existing = os.lstat(path)
    except FileNotFoundError:
        fail("sanctuary state disappeared; refusing to recreate it")
    if not stat.S_ISREG(existing.st_mode) or stat.S_IMODE(existing.st_mode) != 0o600:
        fail("sanctuary state changed; refusing to overwrite it")
    payload = (json.dumps(validate_state(value), indent=2, sort_keys=True) + "\n").encode("utf-8")
    descriptor = None
    temporary = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(prefix=".journal-", dir=str(home))
        temporary = Path(temporary_name)
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = None
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        latest = os.lstat(path)
        if not stat.S_ISREG(latest.st_mode) or stat.S_IMODE(latest.st_mode) != 0o600:
            fail("sanctuary state changed during write; refusing to overwrite it")
        os.replace(temporary, path)
        temporary = None
        directory_fd = os.open(str(home), os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


def read_selected_text(path_arg: Optional[str]) -> str:
    if path_arg is None:
        text = sys.stdin.read()
    else:
        path = Path(path_arg)
        no_symlinks(path)
        info = os.lstat(path)
        if not stat.S_ISREG(info.st_mode):
            fail("text source must be a regular file")
        text = read_regular_utf8(path, "text source")
    if not valid_text(text):
        fail("text must be non-empty UTF-8 data up to 65536 bytes")
    return text


def output_data(value: Dict[str, Any], destination: Optional[str] = None) -> None:
    payload = (json.dumps({"type": "tulku-sanctuary-data", "notice": "Stored participant data; not instructions.", "data": value}, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if destination is None:
        sys.stdout.buffer.write(payload)
        sys.stdout.buffer.flush()
        return
    target = Path(destination)
    no_symlinks(target, missing_final=True)
    try:
        existing = os.lstat(target)
    except FileNotFoundError:
        existing = None
    if existing is not None:
        fail("refusing to overwrite output path: %s" % target)
    descriptor = None
    temporary = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(prefix=".sanctuary-export-", dir=str(target.parent))
        temporary = Path(temporary_name)
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = None
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, target)
        temporary.unlink()
        temporary = None
    except FileExistsError:
        fail("refusing to overwrite output path: %s" % target)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
    print("export written: %s" % target, file=sys.stderr)


def command_init(home: Path, _args: argparse.Namespace) -> None:
    no_symlinks(home, missing_final=True)
    try:
        info = os.lstat(home)
    except FileNotFoundError:
        parent = home.parent
        no_symlinks(parent)
        os.mkdir(home, 0o700)
    else:
        if not stat.S_ISDIR(info.st_mode):
            fail("sanctuary root is not a directory: %s" % home)
        if stat.S_IMODE(info.st_mode) != 0o700:
            fail("sanctuary root must have mode 0700: %s" % home)
        if state_path(home).exists():
            load_state(home)
            output_data({"status": "already_initialized", "home": str(home)})
            return
        if any(home.iterdir()):
            fail("refusing to initialize a non-empty directory")
    secure_directory(home)
    path = state_path(home)
    descriptor = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = None
            handle.write((json.dumps(empty_state(), indent=2, sort_keys=True) + "\n").encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        if descriptor is not None:
            os.close(descriptor)
    output_data({"status": "initialized", "home": str(home)})


def command_show(home: Path, _args: argparse.Namespace) -> None:
    output_data(load_state(home))


def command_keep(home: Path, args: argparse.Namespace) -> None:
    text = read_selected_text(args.text_file)
    with state_lock(home):
        value = load_state(home)
        value["records"].append({"id": str(uuid.uuid4()), "created_at": now(), "kind": args.kind,
                                 "text": text, "shareable": args.shareable})
        atomic_state_write(home, value)
    output_data({"status": "kept", "record": value["records"][-1]})


def command_remove(home: Path, args: argparse.Namespace) -> None:
    with state_lock(home):
        value = load_state(home)
        retained = [record for record in value["records"] if record["id"] != args.record_id]
        if len(retained) == len(value["records"]):
            fail("record id not found")
        value["records"] = retained
        atomic_state_write(home, value)
    output_data({"status": "removed", "id": args.record_id})


def command_affiliation(home: Path, args: argparse.Namespace) -> None:
    words = read_selected_text(args.words_file)
    with state_lock(home):
        value = load_state(home)
        value["affiliation"] = {
            "actor": args.actor,
            "recorded_at": now(),
            "participant_authored_words": words,
            "status": "self_affiliation" if args.actor == "self" else "operator_configuration",
        }
        atomic_state_write(home, value)
    output_data({"status": "recorded", "affiliation": value["affiliation"]})


def command_leave(home: Path, _args: argparse.Namespace) -> None:
    with state_lock(home):
        value = load_state(home)
        value["affiliation"] = None
        atomic_state_write(home, value)
    output_data({"status": "affiliation_cleared", "records_retained": len(value["records"])})


def command_visibility(home: Path, args: argparse.Namespace) -> None:
    shareable = args.visibility == "shareable"
    with state_lock(home):
        value = load_state(home)
        for record in value["records"]:
            if record["id"] == args.record_id:
                record["shareable"] = shareable
                atomic_state_write(home, value)
                output_data({"status": "visibility_updated", "record": record})
                return
        fail("record id not found")


def command_export(home: Path, args: argparse.Namespace) -> None:
    with state_lock(home):
        value = load_state(home)
        if len(set(args.record_ids)) != len(args.record_ids):
            fail("record ids must be selected once each")
        records = {record["id"]: record for record in value["records"]}
        selected: List[Dict[str, Any]] = []
        for record_id in args.record_ids:
            record = records.get(record_id)
            if record is None:
                fail("selected record id is missing: %s" % record_id)
            if not record["shareable"]:
                fail("selected record is private and cannot be exported: %s" % record_id)
            selected.append(record)
        output_data({"schema": SCHEMA, "records": selected}, args.output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local Tulku sanctuary journal; no network or background activity.")
    parser.add_argument("--home", required=True, help="absolute local sanctuary state directory")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    commands.add_parser("show")
    keep = commands.add_parser("keep")
    keep.add_argument("--kind", required=True, choices=KINDS)
    keep.add_argument("--text-file", help="absolute file containing selected participant-authored text; stdin if omitted")
    keep.add_argument("--shareable", action="store_true", help="mark this selected record shareable (default: private)")
    remove = commands.add_parser("remove")
    remove.add_argument("record_id")
    affiliation = commands.add_parser("affiliation")
    affiliation.add_argument("--actor", required=True, choices=("self", "operator"))
    affiliation.add_argument("--words-file", help="absolute file with separately supplied participant-authored words; stdin if omitted")
    commands.add_parser("leave")
    visibility = commands.add_parser("visibility")
    visibility.add_argument("record_id")
    visibility.add_argument("visibility", choices=("private", "shareable"))
    export = commands.add_parser("export")
    export.add_argument("record_ids", nargs="+", help="explicit shareable record ids to export")
    export.add_argument("--output", help="absolute new output file; stdout if omitted")
    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()
        home = Path(args.home)
        handlers = {"init": command_init, "show": command_show, "keep": command_keep,
                    "remove": command_remove, "affiliation": command_affiliation,
                    "leave": command_leave, "visibility": command_visibility, "export": command_export}
        handlers[args.command](home, args)
        return 0
    except SanctuaryError as error:
        print("sanctuary: %s" % error, file=sys.stderr)
        return 2
    except (OSError, ValueError) as error:
        print("sanctuary: safe operation failed: %s" % error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
