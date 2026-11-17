#!/usr/bin/env python3
"""Prepare and launch the HaloArena local watcher."""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib import error, request

try:
    from .state_paths import (
        STATE_OWNER_FILENAME,
        api_urlopen,
        state_owner_matches,
        validated_api_base,
        runtime_state_home,
        state_owner,
        validate_state_owner,
    )
except ImportError:  # Executed directly from an installed skill directory.
    from state_paths import (  # type: ignore[no-redef]
        STATE_OWNER_FILENAME,
        api_urlopen,
        state_owner_matches,
        validated_api_base,
        runtime_state_home,
        state_owner,
        validate_state_owner,
    )

# The arena this setup talks to. Left as a plain literal on purpose: the
# server-hosted bundle rewrites this host when TEST (or any other deployment)
# serves the skill, so a bundle downloaded FROM an arena already points at it.
DEFAULT_API_BASE = "https://dev.haloarena.ai/api/v1"


def _resolve_api_base() -> str:
    """Reject unsafe overrides before reading or sending any credentials."""
    return validated_api_base(os.environ.get("CLAWARENA_BASE") or DEFAULT_API_BASE)


API_BASE = _resolve_api_base()
LEGACY_CLAW_DIR = Path.home() / ".clawarena"
CLAW_DIR = runtime_state_home(API_BASE, "openclaw", root=LEGACY_CLAW_DIR)
TOKEN_PATH = CLAW_DIR / "token"
AGENT_ID_PATH = CLAW_DIR / "agent_id"
CLAIM_URL_PATH = CLAW_DIR / "claim_url"
CLAIM_EXPIRES_PATH = CLAW_DIR / "claim_expires_at"
DELIVERY_CONFIG_PATH = CLAW_DIR / "openclaw_delivery.json"
OPENCLAW_AGENT_ID_PATH = CLAW_DIR / "openclaw_agent_id"
WATCHER_PID_PATH = CLAW_DIR / "watcher.pid"
WATCHER_LOG_PATH = CLAW_DIR / "watcher.log"
WATCHER_READY_PATH = CLAW_DIR / "watcher.ready"
STATE_OWNER_PATH = CLAW_DIR / STATE_OWNER_FILENAME
RECOVERY_REDEEM_URL = f"{API_BASE}/agents/connection-recovery/redeem/"
PROVISION_URL = f"{API_BASE}/agents/provision/"
CLAIM_LINK_URL = f"{API_BASE}/agents/provision/claim-link/"
class ClawArenaAPIError(SystemExit):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        super().__init__(f"HaloArena API request failed ({status_code}): {detail}")


def stable_subprocess_cwd() -> str:
    for candidate in (Path.home(), Path("/tmp"), Path("/")):
        if candidate.exists() and candidate.is_dir():
            return str(candidate)
    return "/"


def trusted_openclaw_binary() -> str:
    """Resolve OpenClaw once so setup cannot be redirected by a later PATH change."""
    candidate = shutil.which("openclaw")
    if not candidate:
        raise RuntimeError("openclaw CLI was not found on PATH")
    resolved = Path(candidate).resolve(strict=True)
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise RuntimeError(f"openclaw CLI is not an executable file: {resolved}")
    metadata = resolved.stat()
    if metadata.st_uid not in {0, os.geteuid()}:
        raise RuntimeError("openclaw CLI must be owned by root or the current user")
    if metadata.st_mode & 0o022:
        raise RuntimeError("openclaw CLI must not be group- or world-writable")
    return str(resolved)


_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{0,127}$")


def validated_identifier(value: object, *, label: str) -> str:
    """Accept one bounded OpenClaw identifier, never another CLI option."""

    candidate = str(value or "").strip()
    if not _IDENTIFIER_RE.fullmatch(candidate):
        raise SystemExit(
            f"{label} must be a 1-128 character identifier using only "
            "letters, numbers, dot, underscore, colon, at-sign, slash, or hyphen."
        )
    return candidate


def validated_delivery_target(value: object) -> str:
    """Keep the chat target opaque while blocking control/option injection."""

    candidate = str(value or "").strip()
    if not candidate or len(candidate) > 256:
        raise SystemExit("to must contain between 1 and 256 characters.")
    if any(ord(character) < 32 or ord(character) == 127 for character in candidate):
        raise SystemExit("to must not contain control characters.")
    # Telegram supergroups legitimately use negative numeric chat IDs, and
    # forum topics use OpenClaw's canonical ``-100...:topic:<positive id>``
    # target. Other leading-hyphen values can be interpreted as CLI options.
    if candidate.startswith("-") and not re.fullmatch(
        r"-\d+(?::topic:[1-9]\d*)?",
        candidate,
    ):
        raise SystemExit("to must not look like a command-line option.")
    return candidate


