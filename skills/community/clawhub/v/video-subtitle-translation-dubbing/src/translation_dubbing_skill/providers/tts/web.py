"""Third-party web-API text-to-speech provider.

Concrete :class:`TTSProvider` that targets a conventional REST ``/tts``
endpoint. Most third-party TTS services expose a single-text endpoint
so this provider declares ``supports_batch = False`` and the adaptive
scheduler will clamp ``batch_size`` to ``1`` at runtime (R12.14).

Design notes
------------

- ``supports_batch = False`` — scheduler forces one text per request.
- ``payload_unit = "chars"`` — character-denominated pricing is standard.
- Response shape: ``{"audio_base64": "<b64>", "duration_ms": N}``, a raw
  audio body (when ``Content-Type`` starts with ``audio/``), or any JSON
  object with ``audio_base64`` + ``duration_ms``. Providers whose shape
  differs can subclass and override :meth:`_parse_response`.
- Error mapping mirrors the translation side (R12.6, R12.7, R12.12):
    - HTTP 429 → :class:`RateLimitError` (``retry_after`` honoured).
    - HTTP 413 / text-too-long / char-limit hints →
      :class:`PayloadTooLargeError`.
    - Timeouts, 5xx, malformed JSON, missing audio → :class:`TransientError`.

Requirements: R6.4, R7.3, R12.2, R12.12, R12.14.
"""

from __future__ import annotations

import base64
import binascii
import json
from typing import Any, ClassVar, Literal

import httpx

from translation_dubbing_skill.models import ProviderConfig
from translation_dubbing_skill.providers.registry import register
from translation_dubbing_skill.scheduler.signals import (
    PayloadTooLargeError,
    RateLimitError,
    TransientError,
)
from translation_dubbing_skill.scheduler.sizing import size_of_chars

_PAYLOAD_TOO_LARGE_HINTS: tuple[str, ...] = (
    "text too long",
    "input too long",
    "input_too_long",
    "string too long",
    "char limit",
    "character limit",
    "payload too large",
    "request entity too large",
)

_RATE_LIMIT_HINTS: tuple[str, ...] = (
    "rate_limit",
    "rate limit",
    "too many requests",
    "quota",
)

_DEFAULT_TIMEOUT_S: float = 30.0


