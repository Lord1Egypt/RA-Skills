#!/usr/bin/env python3
"""Preview, create and restore an explicit TokenLab launcher for Claude Code. Python 3.11+."""

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

from setup_files import SetupError, SafeParser, read_file, require_same, atomic_write, setup_lock


BASE_URL = "https://api.tokenlab.sh"
KEY_ENV = "TOKENLAB_API_KEY"
MARKER = "# TokenLab Claude Code setup v1"
MIN_VERSION = (2, 1, 263)
SCRIPT_DIR = Path(__file__).resolve().parent


def session_settings() -> dict:
    # No key goes into JSON or argv. Bearer auth avoids changing the user's
    # remembered choice between a subscription and an ANTHROPIC_API_KEY.
    return {
        "apiKeyHelper": "",
        "fallbackModel": [],
        "env": {
            "ANTHROPIC_BASE_URL": BASE_URL,
            "ANTHROPIC_API_KEY": "",
            "ANTHROPIC_CUSTOM_HEADERS": "",
            "CLAUDE_CODE_OAUTH_TOKEN": "",
            "CLAUDE_CODE_USE_BEDROCK": "0",
            "CLAUDE_CODE_USE_VERTEX": "0",
            "CLAUDE_CODE_USE_FOUNDRY": "0",
        },
    }