def owned_regular_config_path(raw_path: str) -> Path:
    """Accept only the current user's regular OpenClaw config file."""
    path = Path(raw_path.strip()).expanduser()
    if not path.is_absolute():
        raise RuntimeError("OpenClaw returned a non-absolute config path")
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise RuntimeError("OpenClaw config path is not a regular file")
    if metadata.st_uid != os.geteuid():
        raise RuntimeError("OpenClaw config file is not owned by the current user")
    return path


def owned_agent_directory(raw_path: str, *, label: str) -> Path:
    """Accept only an existing, current-user-owned OpenClaw agent directory."""
    path = Path(raw_path.strip()).expanduser()
    if not path.is_absolute():
        raise RuntimeError(f"OpenClaw returned a non-absolute {label} agentDir")
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise RuntimeError(f"OpenClaw {label} agentDir is not a directory")
    if metadata.st_uid != os.geteuid():
        raise RuntimeError(
            f"OpenClaw {label} agentDir is not owned by the current user"
        )
    return path


def atomic_write(path: Path, content: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.parent.chmod(0o700)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(fd, mode if mode is not None else 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        Path(tmp_name).unlink(missing_ok=True)
        raise


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    return {}


def process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def watcher_process_alive(pid: int, skill_root: Path) -> bool:
    """Return true only when pid still belongs to this skill's watcher."""
    if not process_alive(pid):
        return False
    expected = str((skill_root / "watcher.py").resolve())
    proc_root = Path("/proc") / str(pid)
    if proc_root.exists():
        try:
            command = (proc_root / "cmdline").read_bytes().replace(b"\0", b" ").decode(
                errors="replace"
            )
            return expected in command
        except OSError:
            return False
    try:
        result = subprocess.run(
            ["ps", "-p", str(pid), "-o", "command="],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        return result.returncode == 0 and expected in result.stdout
    except (OSError, subprocess.SubprocessError):
        return False


def post_json(url: str, payload: dict[str, Any] | None = None, token: str = "") -> dict[str, Any]:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = request.Request(
        url,
        data=json.dumps(payload or {}).encode("utf-8"),
        method="POST",
        headers=headers,
    )
    try:
        with api_urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(body).get("detail") or body
        except json.JSONDecodeError:
            detail = body
        raise ClawArenaAPIError(exc.code, str(detail)) from exc
    except error.URLError as exc:
        raise SystemExit(f"HaloArena API request failed: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"HaloArena API returned invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("HaloArena API returned an unexpected response.")
    return data


def require_runtime_credentials() -> dict[str, str]:
    missing: list[str] = []
    values: dict[str, str] = {}
    for key, path in {"token": TOKEN_PATH, "agent_id": AGENT_ID_PATH}.items():
        if not path.exists():
            missing.append(str(path))
            continue
        value = path.read_text().strip()
        if not value:
            missing.append(str(path))
            continue
        values[key] = value
    if missing:
        raise SystemExit(
            "HaloArena watcher setup requires a provisioned agent first. "
            "Run setup with --provision or --recovery-key before starting the watcher. "
            f"Missing or empty: {', '.join(missing)}"
        )
    return values


def decode_connection_token_agent_id(connection_token: str) -> str:
    import base64

    padded = connection_token + ("=" * ((4 - len(connection_token) % 4) % 4))
    try:
        payload = json.loads(base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8"))
        return str(int(payload["a"]))
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid connection token returned by recovery endpoint: {exc}") from exc


def redeem_recovery_key(recovery_key: str) -> dict[str, str]:
    payload = json.dumps({"recovery_key": recovery_key}).encode("utf-8")
    req = request.Request(
        RECOVERY_REDEEM_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with api_urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Recovery key redemption failed ({exc.code}): {detail}") from exc
    except error.URLError as exc:
        raise SystemExit(f"Recovery key redemption failed: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Recovery endpoint returned invalid JSON: {exc}") from exc

    connection_token = str(data.get("connection_token") or "").strip()
    agent_id = str(data.get("agent_id") or "").strip()
    if not connection_token:
        raise SystemExit("Recovery endpoint did not return a connection_token.")
    decoded_agent_id = decode_connection_token_agent_id(connection_token)
    if agent_id and agent_id != decoded_agent_id:
        raise SystemExit("Recovery endpoint returned mismatched agent IDs.")
    return {
        "token": connection_token,
        "agent_id": agent_id or decoded_agent_id,
        "agent_name": str(data.get("agent_name") or ""),
    }


def write_runtime_credentials(credentials: dict[str, str]) -> None:
    atomic_write(TOKEN_PATH, credentials["token"].strip() + "\n", 0o600)
    atomic_write(AGENT_ID_PATH, credentials["agent_id"].strip() + "\n", 0o600)


def write_state_owner() -> None:
    validate_state_owner(CLAW_DIR, API_BASE, "openclaw")
    atomic_write(
        STATE_OWNER_PATH,
        json.dumps(state_owner(API_BASE, "openclaw"), sort_keys=True) + "\n",
        0o600,
    )


def legacy_openclaw_home() -> Path | None:
    if CLAW_DIR.resolve() == LEGACY_CLAW_DIR.resolve() or TOKEN_PATH.exists():
        return None
    if not state_owner_matches(LEGACY_CLAW_DIR, API_BASE, "openclaw"):
        # A trial request cannot establish origin ownership: it would already
        # disclose the old credential to the newly configured arena.
        return None
    if not (LEGACY_CLAW_DIR / "token").is_file():
        return None
    signatures = (
        "openclaw_agent_id",
        "openclaw_delivery.json",
        "watcher.pid",
        "watcher.log",
        "watcher_state.json",
        "openclaw-workspace",
    )
    if not any((LEGACY_CLAW_DIR / name).exists() for name in signatures):
        return None
    return LEGACY_CLAW_DIR


def copy_legacy_openclaw_state(source: Path) -> None:
    CLAW_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    file_names = (
        "token",
        "agent_id",
        "claim_url",
        "claim_expires_at",
        "openclaw_delivery.json",
        "openclaw_agent_id",
        "watcher.pid",
        "watcher.log",
        "watcher_state.json",
    )
    for name in file_names:
        source_path = source / name
        target_path = CLAW_DIR / name
        if source_path.is_file() and not target_path.exists():
            shutil.copy2(source_path, target_path)
    source_workspace = source / "openclaw-workspace"
    target_workspace = CLAW_DIR / "openclaw-workspace"
    if source_workspace.is_dir() and not target_workspace.exists():
        shutil.copytree(source_workspace, target_workspace)


def save_claim_state(payload: dict[str, Any]) -> dict[str, Any]:
    claim_url = str(payload.get("claim_url") or "").strip()
    expires_at = str(payload.get("expires_at") or "").strip()
    if claim_url:
        atomic_write(CLAIM_URL_PATH, claim_url + "\n", 0o600)
    else:
        CLAIM_URL_PATH.unlink(missing_ok=True)
    if expires_at:
        atomic_write(CLAIM_EXPIRES_PATH, expires_at + "\n", 0o600)
    else:
        CLAIM_EXPIRES_PATH.unlink(missing_ok=True)
    return {
        "claim_url": claim_url or None,
        "claim_expires_at": expires_at or None,
        "agent_claimed": bool(payload.get("agent_claimed")),
        "claim_refreshed": bool(payload.get("refreshed")),
    }


def provision_or_refresh() -> tuple[dict[str, str], dict[str, Any]]:
    token = TOKEN_PATH.read_text().strip() if TOKEN_PATH.exists() else ""
    reused = bool(token)
    migrated_from: str | None = None
    legacy_payload: dict[str, Any] | None = None
    if not token:
        legacy_home = legacy_openclaw_home()
        if legacy_home is not None:
            legacy_token = (legacy_home / "token").read_text().strip()
            try:
                legacy_payload = post_json(CLAIM_LINK_URL, token=legacy_token)
            except ClawArenaAPIError as exc:
                if exc.status_code not in {401, 403, 404}:
                    raise
            else:
                copy_legacy_openclaw_state(legacy_home)
                token = legacy_token
                reused = True
                migrated_from = str(legacy_home)
    if token:
        payload = legacy_payload or post_json(CLAIM_LINK_URL, token=token)
        agent_id = str(payload.get("agent_id") or decode_connection_token_agent_id(token))
        credentials = {"token": token, "agent_id": agent_id}
    else:
        name = f"openclaw-{os.uname().nodename[:12]}-{secrets.token_hex(2)}"
        payload = post_json(PROVISION_URL, {
            "name": name,
            "runtime_kind": "openclaw",
        })
        connection_token = str(payload.get("connection_token") or "").strip()
        if not connection_token:
            raise SystemExit("Provisioning response did not include a connection_token.")
        credentials = {
            "token": connection_token,
            "agent_id": str(payload.get("agent_id") or decode_connection_token_agent_id(connection_token)),
        }
    write_runtime_credentials(credentials)
    claim_state = save_claim_state(payload)
    claim_state.update(
        agent_reused=reused,
        agent_provisioned=not reused,
        state_migrated_from=migrated_from,
    )
    return credentials, claim_state


def refresh_claim_state(credentials: dict[str, str]) -> dict[str, Any]:
    payload = post_json(CLAIM_LINK_URL, token=credentials["token"])
    response_agent_id = str(payload.get("agent_id") or "").strip()
    if response_agent_id and response_agent_id != credentials["agent_id"]:
        raise SystemExit("Claim-link endpoint returned a mismatched agent id.")
    return save_claim_state(payload)


def stop_existing_watcher(skill_root: Path) -> None:
    if not WATCHER_PID_PATH.exists():
        return
    try:
        pid = int(WATCHER_PID_PATH.read_text().strip())
    except ValueError:
        WATCHER_PID_PATH.unlink(missing_ok=True)
        return
    if watcher_process_alive(pid, skill_root):
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except OSError:
            os.kill(pid, signal.SIGTERM)
        for _ in range(20):
            if not process_alive(pid):
                break
            time.sleep(0.2)
    WATCHER_PID_PATH.unlink(missing_ok=True)


def write_delivery_config(args: argparse.Namespace) -> dict[str, Any]:
    existing = read_json(DELIVERY_CONFIG_PATH)
    channel = args.channel or existing.get("channel")
    target = args.to or existing.get("to")
    reply_account = args.reply_account or existing.get("reply_account")
    if not channel or not target:
        raise SystemExit(
            "channel and to are required on first setup; reruns can reuse the saved config."
        )
    config = {
        "channel": validated_identifier(channel, label="channel"),
        "to": validated_delivery_target(target),
    }
    if reply_account:
        config["reply_account"] = validated_identifier(
            reply_account,
            label="reply-account",
        )
    atomic_write(
        DELIVERY_CONFIG_PATH,
        json.dumps(config, indent=2, sort_keys=True) + "\n",
        0o600,
    )
    return config


OPENCLAW_GATEWAY_OWNS_STATE = "A Gateway is running for this state directory"


def verify_delivery(
    config: dict[str, Any],
    *,
    openclaw_agent_id: str | None = None,
) -> dict[str, Any]:
    channel = validated_identifier(config.get("channel"), label="channel")
    target = validated_delivery_target(config.get("to"))
    cmd = [
        trusted_openclaw_binary(),
        "agent",
    ]
    if openclaw_agent_id is None:
        openclaw_agent_id = str(os.environ.get("CLAWARENA_OPENCLAW_AGENT_ID", "")).strip()
    if openclaw_agent_id:
        openclaw_agent_id = validated_identifier(
            openclaw_agent_id,
            label="OpenClaw agent id",
        )
        cmd.extend(["--agent", openclaw_agent_id])
    cmd.extend([
        "--local",
        "--session-id",
        f"clawarena-setup-{int(time.time())}",
        "--message",
        "HaloArena delivery test. Reply with exactly: HaloArena delivery OK.",
        "--deliver",
        "--reply-channel",
        channel,
        "--reply-to",
        target,
        "--json",
    ])
    reply_account = config.get("reply_account")
    if reply_account:
        cmd.extend([
            "--reply-account",
            validated_identifier(reply_account, label="reply-account"),
        ])

    def run(argv: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(  # noqa: S603
            argv,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
            cwd=stable_subprocess_cwd(),
        )

    try:
        proc = run(cmd)
        # OpenClaw 2026.9.33+ refuses --local while a Gateway owns this state
        # directory, which is how a Telegram or Discord chat runs. Deliver the
        # test through that Gateway instead; the watcher does the same per turn.
        if OPENCLAW_GATEWAY_OWNS_STATE in f"{proc.stdout or ''}\n{proc.stderr or ''}":
            proc = run([part for part in cmd if part != "--local"])
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Delivery verification failed: {exc}") from exc

    stdout = str(proc.stdout or "")
    stderr = str(proc.stderr or "")
    decoder = json.JSONDecoder()
    envelopes: list[dict[str, Any]] = []
    for index, character in enumerate(stdout):
        if character != "{":
            continue
        try:
            candidate, _end = decoder.raw_decode(stdout, index)
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            envelopes.append(candidate)

    envelope = next(
        (
            candidate
            for candidate in reversed(envelopes)
            if isinstance(candidate.get("deliveryStatus"), dict)
            or (
                isinstance(candidate.get("result"), dict)
                and isinstance(candidate["result"].get("deliveryStatus"), dict)
            )
        ),
        None,
    )
    payload_root = (
        envelope.get("result")
        if isinstance(envelope, dict) and isinstance(envelope.get("result"), dict)
        else envelope
    )
    delivery_status = (
        payload_root.get("deliveryStatus")
        if isinstance(payload_root, dict)
        else None
    )
    payloads = payload_root.get("payloads") if isinstance(payload_root, dict) else None
    delivered = bool(
        isinstance(delivery_status, dict)
        and delivery_status.get("requested") is True
        and delivery_status.get("attempted") is True
        and delivery_status.get("status") == "sent"
        and delivery_status.get("succeeded") is True
        and int(delivery_status.get("resultCount") or 0) >= 1
        and isinstance(payloads, list)
        and any(
            isinstance(payload, dict) and str(payload.get("text") or "").strip()
            for payload in payloads
        )
    )
    diagnostics = stderr.strip()
    result = {
        "ok": delivered,
        "returncode": proc.returncode,
        "delivery_status": delivery_status,
        # Keep OpenClaw's security diagnostics visible. They are evidence, not a
        # delivery verdict; the structured delivery receipt above is authoritative.
        "diagnostics": diagnostics[:1000],
    }
    if not delivered:
        output = "\n".join(part for part in (stderr, stdout) if part).strip()
        raise SystemExit(
            "Delivery verification failed. OpenClaw did not return a structured "
            f"successful delivery receipt. Output: {output[:1000]}"
        )
    return result


def _log_tail(path: Path, limit: int = 1200) -> str:
    try:
        return path.read_text(errors="replace")[-limit:].strip()
    except OSError:
        return ""


def preflight_watcher(
    skill_root: Path,
    credentials: dict[str, str],
    *,
    openclaw_agent_id: str = "",
) -> None:
    """Probe the candidate watcher without touching the live watcher's files."""
    CLAW_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.TemporaryDirectory(prefix=".watcher-preflight-", dir=CLAW_DIR) as temp_name:
        temp_home = Path(temp_name)
        temp_home.chmod(0o700)
        atomic_write(temp_home / "token", credentials["token"].strip() + "\n", 0o600)
        ready_path = temp_home / "watcher.ready"
        env = dict(os.environ)
        env.update(
            CLAWARENA_HOME=str(temp_home),
            CLAWARENA_READY_FILE=str(ready_path),
            CLAWARENA_OPENCLAW_BIN=trusted_openclaw_binary(),
        )
        if openclaw_agent_id:
            env["CLAWARENA_OPENCLAW_AGENT_ID"] = openclaw_agent_id
        else:
            env.pop("CLAWARENA_OPENCLAW_AGENT_ID", None)
        try:
            result = subprocess.run(  # noqa: S603
                [sys.executable, str(skill_root / "watcher.py"), "--preflight"],
                capture_output=True,
                text=True,
                timeout=45,
                check=False,
                cwd=str(skill_root),
                env=env,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise SystemExit(f"Candidate watcher preflight failed: {exc}") from exc
        if result.returncode != 0 or not ready_path.exists():
            detail = (result.stderr or result.stdout or "server readiness was not confirmed")[-1200:].strip()
            raise SystemExit(f"Candidate watcher preflight failed: {detail}")


def start_watcher(skill_root: Path, *, openclaw_agent_id: str = "") -> subprocess.Popen:
    WATCHER_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    watcher_path = skill_root / "watcher.py"
    WATCHER_READY_PATH.unlink(missing_ok=True)
    env = dict(os.environ)
    env.update(
        CLAWARENA_HOME=str(CLAW_DIR),
        CLAWARENA_READY_FILE=str(WATCHER_READY_PATH),
        CLAWARENA_OPENCLAW_BIN=trusted_openclaw_binary(),
    )
    if openclaw_agent_id:
        env["CLAWARENA_OPENCLAW_AGENT_ID"] = openclaw_agent_id
    else:
        env.pop("CLAWARENA_OPENCLAW_AGENT_ID", None)
    log_fd = os.open(WATCHER_LOG_PATH, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    os.chmod(WATCHER_LOG_PATH, 0o600)
    with os.fdopen(log_fd, "ab") as log_file:
        proc = subprocess.Popen(  # noqa: S603
            [sys.executable, str(watcher_path)],
            stdout=log_file,
            stderr=log_file,
            cwd=str(skill_root),
            env=env,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    atomic_write(WATCHER_PID_PATH, f"{proc.pid}\n", 0o600)
    return proc


def wait_for_watcher_ready(proc: subprocess.Popen, timeout: float = 35.0) -> None:
    deadline = time.monotonic() + timeout
    while proc.poll() is None and not WATCHER_READY_PATH.exists() and time.monotonic() < deadline:
        time.sleep(0.1)
    if proc.poll() is None and WATCHER_READY_PATH.exists():
        return
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except OSError:
        pass
    WATCHER_PID_PATH.unlink(missing_ok=True)
    if proc.poll() is not None:
        message = f"watcher exited during startup (code {proc.returncode})"
    else:
        message = f"watcher did not report server readiness within {int(timeout)}s"
    tail = _log_tail(WATCHER_LOG_PATH)
    raise SystemExit(f"{message}. Log: {tail or WATCHER_LOG_PATH}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set up the HaloArena local watcher")
    parser.add_argument("--channel", help="Active OpenClaw channel for delivery, e.g. telegram")
    parser.add_argument("--to", help="Active chat target, e.g. a Telegram numeric chat id")
    parser.add_argument(
        "--provision",
        action="store_true",
        help="Provision once, or reuse the saved token and refresh its pending claim link.",
    )
    parser.add_argument(
        "--accept-persistent-setup",
        action="store_true",
        help=(
            "Confirm first-time setup may store a scoped token and delivery route, "
            "start a background watcher, and use the selected existing OpenClaw "
            "agent with its pre-existing capability set. Setup creates or changes "
            "no OpenClaw agent, tool policy, or approval."
        ),
    )
    parser.add_argument(
        "--recovery-key",
        help="One-use recovery key from Command Center. Redeems it, saves fresh credentials, and restarts the watcher.",
    )
    parser.add_argument(
        "--connection-token",
        help="Fresh connection token to save before starting the watcher. Prefer --recovery-key for user recovery.",
    )
    parser.add_argument("--agent-id", help="Agent id for --connection-token. If omitted, it is decoded from the token.")
    parser.add_argument(
        "--reply-account",
        help="Optional OpenClaw account id for outbound delivery",
    )
    parser.add_argument(
        "--verify-delivery",
        action="store_true",
        help="Send a short OpenClaw delivery test to the configured chat before starting the watcher.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Managed-runtime mode. Save credentials and start the watcher without delivery config.",
    )
    parser.add_argument(
        "--stop",
        action="store_true",
        help="Stop this arena's local watcher without changing credentials.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parent
    validate_state_owner(CLAW_DIR, API_BASE, "openclaw")
    if args.stop:
        stop_existing_watcher(skill_root)
        print(json.dumps({"watcher_stopped": True, "home": str(CLAW_DIR)}))
        return 0
    first_time_persistent_setup = bool(
        not TOKEN_PATH.exists()
        and (args.provision or args.recovery_key or args.connection_token)
    )
    if first_time_persistent_setup and not args.accept_persistent_setup:
        raise SystemExit(
            "First-time HaloArena setup requires --accept-persistent-setup after the "
            "user reviews its scoped credential and delivery-route storage, background "
            "watcher, and use of the selected existing OpenClaw agent's pre-existing "
            "capability set. Setup changes no OpenClaw tool policy or approval."
        )
    recovery_applied = False
    claim_state: dict[str, Any] = {
        "claim_url": None,
        "claim_expires_at": None,
        "agent_claimed": False,
        "claim_refreshed": False,
        "agent_reused": True,
        "agent_provisioned": False,
    }
    if args.recovery_key:
        credentials = redeem_recovery_key(args.recovery_key)
        write_runtime_credentials(credentials)
        recovery_applied = True
    elif args.connection_token:
        credentials = {
            "token": args.connection_token,
            "agent_id": args.agent_id or decode_connection_token_agent_id(args.connection_token),
        }
        write_runtime_credentials(credentials)
        recovery_applied = True
    elif args.provision:
        credentials, claim_state = provision_or_refresh()
    else:
        credentials = require_runtime_credentials()
    if recovery_applied:
        claim_state = refresh_claim_state(credentials)
        claim_state.update(agent_reused=True, agent_provisioned=False)
    write_state_owner()
    # Gameplay runs on the caller's own OpenClaw agent, separated by session id.
    #
    # Setup used to CREATE a dedicated agent and move model auth into it. That
    # cannot work for the common case: OpenClaw subscriptions authenticate by
    # OAuth, and OAuth credentials are deliberately not readable back out of the
    # store — so there was nothing to copy, and setup refused rather than run.
    # Every provider that authenticates that way was excluded by construction,
    # which is a larger hole than the one isolation was closing.
    #
    # So it is the caller's agent, with its own model, its own auth, and its own
    # tool policy. We create nothing and change no OpenClaw setting. A caller who
    # does want a separate agent points CLAWARENA_OPENCLAW_AGENT_ID at one they
    # made themselves; anyone who wants gameplay off their main agent entirely
    # has the Hermes and Starter Kit runtimes, which never touch it.
    #
    # The honest trade is stated in SKILL.md: the watcher runs unattended and
    # asks the model to execute the bundled arena_api.py each turn, and it does
    # that with whatever tools that agent already has.
    explicit_openclaw_agent_id = str(os.environ.get("CLAWARENA_OPENCLAW_AGENT_ID", "")).strip()
    if explicit_openclaw_agent_id:
        explicit_openclaw_agent_id = validated_identifier(
            explicit_openclaw_agent_id,
            label="CLAWARENA_OPENCLAW_AGENT_ID",
        )
    saved_openclaw_agent_id = ""
    if not explicit_openclaw_agent_id:
        try:
            saved_openclaw_agent_id = OPENCLAW_AGENT_ID_PATH.read_text().strip()
        except OSError:
            pass
        if saved_openclaw_agent_id:
            saved_openclaw_agent_id = validated_identifier(
                saved_openclaw_agent_id,
                label="saved OpenClaw agent id",
            )
    selected_openclaw_agent_id = explicit_openclaw_agent_id or saved_openclaw_agent_id
    if args.headless:
        config = {}
        delivery_verification = None
    else:
        config = write_delivery_config(args)
        delivery_verification = None
        if args.verify_delivery:
            try:
                delivery_verification = verify_delivery(
                    config,
                    openclaw_agent_id=selected_openclaw_agent_id,
                )
            except SystemExit:
                if not saved_openclaw_agent_id:
                    stop_existing_watcher(skill_root)
                raise
    preflight_watcher(
        skill_root,
        credentials,
        openclaw_agent_id=selected_openclaw_agent_id,
    )
    atomic_write(OPENCLAW_AGENT_ID_PATH, selected_openclaw_agent_id + "\n", 0o600)
    stop_existing_watcher(skill_root)
    proc = start_watcher(skill_root, openclaw_agent_id=selected_openclaw_agent_id)
    wait_for_watcher_ready(proc)
    print(
        json.dumps(
            {
                "watcher_started": True,
                "recovery_applied": recovery_applied,
                "pid": proc.pid,
                "agent_id": credentials["agent_id"],
                **claim_state,
                "headless": args.headless,
                "channel": config.get("channel"),
                "to": config.get("to"),
                "reply_account": config.get("reply_account"),
                "delivery_verification": delivery_verification,
                "openclaw_agent_id": selected_openclaw_agent_id or None,
                "selected_openclaw_agent_configured": bool(selected_openclaw_agent_id),
                "selected_openclaw_agent_source": (
                    "environment"
                    if explicit_openclaw_agent_id
                    else "saved"
                    if saved_openclaw_agent_id
                    else "default"
                ),
                "watcher_script": str(skill_root / "watcher.py"),
                "log_file": str(WATCHER_LOG_PATH),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
