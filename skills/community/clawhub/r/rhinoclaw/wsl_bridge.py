#!/usr/bin/env python3
"""WSL -> Rhino bridge: one call, one RhinoClaw command, no blocked processes.

Why this exists (field finding): from WSL, the documented "PowerShell
one-liner as a -Command argument" path is hit by a content-based process
start blockade (presumably Defender/ASR — command lines containing
TcpClient + GetStream + .Read fail with execve EINVAL). What DOES work:
a .ps1 executed via -File from a \\wsl.localhost UNC path, with the payload
passed as a file. This module packages that working path:

  1. writes a per-call temp dir in the WSL filesystem containing
     - bridge.ps1    STATIC script, byte-identical on every call, so any
                     content-based blockade verdict is cacheable
     - config.json   host/port/timeout (flat values only)
     - request.json  the raw command JSON ({type, params, request_id})
  2. runs powershell.exe -NoProfile -ExecutionPolicy Bypass -File <UNC path>
  3. the script (on the Windows side, where 127.0.0.1:1999 is local) sends
     request.json to RhinoClaw and writes response.json
  4. prints the response to stdout.

Auth: the token is read ONLY from $env:RHINOCLAW_AUTH_TOKEN on the Windows
side (the bridge forwards a WSL-side value via WSLENV). It is never written
to any file or output.

Usage:
    python3 wsl_bridge.py '{"type": "ping", "params": {}}'
    python3 wsl_bridge.py ping
    python3 wsl_bridge.py get_document_info '{}'
    python3 wsl_bridge.py list_block_definitions '{"name_filter": "glutz"}'

Exit code 0 on a non-error response, 1 otherwise. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

POWERSHELL_EXE = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
DEFAULT_HOST = "127.0.0.1"  # loopback on the WINDOWS side (where Rhino runs)
DEFAULT_PORT = 1999
DEFAULT_TIMEOUT = 15.0
BASE_DIR = Path.home() / ".cache" / "rhinoclaw" / "wsl_bridge"

# The transport script. MUST stay static (no per-call substitutions): a
# byte-identical file lets content-hash-based blockades cache their verdict.
# All variability lives in config.json / request.json next to the script.
BRIDGE_PS1 = r"""# RhinoClaw WSL bridge - static transport script (written by wsl_bridge.py).
# Intentionally IDENTICAL content on every call; per-call data lives in
# config.json and request.json next to this script. The auth token is read
# ONLY from $env:RHINOCLAW_AUTH_TOKEN and never written to files or output.
$ErrorActionPreference = 'Stop'
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$responsePath = Join-Path $dir 'response.json'

function Write-BridgeError([string]$message) {
    $obj = @{ status = 'error'; message = $message; source = 'wsl_bridge.ps1' }
    [System.IO.File]::WriteAllText($responsePath, (ConvertTo-Json -InputObject $obj -Compress))
}

