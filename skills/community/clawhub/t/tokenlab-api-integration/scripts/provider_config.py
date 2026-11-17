"""Lossless provider insertion and reversible file writes for OpenCode and Pi."""

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from setup_files import MAX_CONFIG_BYTES, SetupError, read_file, require_same, atomic_write, setup_lock


def check_provider(name: str) -> None:
    if not re.fullmatch(r"tokenlab(?:[-_][a-z0-9_-]{1,40})?", name):
        raise SetupError("Use tokenlab or a provider name such as tokenlab-personal.")


def check_model(name: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/\[\]-]{0,199}", name) or name.startswith("sk-"):
        raise SetupError("Choose an explicit public model ID, never an API key.")


def _unique_object(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError("Duplicate JSON keys")
        result[name] = value
    return result


def _invalid_constant(_):
    raise ValueError("Invalid constant")


DECODER = json.JSONDecoder(object_pairs_hook=_unique_object, parse_constant=_invalid_constant)


def parse(content: bytes, *, trailing_commas: bool = False, block_comments: bool = True) -> tuple[str, str, dict]:
    """Mask the client's supported comments/commas without changing character offsets."""
    try:
        text = content.decode("utf-8")
        clean = list(text)
        if clean and clean[0] == "\ufeff":
            clean[0] = " "
        index = 0
        commas = []
        while index < len(text):
            if text[index] == '"':
                _, index = DECODER.raw_decode(text, index)
                continue
            if text.startswith("//", index):
                end = text.find("\n", index)
                end = len(text) if end < 0 else end
            elif text.startswith("/*", index):
                if not block_comments:
                    raise ValueError("Unsupported block comment")
                end = text.find("*/", index + 2)
                if end < 0:
                    raise ValueError("Unclosed comment")
                end += 2
            else:
                if text[index] == ",":
                    commas.append(index)
                index += 1
                continue
            clean[index:end] = [char if char in "\r\n" else " " for char in text[index:end]]
            index = end
        if trailing_commas:
            for index in commas:
                next_index = index + 1
                while next_index < len(clean) and clean[next_index].isspace():
                    next_index += 1
                if next_index < len(clean) and clean[next_index] in "}]":
                    previous = index - 1
                    while previous >= 0 and clean[previous].isspace():
                        previous -= 1
                    if previous < 0 or clean[previous] in "{[,":
                        raise ValueError("Unexpected comma")
                    clean[index] = " "
        masked = "".join(clean)
        document = DECODER.decode(masked)
        if not isinstance(document, dict):
            raise ValueError("Expected object")
        return text, masked, document
    except (ValueError, UnicodeDecodeError, RecursionError):
        raise SetupError("Configuration is not a supported JSON object; no existing values were printed.") from None


def _members(masked: str, start: int):
    index = start + 1
    while True:
        while masked[index].isspace() or masked[index] == ",":
            index += 1
        if masked[index] == "}":
            return
        name, index = DECODER.raw_decode(masked, index)
        while masked[index].isspace() or masked[index] == ":":
            index += 1
        start_value = index
        _, index = DECODER.raw_decode(masked, index)
        yield name, start_value


def insert_provider(content: bytes | None, container: str, name: str, provider: dict,
                    *, trailing_commas: bool = False, block_comments: bool = True) -> bytes:
    text, masked, document = parse(content if content is not None else b"{}\n", trailing_commas=trailing_commas,
                                   block_comments=block_comments)
    start = masked.index("{")
    if container in document:
        if not isinstance(document[container], dict):
            raise SetupError("Existing provider configuration has an unsupported shape.")
        if name in document[container]:
            raise SetupError("That provider already exists outside this helper. Choose another provider name.")
        start = next(offset for key, offset in _members(masked, start) if key == container)
        existing = document[container]
        addition = {name: provider}
    else:
        existing = document
        addition = {container: {name: provider}}
    newline = "\r\n" if "\r\n" in text else "\n"
    inserted = json.dumps(addition, ensure_ascii=False, indent=2)[1:-1].replace("\n", newline)
    end = DECODER.raw_decode(masked, start)[1] - 1
    # Append so clients that pick the first available model retain provider order.
    # Keep comments/spacing intact; add a separator only when one is absent.
    if existing:
        last_value = list(_members(masked, start))[-1][1]
        last_end = DECODER.raw_decode(masked, last_value)[1]
        tail = re.sub(r"//[^\r\n]*|/\*[\s\S]*?\*/", "", text[last_end:end])
        prefix = text[:last_end] + ("" if "," in tail else ",") + text[last_end:end]
    else:
        prefix = text[:end]
    result = (prefix + inserted + text[end:]).encode("utf-8")
    parse(result, trailing_commas=trailing_commas, block_comments=block_comments)
    return result


def _digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _managed(content: bytes, client: str, name: str, comment: str = "//") -> bytes:
    # OpenCode normalizes a BOM by rewriting its config at load time. Emit its
    # managed layer without a BOM so ownership survives loading; backup is exact.
    if client == "OpenCode":
        content = content.removeprefix(b"\xef\xbb\xbf")
    bom = b"\xef\xbb\xbf" if content.startswith(b"\xef\xbb\xbf") else b""
    body = content[len(bom):]
    return bom + f"{comment} TokenLab {client} setup v1; provider={name}; sha256={_digest(content)}\n".encode() + body


def _require_managed(content: bytes | None, client: str, name: str, comment: str = "//") -> None:
    if content is None:
        raise SetupError("Configured file is missing; inspect the retained original backup before restoring.")
    raw = content.removeprefix(b"\xef\xbb\xbf")
    header, separator, body = raw.partition(b"\n")
    bom = b"\xef\xbb\xbf" if content.startswith(b"\xef\xbb\xbf") else b""
    expected = f"{comment} TokenLab {client} setup v1; provider={name}; sha256={_digest(bom + body)}".encode()
    if not separator or header != expected:
        raise SetupError("Configuration was edited after setup or belongs to another setup; it will not be overwritten.")


def reject_saved_credential(path: Path, name: str) -> bytes | None:
    content = read_file(path, allow_links=True)
    if content is not None:
        _, _, stored = parse(content)
        if name in stored:
            raise SetupError("A saved credential already uses that provider. Keep it and choose another provider name.")
    return content


def inspect_client(name: str, executable: str | None, minimum: tuple[int, int, int]) -> str:
    command = shutil.which(executable or name)
    if not command:
        raise SetupError(f"{name} was not found. Install the official client, then retry.")
    environment = {key: os.environ[key] for key in
                   ("PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "COMSPEC", "PATHEXT") if key in os.environ}
    with tempfile.TemporaryDirectory(prefix=f"tokenlab-{name}-detect-") as directory:
        environment.update(HOME=directory, USERPROFILE=directory, APPDATA=directory, LOCALAPPDATA=directory,
                           XDG_CONFIG_HOME=directory, XDG_DATA_HOME=directory, XDG_CACHE_HOME=directory,
                           XDG_STATE_HOME=directory, PI_CODING_AGENT_DIR=directory,
                           PI_OFFLINE="1", OPENCODE_DISABLE_AUTOUPDATE="true", OPENCODE_DISABLE_MODELS_FETCH="true")
        try:
            result = subprocess.run([str(Path(command).absolute()), "--version"], cwd=directory,
                                    env=environment, capture_output=True, text=True, timeout=15, check=True)
        except (OSError, subprocess.SubprocessError):
            raise SetupError(f"Could not inspect {name}; no client output or credentials were printed.") from None
    pattern = (r"\bHermes Agent v(\d+)\.(\d+)\.(\d+)\b" if name == "hermes" else
               r"\b(\d+)\.(\d+)\.(\d+)\b")
    match = re.search(pattern, result.stdout)
    if not match or tuple(map(int, match.groups())) < minimum:
        raise SetupError(f"This helper requires {name} {'.'.join(map(str, minimum))} or newer.")
    return ".".join(match.groups())


@dataclass(frozen=True)
class Plan:
    target: Path
    backup_path: Path
    name: str
    before: bytes | None
    backup_before: bytes | None
    after: bytes | None
    backup_after: bytes | None
    guards: dict[Path, bytes | None]

    @property
    def action(self) -> str:
        if self.before == self.after and self.backup_before == self.backup_after:
            return "unchanged"
        return "restore" if self.backup_after is None else "configure"


def prepare(target: Path, client: str, container: str, name: str, provider: dict | None,
            *, restore: bool = False, trailing_commas: bool = False, block_comments: bool = True,
            guards: dict[Path, bytes | None] | None = None, insert=None, comment: str = "//") -> Plan:
    check_provider(name)
    backup_path = target.with_name(f".{target.name}.{name}.tokenlab-backup")
    before, backup = read_file(target), read_file(backup_path)
    original = before
    if backup is not None:
        header, separator, body = backup.partition(b"\n")
        prefix = f"TokenLab {client} original v1; provider={name}; missing=".encode()
        original = None if header.startswith(prefix + b"1;") else body
        expected = prefix + (b"1" if original is None else b"0") + f"; sha256={_digest(body)}".encode()
        if not separator or header != expected or (original is None and body):
            raise SetupError("Original backup is invalid; no configuration was changed.")
        # Also recovers a write interrupted after backup creation or after restoration.
        if before != original:
            _require_managed(before, client, name, comment)
    elif before is not None and before.removeprefix(b"\xef\xbb\xbf").startswith(f"{comment} TokenLab ".encode()):
        raise SetupError("A managed configuration has no matching original backup; inspect it before proceeding.")
    if restore:
        after = original
        next_backup = None
    else:
        if provider is None:
            raise SetupError("--model is required when configuring a provider.")
        inserted = (insert(original, container, name, provider) if insert is not None else
                    insert_provider(original, container, name, provider, trailing_commas=trailing_commas,
                                    block_comments=block_comments))
        after = _managed(inserted, client, name, comment)
        body = original if original is not None else b""
        next_backup = (f"TokenLab {client} original v1; provider={name}; missing={int(original is None)}; sha256={_digest(body)}\n".encode() + body)
        if max(len(after), len(next_backup)) > MAX_CONFIG_BYTES:
            raise SetupError("Configuration plus its backup metadata exceeds the supported file size.")
    return Plan(target, backup_path, name, before, backup, after, next_backup, guards or {})


def apply(plan: Plan) -> None:
    if plan.action == "unchanged":
        return
    plan.target.parent.mkdir(parents=True, exist_ok=True)
    with setup_lock(plan.target.parent, plan.target.name):
        require_same(plan.target, plan.before)
        require_same(plan.backup_path, plan.backup_before)
        for path, content in plan.guards.items():
            require_same(path, content, allow_links=True)
        if plan.backup_after != plan.backup_before and plan.backup_after is not None:
            atomic_write(plan.backup_path, plan.backup_after, plan.backup_before)
        if plan.after != plan.before:
            if plan.after is None:
                plan.target.unlink()
            else:
                atomic_write(plan.target, plan.after, plan.before)
        if plan.backup_after is None and plan.backup_before is not None:
            require_same(plan.backup_path, plan.backup_before)
            plan.backup_path.unlink()
