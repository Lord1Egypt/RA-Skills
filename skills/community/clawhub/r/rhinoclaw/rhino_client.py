#!/usr/bin/env python3
"""
Direct TCP client for RhinoClaw plugin.
Bypasses the MCP server layer for direct raw-TCP integration.
"""

import socket
import json
import logging
import os
import sys
import time
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Optional

# Configure logging based on RHINOMCP_DEBUG env var
_log_level = logging.DEBUG if os.getenv("RHINOMCP_DEBUG") else logging.WARNING
logging.basicConfig(
    level=_log_level,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("rhinoclaw")

# Load config. config.json lives NEXT TO this file — both in the repo
# (scripts/rhinoclaw_client/config.json) and in the deployed skill, where
# sync-skill.sh copies the whole client dir into <skill>/scripts/. The old
# `parent.parent` path pointed one level too high and silently loaded nothing.
CONFIG_PATH = Path(__file__).parent / "config.json"

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}

CONFIG = load_config()
CONNECTION = CONFIG.get("connection", {})

# Defaults: env-vars (matches the standard MCP server's RHINOCLAW_* names)
# win over config.json values, which win over the historical hardcoded
# fallbacks. Lets the same shell that set RHINOCLAW_AUTH_TOKEN also override
# host/port/timeout without editing config.json.
def _env_or(default, env_name, cast=str):
    raw = os.environ.get(env_name)
    if raw is None or raw == "":
        return default
    try:
        return cast(raw)
    except (ValueError, TypeError):
        return default

DEFAULT_HOST = _env_or(CONNECTION.get("host", "172.31.96.1"), "RHINOCLAW_HOST")
DEFAULT_PORT = _env_or(CONNECTION.get("port", 1999), "RHINOCLAW_PORT", int)
DEFAULT_TIMEOUT = _env_or(CONNECTION.get("timeout", 15.0), "RHINOCLAW_TIMEOUT", float)
DEFAULT_RETRIES = CONNECTION.get("max_retries", 3)
DEFAULT_RETRY_DELAY = CONNECTION.get("retry_delay", 1.0)
# RHINOCLAW_AUTH_TOKEN — when set, every TCP command gets an "auth" field
# attached automatically. Empty / unset means "send commands without auth"
# (which works only if the plugin has no token configured either).
DEFAULT_AUTH_TOKEN = os.environ.get("RHINOCLAW_AUTH_TOKEN") or None