def detect_claude(executable: str | None = None) -> tuple[str, str]:
    command = shutil.which(executable or "claude")
    if not command:
        raise SetupError("Claude Code was not found. Install it from the official guide, then retry.")
    command = str(Path(command).absolute())
    with tempfile.TemporaryDirectory(prefix="tokenlab-claude-detect-") as directory:
        environment = {key: os.environ[key] for key in ("PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "COMSPEC", "PATHEXT") if key in os.environ}
        environment.update(HOME=directory, USERPROFILE=directory, CLAUDE_CONFIG_DIR=directory,
                           APPDATA=directory, LOCALAPPDATA=directory, TMPDIR=directory,
                           TMP=directory, TEMP=directory)
        try:
            version = subprocess.run([command, "--version"], env=environment, cwd=directory,
                                     capture_output=True, text=True, timeout=10, check=True)
            help_result = subprocess.run([command, "--help"], env=environment, cwd=directory,
                                         capture_output=True, text=True, timeout=10, check=True)
        except (OSError, subprocess.SubprocessError):
            raise SetupError("Could not inspect Claude Code. No client output or credentials were printed.") from None
    match = re.search(r"\b(\d+)\.(\d+)\.(\d+) \(Claude Code\)", version.stdout)
    if not match or tuple(map(int, match.groups())) < MIN_VERSION:
        raise SetupError("This helper requires Claude Code 2.1.263+; older authentication behavior is not supported.")
    if any(flag not in help_result.stdout for flag in ("--settings", "--model", "--print")):
        raise SetupError("Installed Claude Code does not advertise the required session options.")
    return command, ".".join(match.groups())


def check_name(name: str) -> None:
    if not re.fullmatch(r"tokenlab-claude(?:[-_][A-Za-z0-9_-]{1,48})?", name):
        raise SetupError("Use tokenlab-claude or a name such as tokenlab-claude-personal.")


def check_model(model: str) -> None:
    aliases = {"default", "best", "fable", "sonnet", "opus", "haiku", "opusplan"}
    if (not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}", model)
            or model.startswith("sk-") or model in aliases):
        raise SetupError("Choose an explicit public Messages model ID, not a key or a moving Claude alias.")


def reject_managed_setup(root: Path) -> None:
    if any(os.environ.get(key) for key in ("CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST", "CLAUDE_CODE_SETTINGS_JSON")):
        raise SetupError("A host manages this Claude configuration. Automatic TokenLab setup is not supported there.")
    system_root = (Path("/Library/Application Support/ClaudeCode") if sys.platform == "darwin"
                   else Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "ClaudeCode" if os.name == "nt"
                   else Path("/etc/claude-code"))
    paths = [system_root / "managed-settings.json", system_root / "managed-settings.d",
             root / "remote-settings.json"]
    if any(path.exists() or path.is_symlink() for path in paths):
        raise SetupError("Managed Claude settings are present. This personal-launcher helper will not override them.")
    if sys.platform == "darwin":
        result = subprocess.run(["/usr/bin/defaults", "read", "com.anthropic.claudecode"],
                                capture_output=True, timeout=10)
        if result.returncode == 0:
            raise SetupError("Claude has OS-managed preferences. This helper does not override that policy.")
        if result.returncode != 1 or b"does not exist" not in result.stderr:
            raise SetupError("Claude OS policy could not be inspected. No settings or account details were printed.")
    elif os.name == "nt":
        import winreg
        for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                with winreg.OpenKey(hive, r"SOFTWARE\Policies\ClaudeCode"):
                    raise SetupError("Claude has registry policy. This helper does not override that policy.")
            except FileNotFoundError:
                pass
    elif os.environ.get("WSL_DISTRO_NAME"):
        # WSL can inherit Windows policy. Do not pretend a Linux-only check covers it.
        raise SetupError("WSL policy inheritance has not been validated. Use the manual guide for now.")


def inspect_settings(root: Path, cwd: Path) -> dict[Path, bytes | None]:
    reject_managed_setup(root)
    paths = {root / "settings.json"}
    for directory in (cwd, *cwd.parents):
        paths.update(directory / ".claude" / name for name in ("settings.json", "settings.local.json"))
    snapshots = {}
    for path in sorted(paths):
        content = read_file(path, allow_links=True)
        snapshots[path] = content
        if content is None:
            continue
        try:
            settings = json.loads(content)
        except (ValueError, UnicodeDecodeError):
            raise SetupError("A Claude settings file is not valid JSON; its contents were not printed.") from None
        if not isinstance(settings, dict) or not isinstance(settings.get("env", {}), dict):
            raise SetupError("A Claude settings file has an unsupported shape.")
        # File env values override shell env. A static JSON value cannot safely
        # interpolate the launcher's dynamic TokenLab key.
        if any(key in settings.get("env", {}) for key in ("ANTHROPIC_AUTH_TOKEN", "CLAUDE_CONFIG_DIR", "CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST")):
            raise SetupError("A settings env block conflicts with session credentials or configuration location. Keep it unchanged and use a separately reviewed setup.")
        if settings.get("modelOverrides"):
            raise SetupError("Existing modelOverrides could remap the chosen model. Resolve that conflict explicitly first.")
        if any(settings.get(key) for key in ("forceLoginMethod", "forceLoginOrgUUID", "forceLoginGatewayUrl")):
            raise SetupError("Claude login policy is configured. This helper does not replace it.")
    return snapshots


def render_launcher(root: Path, name: str, model: str, executable: str) -> bytes:
    check_name(name)
    check_model(model)
    # Keep launch behavior at the installed Skill's canonical source; this small
    # entry point stores only paths and the explicitly selected model.
    body = ("from pathlib import Path\nimport sys\n"
            f"sys.path.insert(0, {str(SCRIPT_DIR)!r})\n"
            "from configure_claude import start_launcher\n"
            f"raise SystemExit(start_launcher(Path(__file__), Path({str(root)!r}), "
            f"{name!r}, {model!r}, {executable!r}))\n").encode()
    digest = hashlib.sha256(body).hexdigest()
    return f"{MARKER}; name={name}; sha256={digest}\n".encode() + body


def require_managed(content: bytes, name: str) -> None:
    header, separator, body = content.partition(b"\n")
    expected = f"{MARKER}; name={name}; sha256={hashlib.sha256(body).hexdigest()}".encode()
    if not separator or header != expected:
        raise SetupError("Launcher or backup belongs to another setup or was edited. It will not be overwritten.")


@dataclass(frozen=True)
class Plan:
    root: Path
    name: str
    action: str
    before: bytes | None
    backup: bytes | None
    after: bytes | None
    settings: dict[Path, bytes | None]

    @property
    def target(self) -> Path:
        return self.root / f"{self.name}.py"

    @property
    def backup_path(self) -> Path:
        return self.root / f".{self.name}.py.tokenlab-backup"


def prepare(root: Path, name: str, desired: bytes | None, restore: bool = False) -> Plan:
    check_name(name)
    before = read_file(root / f"{name}.py")
    backup = read_file(root / f".{name}.py.tokenlab-backup")
    for content in (before, backup):
        if content is not None:
            require_managed(content, name)
    if before is None and backup is not None:
        raise SetupError("Launcher is missing but a backup remains. Inspect it before making changes.")
    if restore:
        action = "restore" if backup is not None else "remove" if before is not None else "unchanged"
        return Plan(root, name, action, before, backup, backup, {})
    settings = inspect_settings(root, Path.cwd().resolve())
    if desired is None:
        raise SetupError("--model is required when configuring a launcher.")
    action = "unchanged" if before == desired else "create" if before is None else "update"
    return Plan(root, name, action, before, backup, desired, settings)


def apply(plan: Plan) -> None:
    if plan.action == "unchanged":
        return
    plan.root.mkdir(parents=True, exist_ok=True)
    with setup_lock(plan.root, plan.name):
        for path, content in plan.settings.items():
            require_same(path, content, allow_links=True)
        require_same(plan.target, plan.before)
        require_same(plan.backup_path, plan.backup)
        if plan.action == "update":
            atomic_write(plan.backup_path, plan.before, plan.backup)
        if plan.after is None:
            plan.target.unlink()
        else:
            atomic_write(plan.target, plan.after, plan.before)
        if plan.action == "restore":
            require_same(plan.backup_path, plan.backup)
            plan.backup_path.unlink()


def launch_environment(root: Path) -> dict[str, str]:
    key = os.environ.get(KEY_ENV)
    if not key or any(character.isspace() for character in key):
        raise SetupError("Set a complete TOKENLAB_API_KEY in your local launch environment; never pass it as an argument.")
    environment = os.environ.copy()
    environment.update(session_settings()["env"])
    environment["ANTHROPIC_AUTH_TOKEN"] = key
    environment["CLAUDE_CONFIG_DIR"] = str(root)
    return environment


def check_auth(command: list[str], environment: dict[str, str]) -> None:
    try:
        result = subprocess.run([*command, "auth", "status", "--json"], env=environment,
                                capture_output=True, text=True, timeout=15)
        status = json.loads(result.stdout)
    except (ValueError, subprocess.SubprocessError):
        raise SetupError("Claude authentication selection could not be checked; no account details were printed.") from None
    if (result.returncode != 0 or not isinstance(status, dict) or status.get("loggedIn") is not True
            or status.get("apiProvider") != "firstParty" or status.get("authMethod") != "oauth_token"
            or status.get("apiKeySource") not in (None, "none")):
        raise SetupError("Claude selected another authentication source or gateway. No model session was started.")


def start_launcher(path: Path, root: Path, name: str, model: str, executable: str) -> int:
    parser = SafeParser(description="Start Claude Code with this explicit TokenLab session.", allow_abbrev=False)
    parser.add_argument("--auth-status", action="store_true", help="Check local authentication selection without sending a model request")
    parser.add_argument("--print", dest="prompt", help="Run an explicit prompt; normal TokenLab usage charges apply")
    parser.add_argument("--output-format", choices=("text", "json", "stream-json"), default="text")
    parser.add_argument("--no-session-persistence", action="store_true", help="For --print only; passed to Claude Code")
    args = parser.parse_args()
    try:
        if (args.auth_status and args.prompt is not None) or (args.prompt is None and (args.output_format != "text" or args.no_session_persistence)):
            raise SetupError("Output options require --print; --auth-status cannot be combined with a prompt.")
        content = read_file(path)
        if content is None:
            raise SetupError("Launcher is missing.")
        require_managed(content, name)
        check_model(model)
        snapshots = inspect_settings(root, Path.cwd().resolve())
        command, _ = detect_claude(executable)
        environment = launch_environment(root)
        arguments = [command, "--settings", json.dumps(session_settings()), "--model", model]
        check_auth(arguments, environment)
        for settings_path, value in snapshots.items():
            require_same(settings_path, value, allow_links=True)
        if args.auth_status:
            print("Claude selected the session Bearer credential; existing API keys/helpers are inactive.")
            print("This is local configuration selection, not verification of the key or a model request.")
            return 0
        if args.prompt is not None:
            arguments += ["--print", args.prompt, "--output-format", args.output_format]
            if args.output_format == "stream-json":
                arguments.append("--verbose")
            if args.no_session_persistence:
                arguments.append("--no-session-persistence")
        return subprocess.call(arguments, env=environment)
    except SetupError as error:
        print(f"Error: {error}", file=sys.stderr)
    except (OSError, subprocess.SubprocessError):
        print("Error: Claude could not be started; no credentials or account details were printed.", file=sys.stderr)
    except KeyboardInterrupt:
        return 130
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--claude-config-dir", type=Path, help="Existing Claude configuration directory; default CLAUDE_CONFIG_DIR or ~/.claude")
    parser.add_argument("--claude-bin", help="Installed Claude Code executable; never an installation command")
    parser.add_argument("--name", default="tokenlab-claude", help="Name of the explicit Python launcher")
    parser.add_argument("--model", help="Explicit public model ID with Messages support")
    parser.add_argument("--restore", action="store_true", help="Preview restoring the last update, or removing a newly created launcher")
    parser.add_argument("--apply", action="store_true", help="Write the displayed change; otherwise preview only")
    args = parser.parse_args(argv)
    try:
        root = (args.claude_config_dir or Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude")))).expanduser().resolve()
        if args.restore:
            if args.model:
                raise SetupError("Do not combine --restore and --model.")
            desired = None
        else:
            if not args.model:
                raise SetupError("Choose a Messages-capable model with --model.")
            check_model(args.model)
            executable, version = detect_claude(args.claude_bin)
            print(f"Claude Code {version}; session settings and model options supported.")
            desired = render_launcher(root, args.name, args.model, executable)
        plan = prepare(root, args.name, desired, args.restore)
        print(f"{'Apply' if args.apply else 'Preview'}: {plan.action} {plan.target}")
        if not args.restore:
            print(f"Model: {args.model}; Messages endpoint root: {BASE_URL}")
            print(f"Credential: {KEY_ENV} -> session ANTHROPIC_AUTH_TOKEN; value not read during setup.")
        if args.apply:
            apply(plan)
            print("Done. Existing settings, accounts and permission policies were not changed.")
        elif plan.action != "unchanged":
            print("Run the same command with --apply to write this change.")
        if not args.restore:
            print(f"Start explicitly with Python 3.11+: {plan.target}")
            print("The launcher needs this installed Skill directory. Configuration creation is not a paid-request check.")
        return 0
    except SetupError as error:
        print(f"Error: {error}", file=sys.stderr)
    except (OSError, subprocess.SubprocessError):
        print("Error: file or client inspection failed. Existing contents were not printed.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
