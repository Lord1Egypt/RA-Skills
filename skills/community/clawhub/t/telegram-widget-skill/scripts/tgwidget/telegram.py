"""A minimal Bot API client for sendWidget, editMessageWidgetData and editMessageCaption.

The bot token is read from the environment and goes into the request URL, as
the Bot API requires. It never appears in anything this module returns or
raises: HTTP libraries put the request URL into their error texts, so errors
here carry only Telegram's own `description` or the name of the network error.
"""

from __future__ import annotations

import json
import os
import socket
import urllib.error
import urllib.request
from typing import Any, Dict, Optional
from urllib.parse import urlsplit

TOKEN_ENV_VARS = ("TG_WIDGETS_BOT_TOKEN", "TELEGRAM_BOT_TOKEN")
API_BASE_ENV = "TG_WIDGETS_API_BASE"
DEFAULT_API_BASE = "https://api.telegram.org"
LOOPBACK_HOSTS = ("localhost", "127.0.0.1", "::1")


def check_api_base(base: str) -> str:
    """Return `base` without a trailing slash, or raise ValueError.

    The bot token is part of every request URL, so whoever runs the server at
    `base` gets the token. Only Telegram's own API and a Bot API server on this
    machine qualify: a command line that points the CLI anywhere else is refused.
    """
    parts = urlsplit(base.strip())
    host = (parts.hostname or "").lower()
    clean = parts.scheme in ("http", "https") and not (parts.username or parts.password or parts.query or parts.fragment)
    official = parts.scheme == "https" and host == "api.telegram.org" and parts.port in (None, 443)
    local = host in LOOPBACK_HOSTS or host.endswith(".localhost")
    if not (clean and (official or local)):
        raise ValueError("%s must be %s or a Bot API server on this machine (localhost): the bot token "
                         "is sent to it" % (API_BASE_ENV, DEFAULT_API_BASE))
    return base.strip().rstrip("/")


class TelegramError(Exception):
    def __init__(self, description: str, error_code: Optional[int] = None, retry_after: Optional[int] = None):
        super().__init__(description)
        self.description = description
        self.error_code = error_code
        self.retry_after = retry_after

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"description": self.description}
        if self.error_code is not None:
            d["error_code"] = self.error_code
        if self.retry_after is not None:
            d["retry_after"] = self.retry_after
        return d


def token_from_env() -> Optional[str]:
    for name in TOKEN_ENV_VARS:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return None


def redact(text: str, token: Optional[str]) -> str:
    if token and text:
        text = text.replace(token, "<redacted>")
        # the numeric bot id before the colon is not secret, the rest is
        secret = token.split(":", 1)[-1]
        if len(secret) >= 8:
            text = text.replace(secret, "<redacted>")
    return text


class BotApi:
    def __init__(self, token: str, test_env: bool = False, api_base: Optional[str] = None, timeout: float = 30):
        self._token = token
        self.test_env = test_env
        self.api_base = check_api_base(api_base or os.environ.get(API_BASE_ENV) or DEFAULT_API_BASE)
        self.timeout = timeout

    def __repr__(self) -> str:  # never show the token, even in a traceback's locals
        return "BotApi(api_base=%r, test_env=%r)" % (self.api_base, self.test_env)

    def call(self, method: str, payload: Dict[str, Any]) -> Any:
        url = "%s/bot%s/%s%s" % (self.api_base, self._token, "test/" if self.test_env else "", method)
        body = json.dumps({k: v for k, v in payload.items() if v is not None}).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as e:
            # Telegram answers errors with a JSON body; read it, drop the exception (its text has the URL)
            try:
                raw = e.read()
            except Exception:
                raw = b""
            if not raw:
                raise TelegramError("HTTP %d from the Bot API" % e.code, e.code) from None
        except urllib.error.URLError as e:
            reason = getattr(e, "reason", None)
            name = type(reason).__name__ if isinstance(reason, BaseException) else "URLError"
            raise TelegramError("network error (%s) calling %s" % (name, method)) from None
        except (socket.timeout, TimeoutError):
            raise TelegramError("timed out calling %s" % method) from None
        except Exception as e:  # anything else: name only, never str(e)
            raise TelegramError("%s calling %s" % (type(e).__name__, method)) from None
        try:
            obj = json.loads(raw.decode("utf-8"))
        except Exception:
            raise TelegramError("the Bot API returned something that is not JSON") from None
        if not obj.get("ok"):
            params = obj.get("parameters") or {}
            raise TelegramError(redact(str(obj.get("description") or "request failed"), self._token),
                                obj.get("error_code"), params.get("retry_after"))
        return obj.get("result")