# The wire framing (command build/encode, chunked JSON read, id minting) is
# shared with the MCP server's RhinoConnection so neither transport re-rolls it
# (A3). Resolution order mirrors `_load_door_batch` in grasshopper.py: installed
# rhinoclaw package → flat module next to this file (deployed skill;
# sync-skill.sh copies wire.py) → repo-relative source path.
def _load_wire():
    try:
        from rhinoclaw.transport import wire
        return wire
    except ImportError:
        pass
    try:
        import wire
        return wire
    except ImportError:
        pass
    import importlib.util
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', '..', 'rhinoclaw_server', 'src', 'rhinoclaw', 'transport',
        'wire.py',
    )
    spec = importlib.util.spec_from_file_location('wire', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


wire = _load_wire()


# --- Custom Exceptions ---

class RhinoClawError(Exception):
    """Base exception for RhinoClaw."""
    pass

class RhinoConnectionError(RhinoClawError):
    """Could not connect to Rhino."""
    pass

class RhinoTimeoutError(RhinoClawError):
    """Operation timed out."""
    pass

class RhinoCommandError(RhinoClawError):
    """Rhino returned an error."""
    def __init__(self, message: str, command: str = None, details: dict = None):
        super().__init__(message)
        self.command = command
        self.details = details or {}

class ValidationError(RhinoClawError):
    """Invalid parameters."""
    pass


# --- Retry Decorator ---

def with_retry(max_retries: int = None, delay: float = None,
               exceptions: tuple = (RhinoConnectionError, RhinoTimeoutError)):
    """Decorator for automatic retry with exponential backoff."""
    _max = max_retries if max_retries is not None else DEFAULT_RETRIES
    _delay = delay if delay is not None else DEFAULT_RETRY_DELAY

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(_max):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    if attempt < _max - 1:
                        wait = _delay * (2 ** attempt)
                        logger.warning(f"Retry {attempt + 1}/{_max} after {wait:.1f}s: {e}")
                        time.sleep(wait)
            raise last_error
        return wrapper
    return decorator


__all__ = ['RhinoClient', 'get_client', 'RhinoClawError', 'RhinoConnectionError',
           'RhinoTimeoutError', 'RhinoCommandError', 'ValidationError', 'with_retry']


class RhinoClient:
    """TCP client for communicating with RhinoClaw plugin."""

    def __init__(self, host: str = None, port: int = None, timeout: float = None,
                 auth_token: Optional[str] = None):
        self.host = host or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self.timeout = timeout or DEFAULT_TIMEOUT
        # Explicit kwarg wins; otherwise pick up RHINOCLAW_AUTH_TOKEN once.
        # `None` means "don't attach an auth field" — the plugin will reject
        # iff it itself has a token configured.
        self.auth_token = auth_token if auth_token is not None else DEFAULT_AUTH_TOKEN
        self.sock: Optional[socket.socket] = None
    
    def connect(self) -> bool:
        """Connect to Rhino plugin.
        
        Returns:
            True on success.
        
        Raises:
            RhinoConnectionError: If connection fails.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            logger.debug(f"Connecting to {self.host}:{self.port}")
            self.sock.connect((self.host, self.port))
            return True
        except socket.timeout as e:
            logger.error(f"Connection timed out: {e}")
            self.sock = None
            raise RhinoConnectionError(f"Connection timed out to {self.host}:{self.port}: {e}") from e
        except (socket.error, ConnectionError, OSError) as e:
            logger.error(f"Connection failed: {e}")
            self.sock = None
            raise RhinoConnectionError(f"Could not connect to Rhino at {self.host}:{self.port}: {e}") from e
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.sock = None
            raise RhinoConnectionError(f"Connection failed: {e}") from e
    
    def disconnect(self):
        """Close the connection."""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None
    
    def send_command(self, cmd_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a command and receive the response.
        
        Raises:
            RhinoConnectionError: If not connected or connection lost.
            RhinoTimeoutError: If the operation times out.
            RhinoCommandError: If Rhino returns an error response.
        """
        if not self.sock:
            raise RhinoConnectionError("Not connected to Rhino")

        # Frame assembly + the chunked read loop live in `wire`, shared with the
        # MCP server's RhinoConnection (A3). Stateless TCP: the auth token rides
        # on every command so the plugin can verify each call without a session.
        # The CLI intentionally omits request_id/idempotency_key — only the
        # server needs the reconnect-retry dedup contract.
        command = wire.build_command(cmd_type, params, auth_token=self.auth_token)

        try:
            self.sock.sendall(wire.encode_command(command))

            # The connect-time socket timeout bounds this read.
            try:
                data = wire.read_json_frame(self.sock)
            except wire.IncompleteFrameError as e:
                raise RhinoTimeoutError(
                    f"No response received for '{cmd_type}': {e}"
                ) from e

            # read_json_frame only returns bytes that already parsed as JSON.
            result = json.loads(data.decode('utf-8'))
            if result.get('status') == 'error':
                raise RhinoCommandError(
                    result.get('message', 'Unknown error'),
                    command=cmd_type,
                    details=result
                )
            return result

        except socket.timeout as e:
            raise RhinoTimeoutError(f"Timeout waiting for response to '{cmd_type}': {e}") from e
        except (socket.error, ConnectionError, OSError) as e:
            raise RhinoConnectionError(f"Connection lost during '{cmd_type}': {e}") from e
        except (RhinoClawError,):
            raise  # Re-raise our own exceptions

    # ------------------------------------------------------------------
    #  High-level helpers — parity with the MCP server's tools so raw TCP
    #  can do the same things. Recipes live in the plugin (single source);
    #  preflight/hello are client-side (connection/auth) so they live here.
    # ------------------------------------------------------------------

    def hello(self) -> Dict[str, Any]:
        """Auth-free handshake — discover the server's state WITHOUT a token.

        Returns the plugin's hello payload (plugin_version, auth_required, mode,
        gh_available, blocked, blocked_until). Requires a plugin build
        that supports `hello` (0.5.0+); older plugins raise RhinoCommandError.
        """
        resp = self.send_command("hello")
        return resp.get("result", resp)

    def preflight(self) -> Dict[str, Any]:
        """RUN THIS FIRST. One call → connection/auth state + an exact next_action.

        Uses the auth-free `hello` handshake (never trips the brute-force block);
        falls back gracefully on plugins that predate it. `auth` ∈
        {ready, missing_client_token, token_mismatch, blocked, unknown}.
        Act only when `auth == "ready"`.
        """
        client_has_token = bool(self.auth_token)

        def verdict(connected, auth, next_action, **extra):
            d = {"connected": connected, "auth": auth, "next_action": next_action,
                 "host": self.host, "port": self.port}
            d.update({k: v for k, v in extra.items() if v is not None})
            return d

        try:
            h = self.hello()
        except RhinoCommandError as e:
            details = getattr(e, "details", None) or {}
            code = details.get("error_code", "")
            msg = str(e).lower()
            if code == "AUTH_REQUIRED" or "auth token missing or invalid" in msg:
                if not client_has_token:
                    return verdict(True, "missing_client_token",
                        "set RHINOCLAW_AUTH_TOKEN on the client (same value as the plugin) "
                        "and restart. Using the deployed skill? Re-sync: scripts/sync-skill.sh.",
                        hello_supported=False)
                return verdict(True, "token_mismatch",
                    "same RHINOCLAW_AUTH_TOKEN on both sides, then restart Rhino.",
                    hello_supported=False)
            if code == "AUTH_BLOCKED" or "blocked" in msg:
                return verdict(True, "blocked",
                    f"blocked until {details.get('blocked_until')} — wait, do NOT retry.",
                    hello_supported=False, blocked_until=details.get("blocked_until"))
            if "unknown command" in msg:
                return verdict(True, "ready",
                    "ready — this plugin predates `hello`; rebuild to enable the handshake.",
                    hello_supported=False)
            return verdict(True, "unknown", f"unexpected handshake error: {e}", hello_supported=False)
        except (RhinoConnectionError, RhinoTimeoutError) as e:
            return verdict(False, "unknown",
                f"plugin not reachable at {self.host}:{self.port}. Start Rhino + run "
                f"`tcpstart`; on WSL check RHINOCLAW_HOST.", detail=str(e))

        plugin = h.get("plugin_version")
        mode = h.get("mode")
        if h.get("blocked"):
            return verdict(True, "blocked",
                f"blocked until {h.get('blocked_until')} — wait, do NOT retry.",
                plugin_version=plugin, mode=mode, hello_supported=True,
                blocked_until=h.get("blocked_until"))
        auth_required = h.get("auth_required")
        if auth_required and not client_has_token:
            return verdict(True, "missing_client_token",
                "plugin requires a token; set RHINOCLAW_AUTH_TOKEN on the client and restart.",
                plugin_version=plugin, mode=mode, hello_supported=True)
        if auth_required and client_has_token:
            try:
                self.send_command("ping")
            except RhinoCommandError:
                return verdict(True, "token_mismatch",
                    "auth token mismatch — same RHINOCLAW_AUTH_TOKEN on both sides, restart Rhino.",
                    plugin_version=plugin, mode=mode, hello_supported=True)
        return verdict(True, "ready", "ready",
                       plugin_version=plugin, mode=mode, hello_supported=True)

    def build_and_bake_recipe(self, recipe: str, file_path: str = "",
                              params: Optional[Dict[str, Any]] = None,
                              layer: str = "GH_Bake",
                              material: Optional[str] = None) -> Dict[str, Any]:
        """Build + bake a native primitive recipe (box/sphere/cylinder/cone), or
        `recipe="list"` to list them. Same plugin command as the MCP tool —
        reached here over raw TCP. Requires a plugin build with the recipe command.
        """
        cmd: Dict[str, Any] = {"recipe": recipe}
        if recipe != "list":
            cmd["file_path"] = file_path
            cmd["layer"] = layer
            if params:
                cmd["params"] = params
            if material is not None:
                cmd["material"] = material
        resp = self.send_command("build_and_bake_recipe", cmd)
        return resp.get("result", resp)

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, *args):
        self.disconnect()