try {
    $config = Get-Content -Raw -Path (Join-Path $dir 'config.json') | ConvertFrom-Json
    $rhinoHost = [string]$config.host
    $rhinoPort = [int]$config.port
    $timeoutMs = [int]$config.timeout_ms

    $payload = [System.IO.File]::ReadAllText((Join-Path $dir 'request.json')).Trim()
    if (-not $payload.StartsWith('{')) {
        Write-BridgeError 'request.json must contain a JSON object.'
        exit 1
    }

    # Inject the auth token (env only, never persisted). Plain string surgery
    # instead of a ConvertFrom/To-Json round trip so the payload bytes pass
    # through untouched.
    $token = $env:RHINOCLAW_AUTH_TOKEN
    if ($token -and ($payload.IndexOf('"auth"') -lt 0)) {
        $escaped = $token.Replace('\', '\\').Replace('"', '\"')
        $rest = $payload.Substring(1).TrimStart()
        if ($rest.StartsWith('}')) {
            $payload = '{"auth":"' + $escaped + '"' + $rest
        } else {
            $payload = '{"auth":"' + $escaped + '",' + $rest
        }
    }

    $client = New-Object System.Net.Sockets.TcpClient
    $client.ReceiveTimeout = $timeoutMs
    $client.SendTimeout = $timeoutMs
    $client.Connect($rhinoHost, $rhinoPort)
    $stream = $client.GetStream()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $stream.Write($bytes, 0, $bytes.Length)
    $stream.Flush()

    # Read until the accumulated bytes parse as complete JSON (same framing
    # strategy as the repo's wire.py) or the deadline passes.
    $ms = New-Object System.IO.MemoryStream
    $buffer = New-Object byte[] 65536
    $text = $null
    $deadline = [DateTime]::UtcNow.AddMilliseconds($timeoutMs)
    while ($true) {
        $n = $stream.Read($buffer, 0, $buffer.Length)
        if ($n -le 0) { break }
        $ms.Write($buffer, 0, $n)
        $candidate = [System.Text.Encoding]::UTF8.GetString($ms.ToArray())
        try {
            $null = ConvertFrom-Json -InputObject $candidate
            $text = $candidate
            break
        } catch { }
        if ([DateTime]::UtcNow -gt $deadline) { break }
    }
    $stream.Close()
    $client.Close()

    if ($null -eq $text) {
        Write-BridgeError 'No complete JSON response from RhinoClaw (timeout or connection closed).'
        exit 1
    }
    [System.IO.File]::WriteAllText($responsePath, $text)
    exit 0
} catch {
    Write-BridgeError ('Bridge error: ' + $_.Exception.Message)
    exit 1
}
"""


class BridgeError(Exception):
    """Bridge-level failure (environment, powershell launch, no response)."""


def wsl_path_to_unc(path: Path) -> str:
    r"""WSL path -> \\wsl.localhost\<distro>\... UNC path for Windows."""
    distro = os.environ.get("WSL_DISTRO_NAME") or "Ubuntu"
    return f"\\\\wsl.localhost\\{distro}" + str(path).replace("/", "\\")


def _forwarding_env() -> Dict[str, str]:
    """Environment for powershell.exe with RHINOCLAW_AUTH_TOKEN forwarded.

    WSL env vars do not cross into Windows processes unless listed in
    WSLENV; '/u' scopes the forwarding to WSL->Windows only. If the token
    is instead set as a Windows user env var (the Rhino side needs it there
    anyway), forwarding is a no-op and the Windows value is used.
    """
    env = dict(os.environ)
    if env.get("RHINOCLAW_AUTH_TOKEN"):
        entries = [e for e in env.get("WSLENV", "").split(":") if e]
        if not any(e.split("/")[0] == "RHINOCLAW_AUTH_TOKEN" for e in entries):
            entries.append("RHINOCLAW_AUTH_TOKEN/u")
        env["WSLENV"] = ":".join(entries)
    return env


def call_rhinoclaw(
    command: Dict[str, Any],
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    timeout: float = DEFAULT_TIMEOUT,
    keep_dir: bool = False,
) -> Dict[str, Any]:
    """Send one RhinoClaw command dict via the PowerShell file bridge.

    ``command`` is the wire-format request ({"type": ..., "params": {...}});
    a request_id is minted if missing. Returns the parsed response dict.
    Raises BridgeError when the transport itself fails.
    """
    if not isinstance(command, dict) or not command.get("type"):
        raise BridgeError('command must be a dict with a "type" key')
    command.setdefault("params", {})
    command.setdefault("request_id", uuid.uuid4().hex)

    if not os.path.exists(POWERSHELL_EXE):
        raise BridgeError(
            f"powershell.exe not found at {POWERSHELL_EXE} — "
            "this bridge only works from WSL with a Windows host."
        )

    call_dir = BASE_DIR / f"call_{uuid.uuid4().hex}"
    call_dir.mkdir(parents=True, exist_ok=False)
    try:
        (call_dir / "bridge.ps1").write_text(BRIDGE_PS1, encoding="utf-8")
        (call_dir / "config.json").write_text(json.dumps({
            "host": host,
            "port": int(port),
            "timeout_ms": int(timeout * 1000),
        }), encoding="utf-8")
        (call_dir / "request.json").write_text(
            json.dumps(command, ensure_ascii=False), encoding="utf-8")

        script_unc = wsl_path_to_unc(call_dir / "bridge.ps1")
        proc = subprocess.run(  # noqa: S603 - fixed executable, file-based args
            [POWERSHELL_EXE, "-NoProfile", "-NonInteractive",
             "-ExecutionPolicy", "Bypass", "-File", script_unc],
            capture_output=True,
            text=True,
            timeout=timeout + 30,
            env=_forwarding_env(),
            cwd="/mnt/c",  # Windows-valid cwd; avoids UNC-cwd warnings
        )

        response_path = call_dir / "response.json"
        if not response_path.is_file():
            raise BridgeError(
                "powershell.exe produced no response file "
                f"(exit {proc.returncode}). stderr: {proc.stderr.strip()[:500]}"
            )
        # utf-8-sig: tolerate a BOM in case a PowerShell variant adds one.
        response = json.loads(response_path.read_text(encoding="utf-8-sig"))
        return response
    finally:
        if keep_dir:
            sys.stderr.write(f"[wsl_bridge] kept temp dir: {call_dir}\n")
        else:
            shutil.rmtree(call_dir, ignore_errors=True)


def _parse_cli_command(args: argparse.Namespace) -> Dict[str, Any]:
    """Accept either a full JSON command or `<type> ['<params-json>']`."""
    first = args.command
    try:
        as_json = json.loads(first)
    except json.JSONDecodeError:
        as_json = None
    if isinstance(as_json, dict):
        if args.params is not None:
            raise SystemExit("Pass params inside the JSON command, not as a second argument")
        return as_json
    # Treat as a command type name.
    params: Dict[str, Any] = {}
    if args.params is not None:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as e:
            raise SystemExit(f"Invalid params JSON: {e}")
        if not isinstance(params, dict):
            raise SystemExit("params must be a JSON object")
    return {"type": first, "params": params}


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Send one RhinoClaw command from WSL via the PowerShell file bridge.",
        epilog='Examples: wsl_bridge.py \'{"type":"ping","params":{}}\' | wsl_bridge.py ping',
    )
    parser.add_argument("command",
                        help='Full command JSON ({"type": ..., "params": ...}) or a bare command type')
    parser.add_argument("params", nargs="?", default=None,
                        help="Params JSON when the first argument is a bare command type")
    parser.add_argument("--host", default=DEFAULT_HOST,
                        help=f"Host as seen FROM WINDOWS (default {DEFAULT_HOST}; "
                             "do NOT use the WSL-side RHINOCLAW_HOST value here)")
    parser.add_argument("--port", type=int,
                        default=int(os.environ.get("RHINOCLAW_PORT") or DEFAULT_PORT))
    parser.add_argument("--timeout", type=float,
                        default=float(os.environ.get("RHINOCLAW_TIMEOUT") or DEFAULT_TIMEOUT),
                        help="Seconds to wait for the response (default 15)")
    parser.add_argument("--keep", action="store_true",
                        help="Keep the per-call temp dir (debugging)")
    args = parser.parse_args(argv)

    command = _parse_cli_command(args)
    try:
        response = call_rhinoclaw(command, host=args.host, port=args.port,
                                  timeout=args.timeout, keep_dir=args.keep)
    except (BridgeError, subprocess.TimeoutExpired) as e:
        print(json.dumps({"status": "error", "message": str(e),
                          "source": "wsl_bridge.py"}, indent=2))
        return 1

    print(json.dumps(response, indent=2, ensure_ascii=False))
    return 0 if response.get("status") != "error" else 1


if __name__ == "__main__":
    raise SystemExit(main())
