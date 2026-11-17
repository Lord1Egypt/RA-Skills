"""Destination writers. Secret bytes stay in memory or stdin pipes."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

from secret_drop.dotenv_file import (
    default_openclaw_env_path,
    upsert_env_file,
    validate_name,
    write_secret_file,
)
from secret_drop.errors import SecretDropError


def _openclaw_binary() -> str:
    binary = shutil.which("openclaw")
    if not binary:
        raise SecretDropError("The openclaw CLI is required for the selected destination.")
    return binary


def _run_openclaw(
    argv: list[str],
    *,
    input_bytes: bytes | None = None,
    timeout: int = 45,
) -> None:
    binary = _openclaw_binary()
    try:
        result = subprocess.run(
            [binary, *argv],
            input=input_bytes,
            stdin=subprocess.DEVNULL if input_bytes is None else None,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise SecretDropError("OpenClaw CLI operation timed out.") from exc
    if result.returncode != 0:
        raise SecretDropError("OpenClaw CLI operation failed.")


def write_openclaw_env(name: str, secret: str) -> dict[str, Any]:
    result = upsert_env_file(default_openclaw_env_path(), name, secret)
    return {
        "destination": "openclaw-env",
        "name": name,
        "restart_required": True,
        **result,
    }


def write_dotenv(path: str, name: str, secret: str) -> dict[str, Any]:
    result = upsert_env_file(Path(path), name, secret)
    return {"destination": "dotenv", "name": name, "restart_required": False, **result}


def write_file(path: str, secret: str, *, replace: bool) -> dict[str, Any]:
    result = write_secret_file(Path(path), secret, replace=replace)
    return {"destination": "file", "restart_required": False, **result}


def restart_openclaw_gateway(*, safe: bool = True) -> bool:
    argv = ["gateway", "restart"]
    if safe:
        argv.append("--safe")
    # --safe can wait up to five minutes before forcing the restart.
    _run_openclaw(argv, timeout=330)
    return True


def write_openclaw_store(
    name: str,
    secret: str,
    *,
    kind: str,
    allowed_hosts: list[str],
    config_path: str | None,
    reload_runtime: bool,
) -> dict[str, Any]:
    validate_name(name)
    if kind not in {"secret", "env"}:
        raise SecretDropError("Store kind must be 'secret' or 'env'.")
    argv = ["secrets", "store", "set", name, "--kind", kind, "--value-file", "-"]
    for host in allowed_hosts:
        argv.extend(["--allow-host", host])
    _run_openclaw(argv, input_bytes=secret.encode("utf-8"))
    if config_path:
        _run_openclaw(
            [
                "config",
                "set",
                config_path,
                "--ref-provider",
                "default",
                "--ref-source",
                "store",
                "--ref-id",
                name,
            ]
        )
    if reload_runtime:
        _run_openclaw(["secrets", "reload", "--expect-final"])
    return {
        "destination": "openclaw-store",
        "name": name,
        "kind": kind,
        "config_bound": bool(config_path),
        "runtime_reloaded": reload_runtime,
        "restart_required": False,
    }


def write_secret(
    *,
    destination: str,
    secret: str,
    name: str | None = None,
    path: str | None = None,
    store_kind: str = "secret",
    allowed_hosts: list[str] | None = None,
    config_path: str | None = None,
    reload_runtime: bool = False,
    replace: bool = False,
) -> dict[str, Any]:
    if "\x00" in secret:
        raise SecretDropError("Secret contains a NUL byte and cannot be stored as text.")
    if destination == "openclaw-env":
        if not name:
            raise SecretDropError("--name is required for openclaw-env.")
        return write_openclaw_env(validate_name(name), secret)
    if destination == "dotenv":
        if not name or not path:
            raise SecretDropError("--name and --path are required for dotenv.")
        return write_dotenv(path, validate_name(name), secret)
    if destination == "file":
        if not path:
            raise SecretDropError("--path is required for file.")
        return write_file(path, secret, replace=replace)
    if destination == "openclaw-store":
        if not name:
            raise SecretDropError("--name is required for openclaw-store.")
        return write_openclaw_store(
            name,
            secret,
            kind=store_kind,
            allowed_hosts=allowed_hosts or [],
            config_path=config_path,
            reload_runtime=reload_runtime,
        )
    raise SecretDropError(f"Unsupported destination: {destination}")