@register(kind="tts", provider_type="web")
class WebTTSProvider:
    """TTS provider backed by a generic REST ``/tts`` endpoint.

    Request shape::

        POST {endpoint}
        Authorization: Bearer {credential}
        {"text": "<text>", "voice": "<voice_id>"}

    Attributes:
        provider_type: Stable registry key ``"web"``.
        supports_batch: ``False`` — single-shot endpoint.
        payload_unit: ``"chars"``.
        endpoint: Synthesis endpoint URL.
        credential: Bearer token; redacted in error logs.
        default_voice: Fallback voice id (set via ``extra.default_voice``).
    """

    provider_type: ClassVar[str] = "web"
    supports_batch: ClassVar[bool] = False
    payload_unit: ClassVar[Literal["chars", "tokens"]] = "chars"

    def __init__(self) -> None:
        self.endpoint: str = ""
        self.credential: str = ""
        self.default_voice: str = ""
        self._timeout_s: float = _DEFAULT_TIMEOUT_S
        self._client: httpx.AsyncClient | None = None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def initialize(self, config: ProviderConfig) -> None:
        """Configure endpoint / credential / default voice.

        Args:
            config: Validated provider configuration. Reads
                ``endpoint``, ``credential``, ``extra["default_voice"]``
                and optional ``extra["timeout_s"]``.

        Raises:
            ValueError: If ``endpoint`` or ``credential`` is missing.
        """
        if not config.endpoint:
            raise ValueError("WebTTSProvider requires a non-empty endpoint")
        if not config.credential:
            raise ValueError("WebTTSProvider requires a non-empty credential")
        extra = config.extra or {}
        self.endpoint = config.endpoint
        self.credential = config.credential
        default_voice = extra.get("default_voice")
        self.default_voice = str(default_voice) if default_voice else ""
        timeout_raw = extra.get("timeout_s")
        if timeout_raw is not None:
            try:
                self._timeout_s = float(timeout_raw)
            except (TypeError, ValueError):
                self._timeout_s = _DEFAULT_TIMEOUT_S

    # ------------------------------------------------------------------
    # Sizing
    # ------------------------------------------------------------------

    def size_of(self, text: str) -> int:
        """Return the character count of ``text``."""
        return size_of_chars(text)

    # ------------------------------------------------------------------
    # HTTP client lifecycle
    # ------------------------------------------------------------------

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout_s)
        return self._client

    async def aclose(self) -> None:
        """Release the underlying HTTP client, if any."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    # ------------------------------------------------------------------
    # Synthesis
    # ------------------------------------------------------------------

    async def synth(self, text: str, voice_id: str) -> tuple[bytes, int]:
        """Synthesize one text.

        Args:
            text: Non-empty source text.
            voice_id: Provider-specific voice identifier.

        Returns:
            ``(audio_bytes, duration_ms)`` with a non-negative duration.

        Raises:
            RateLimitError / PayloadTooLargeError / TransientError per
            the module docstring.
        """
        payload = {"text": text, "voice": voice_id}
        headers = {
            "Authorization": f"Bearer {self.credential}",
            "Content-Type": "application/json",
        }
        client = self._get_client()
        try:
            response = await client.post(
                self.endpoint, json=payload, headers=headers
            )
        except httpx.TimeoutException as exc:
            raise TransientError(
                "Web tts request timed out",
                context={"provider_type": self.provider_type},
            ) from exc
        except httpx.HTTPError as exc:
            raise TransientError(
                f"Web tts HTTP error: {exc}",
                context={"provider_type": self.provider_type},
            ) from exc

        self._raise_for_status(response)
        return self._parse_response(response)

    # ------------------------------------------------------------------
    # Helpers — response
    # ------------------------------------------------------------------

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Translate non-2xx HTTP statuses to scheduler signal exceptions."""
        status = response.status_code
        if 200 <= status < 300:
            return

        body_text = self._safe_body_text(response)
        lowered = body_text.lower()

        if status == 429:
            raise RateLimitError(
                "Web tts upstream returned HTTP 429",
                retry_after=_parse_retry_after(response),
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )
        if status == 413 or any(
            hint in lowered for hint in _PAYLOAD_TOO_LARGE_HINTS
        ):
            raise PayloadTooLargeError(
                "Web tts upstream rejected request as too large",
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )
        if any(hint in lowered for hint in _RATE_LIMIT_HINTS):
            raise RateLimitError(
                "Web tts upstream reported rate limiting",
                retry_after=_parse_retry_after(response),
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )
        raise TransientError(
            f"Web tts upstream returned HTTP {status}",
            context={
                "provider_type": self.provider_type,
                "status_code": status,
            },
        )

    @staticmethod
    def _safe_body_text(response: httpx.Response) -> str:
        try:
            return response.text or ""
        except Exception:  # pragma: no cover - defensive
            return ""

    def _parse_response(
        self, response: httpx.Response
    ) -> tuple[bytes, int]:
        """Extract ``(audio_bytes, duration_ms)`` from the 2xx response.

        Accepts a raw audio body (``Content-Type: audio/*``) or a JSON
        object with ``audio_base64`` + ``duration_ms``.
        """
        content_type = (
            response.headers.get("content-type", "") if response.headers else ""
        ).lower()

        if content_type.startswith("audio/"):
            audio = response.content or b""
            duration_ms = 0
            duration_header = (
                response.headers.get("X-Audio-Duration-Ms")
                if response.headers
                else None
            )
            if duration_header is not None:
                try:
                    duration_ms = max(
                        0, int(float(str(duration_header).strip()))
                    )
                except (TypeError, ValueError):
                    duration_ms = 0
            return audio, duration_ms

        try:
            body = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            raise TransientError(
                "Web tts response was not valid JSON",
                context={"provider_type": self.provider_type},
            ) from exc

        if not isinstance(body, dict):
            raise TransientError(
                "Web tts response was not a JSON object",
                context={"provider_type": self.provider_type},
            )

        audio_b64 = body.get("audio_base64")
        if not isinstance(audio_b64, str) or not audio_b64:
            raise TransientError(
                "Web tts response missing audio_base64",
                context={"provider_type": self.provider_type},
            )
        try:
            audio = base64.b64decode(audio_b64, validate=False)
        except (binascii.Error, ValueError) as exc:
            raise TransientError(
                "Web tts response audio_base64 could not be decoded",
                context={"provider_type": self.provider_type},
            ) from exc

        duration_raw: Any = body.get("duration_ms")
        if isinstance(duration_raw, bool) or not isinstance(
            duration_raw, (int, float)
        ):
            raise TransientError(
                "Web tts response missing numeric duration_ms",
                context={"provider_type": self.provider_type},
            )
        duration_ms = int(duration_raw)
        if duration_ms < 0:
            raise TransientError(
                "Web tts response reported negative duration_ms",
                context={
                    "provider_type": self.provider_type,
                    "duration_ms": duration_ms,
                },
            )
        return audio, duration_ms


def _parse_retry_after(response: httpx.Response) -> float | None:
    """Return the ``Retry-After`` header as seconds, or ``None``."""
    if response is None or response.headers is None:
        return None
    raw = response.headers.get("Retry-After")
    if raw is None:
        return None
    try:
        value = float(str(raw).strip())
    except (TypeError, ValueError):
        return None
    return value if value >= 0 else None


__all__ = ["WebTTSProvider"]
