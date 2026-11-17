#!/usr/bin/env python3
"""Preview, create and restore a TokenLab Codex profile. Python 3.11+, no dependencies."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11 or newer is required; no packages need to be installed.")

import tomllib

from setup_files import SetupError, SafeParser, read_file, require_same, atomic_write, setup_lock


BASE_URL = "https://api.tokenlab.sh/v1"
KEY_ENV = "TOKENLAB_API_KEY"
MIN_VERSION = (0, 134, 0)
MARKER = "# TokenLab Codex setup v1"


def parse_config(content: bytes | None, label: str) -> dict:
    try:
        return tomllib.loads((content or b"").decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError):
        raise SetupError(f"Cannot parse {label}; existing contents were not printed.") from None


def check_profile_name(profile: str) -> None:
    if not re.fullmatch(r"tokenlab(?:[-_][A-Za-z0-9_-]{1,48})?", profile):
        raise SetupError("Use tokenlab or a name such as tokenlab-personal for --profile.")


def render_profile(profile: str, model: str, effort: str | None) -> bytes:
    check_profile_name(profile)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}", model) or model.startswith("sk-"):
        raise SetupError("Supply a public TokenLab model ID, not a key or configuration text.")
    lines = [f"model = {json.dumps(model)}", f"model_provider = {json.dumps(profile)}"]
    if effort is not None:
        if effort not in {"none", "minimal", "low", "medium", "high", "xhigh"}:
            raise SetupError("Unsupported reasoning effort.")
        lines.append(f"model_reasoning_effort = {json.dumps(effort)}")
    lines += ["", f"[model_providers.{profile}]", 'name = "TokenLab"',
              f"base_url = {json.dumps(BASE_URL)}", 'wire_api = "responses"',
              f"env_key = {json.dumps(KEY_ENV)}", ""]
    body = "\n".join(lines).encode()
    digest = hashlib.sha256(body).hexdigest()
    return f"{MARKER}; profile={profile}; sha256={digest}\n".encode() + body


def require_managed(content: bytes, profile: str, label: str) -> None:
    header, separator, body = content.partition(b"\n")
    digest = hashlib.sha256(body).hexdigest()
    expected = f"{MARKER}; profile={profile}; sha256={digest}".encode()
    if not separator or header != expected:
        raise SetupError(f"{label} belongs to another setup or was edited. It will not be overwritten.")
    parse_config(body, label)


def detect_codex(executable: str | None = None) -> tuple[str, str]:
    command = shutil.which(executable or "codex")
    if not command:
        raise SetupError("Codex was not found. Install it from the official guide, then retry.")
    # Even discovery commands get a disposable home and no API-key environment.
    with tempfile.TemporaryDirectory(prefix="tokenlab-codex-detect-") as directory:
        environment = {key: os.environ[key] for key in ("PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "COMSPEC", "PATHEXT") if key in os.environ}
        environment.update(HOME=directory, USERPROFILE=directory, CODEX_HOME=directory,
                           APPDATA=directory, LOCALAPPDATA=directory, TMPDIR=directory,
                           TMP=directory, TEMP=directory)
        try:
            version = subprocess.run([command, "--version"], env=environment, cwd=directory,
                                     capture_output=True, text=True, timeout=10, check=True)
            help_result = subprocess.run([command, "--help"], env=environment, cwd=directory,
                                         capture_output=True, text=True, timeout=10, check=True)
        except (OSError, subprocess.SubprocessError):
            raise SetupError("Could not inspect Codex. No client output or credentials were printed.") from None
    match = re.search(r"\bcodex-cli (\d+)\.(\d+)\.(\d+)\b", version.stdout)
    if not match or tuple(map(int, match.groups())) < MIN_VERSION:
        raise SetupError("This helper requires Codex 0.134.0+ with separate profile files.")
    if "--profile" not in help_result.stdout or "<name>.config.toml" not in help_result.stdout:
        raise SetupError("Installed Codex does not advertise the supported profile-file interface.")
    return command, ".".join(match.groups())


@dataclass(frozen=True)
class Plan:
    root: Path
    profile: str
    action: str
    base: bytes | None
    before: bytes | None
    backup: bytes | None
    after: bytes | None

    @property
    def target(self) -> Path:
        return self.root / f"{self.profile}.config.toml"

    @property
    def backup_path(self) -> Path:
        return self.root / f".{self.profile}.config.toml.tokenlab-backup"


def prepare(root: Path, profile: str, desired: bytes | None, restore: bool = False) -> Plan:
    check_profile_name(profile)
    base = read_file(root / "config.toml", allow_links=True)
    config = parse_config(base, "config.toml")
    target = root / f"{profile}.config.toml"
    backup_path = root / f".{profile}.config.toml.tokenlab-backup"
    before, backup = read_file(target), read_file(backup_path)
    if before is not None:
        require_managed(before, profile, target.name)
    if backup is not None:
        require_managed(backup, profile, backup_path.name)
    if before is None and backup is not None:
        raise SetupError("Profile is missing but a backup remains. Inspect it before making changes.")
    if restore:
        action = "restore" if backup is not None else "remove" if before is not None else "unchanged"
        return Plan(root, profile, action, base, before, backup, backup)
    for table_name in ("model_providers", "profiles"):
        table = config.get(table_name, {})
        if not isinstance(table, dict):
            raise SetupError("A provider/profile table in config.toml has an invalid shape.")
        if profile in table:
            raise SetupError("That provider/profile name exists in config.toml. Choose a different --profile.")
    if desired is None:
        raise SetupError("--model is required when configuring a profile.")
    action = "unchanged" if before == desired else "create" if before is None else "update"
    return Plan(root, profile, action, base, before, backup, desired)


def apply(plan: Plan) -> None:
    if plan.action == "unchanged":
        return
    plan.root.mkdir(parents=True, exist_ok=True)
    with setup_lock(plan.root, plan.profile):
        require_same(plan.root / "config.toml", plan.base, allow_links=True)
        require_same(plan.target, plan.before)
        require_same(plan.backup_path, plan.backup)
        if plan.action == "update":
            atomic_write(plan.backup_path, plan.before, plan.backup)
        if plan.after is None:
            require_same(plan.target, plan.before)
            plan.target.unlink()
        else:
            atomic_write(plan.target, plan.after, plan.before)
        if plan.action == "restore":
            require_same(plan.backup_path, plan.backup)
            plan.backup_path.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--codex-home", type=Path, help="Explicit configuration directory; otherwise CODEX_HOME or ~/.codex")
    parser.add_argument("--codex-bin", help="Installed Codex executable (never an installation command)")
    parser.add_argument("--profile", default="tokenlab", help="tokenlab or tokenlab-<name>")
    parser.add_argument("--model", help="Public model ID supporting Responses; no availability claim is made")
    parser.add_argument("--reasoning-effort", help="Optional supported effort; otherwise keep inherited settings")
    parser.add_argument("--restore", action="store_true", help="Preview restoring the last helper update, or removing a newly created profile")
    parser.add_argument("--apply", action="store_true", help="Perform the displayed change; otherwise preview only")
    args = parser.parse_args(argv)
    try:
        root = (args.codex_home or Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))).expanduser().resolve()
        if args.restore:
            desired = None
            if args.model or args.reasoning_effort:
                raise SetupError("Do not combine --restore with model or reasoning options.")
        else:
            if not args.model:
                raise SetupError("Choose a Responses-capable model with --model.")
            desired = render_profile(args.profile, args.model, args.reasoning_effort)
            _, version = detect_codex(args.codex_bin)
            print(f"Codex {version}; separate profile files supported.")
        plan = prepare(root, args.profile, desired, args.restore)
        print(f"{'Apply' if args.apply else 'Preview'}: {plan.action} {plan.target}")
        if not args.restore:
            print(f"Provider: {args.profile}; model: {args.model}; endpoint: {BASE_URL}")
            print(f"Credential reference: {KEY_ENV} (value not read or stored).")
        if args.apply:
            apply(plan)
            print("Done. Base configuration, accounts and permission settings were not changed.")
        elif plan.action != "unchanged":
            print("Run the same command with --apply to write this change.")
        if not args.restore:
            print(f"Set CODEX_HOME to {root} when starting this profile.")
            print(f"Start explicitly with: codex --profile {args.profile}")
            print("Configuration setup is not a client-load or paid-request success check.")
        return 0
    except SetupError as error:
        print(f"Error: {error}", file=sys.stderr)
    except OSError:
        print("Error: file operation failed. Check access and any backup before retrying.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