def get_client() -> RhinoClient:
    """Get a connected RhinoClient instance.
    
    Raises:
        RhinoConnectionError: If connection fails.
    """
    client = RhinoClient()
    client.connect()  # Raises RhinoConnectionError on failure
    return client


# CLI interface
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='RhinoClaw Client')
    parser.add_argument('command', help='Command: preflight, hello, ping, info, or raw command type')
    parser.add_argument('--params', '-p', type=str, help='JSON params', default='{}')
    parser.add_argument('--host', default=None, help=f'Host (default: {DEFAULT_HOST})')
    parser.add_argument('--port', type=int, default=None, help=f'Port (default: {DEFAULT_PORT})')
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON params: {e}")
        sys.exit(1)
    
    # `preflight` connects itself so a connection failure becomes a verdict,
    # not a traceback.
    if args.command == 'preflight':
        c = RhinoClient(args.host, args.port)
        try:
            c.connect()
        except RhinoClawError as e:
            print(json.dumps({
                "connected": False, "auth": "unknown",
                "next_action": f"plugin not reachable at {c.host}:{c.port}. Start Rhino + run "
                               f"`tcpstart`; on WSL check RHINOCLAW_HOST.",
                "detail": str(e),
            }, indent=2))
            sys.exit(0)
        try:
            print(json.dumps(c.preflight(), indent=2))
        finally:
            c.disconnect()
        sys.exit(0)

    # All commands use the same client with host/port from args or config
    with RhinoClient(args.host, args.port) as client:
        if args.command == 'ping':
            result = client.send_command("ping")
        elif args.command == 'hello':
            result = client.hello()
        elif args.command == 'info':
            result = client.send_command("get_document_info")
        else:
            result = client.send_command(args.command, params)

    print(json.dumps(result, indent=2))
