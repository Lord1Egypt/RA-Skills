"""LLM-based text-to-speech provider.

Concrete :class:`TTSProvider` that delegates speech synthesis to a large-
language-model TTS HTTP endpoint (e.g. OpenAI's ``audio/speech`` API).
Supports both single-text and batched-text requests — ``supports_batch``
is ``True`` and :meth:`synth_batch` issues one request with an array of
texts.

Design notes
------------

- ``supports_batch = True`` — the scheduler may feed multi-entry batches;
  when the upstream only supports one text at a time the batch method
  would naturally iterate, but we assume the vendor endpoint accepts a
  batch shape of ``{"inputs": [<text>, ...], "voice": <id>}``. Vendors
  that truly are single-shot can subclass and override
  :meth:`synth_batch`.
- ``payload_unit = "tokens"`` — LLM TTS is typically token-priced.
  ``size_of`` defaults to :func:`size_of_tokens` (``ceil(len / 2)``);
  subclasses with a real tokenizer can override.
- Response shape accepted by :meth:`synth` / :meth:`synth_batch`:
    - JSON: ``{"audio_base64": "<b64>", "duration_ms": N}``.
    - JSON list (batch): ``[{"audio_base64": "<b64>", "duration_ms": N}, ...]``.
    - Raw audio body: when the response ``Content-Type`` is audio/*, the
      body is treated as the raw audio bytes; ``duration_ms`` falls back
      to ``0`` if not advertised in a header.
- Error mapping (R12.6, R12.7, R12.12):
    - HTTP 429 or business rate-limit body → :class:`RateLimitError`
      carrying ``retry_after`` from the ``Retry-After`` header when
      present.
    - HTTP 413 / ``input_too_long`` / ``input is too long`` / ``maximum
      context length`` → :class:`PayloadTooLargeError`.
    - Timeouts, 5xx, malformed JSON, missing audio → :class:`TransientError`.

Requirements: R6.4, R7.3, R12.2, R12.6, R12.7, R12.12, R12.14.
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
from translation_dubbing_skill.scheduler.sizing import size_of_tokens

# Business error keywords indicating the request exceeded an input-size
# limit (context window, max input chars, etc.).
_PAYLOAD_TOO_LARGE_HINTS: tuple[str, ...] = (
    "context_length_exceeded",
    "context length exceeded",
    "maximum context length",
    "input is too long",
    "input_too_long",
    "input too long",
    "payload too large",
    "request entity too large",
)

_RATE_LIMIT_HINTS: tuple[str, ...] = (
    "rate_limit",
    "rate limit",
    "too many requests",
    "quota",
)

_DEFAULT_TIMEOUT_S: float = 60.0


@register(kind="tts", provider_type="llm")
class LLMTTSProvider:
    """TTS provider backed by an LLM ``audio/speech``-style endpoint.

    Instances are created by :class:`ProviderRegistry` via a zero-argument
    constructor, then configured via :meth:`initialize`. All HTTP work
    goes through a single :class:`httpx.AsyncClient` created on first
    request; callers are not expected to manage the client's lifecycle.

    Attributes:
        provider_type: Stable registry key ``"llm"``.
        supports_batch: ``True`` — one request may carry a text array.
        payload_unit: ``"tokens"`` — size estimates drive batching.
        endpoint: Synthesis endpoint URL (set by :meth:`initialize`).
        credential: Bearer token passed in ``Authorization`` (set by
            :meth:`initialize`).
        model_name: LLM TTS model identifier (set by :meth:`initialize`).
        default_voice: Fallback voice id when the caller does not
            supply one (set by :meth:`initialize`).
    """

    provider_type: ClassVar[str] = "llm"
    supports_batch: ClassVar[bool] = True
    payload_unit: ClassVar[Literal["chars", "tokens"]] = "tokens"

    def __init__(self) -> None:
        self.endpoint: str = ""
        self.credential: str = ""
        self.model_name: str = ""
        self.default_voice: str = ""
        self._timeout_s: float = _DEFAULT_TIMEOUT_S
        self._client: httpx.AsyncClient | None = None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def initialize(self, config: ProviderConfig) -> None:
        """Configure endpoint / credential / model / default voice.

        Reads ``config.endpoint``, ``config.credential``,
        ``config.extra["model_name"]`` and ``config.extra["default_voice"]``.
        An optional ``config.extra["timeout_s"]`` overrides the 60-second
        default HTTP timeout.

        Args:
            config: Validated provider configuration.

        Raises:
            ValueError: If ``endpoint``, ``credential`` or
                ``extra.model_name`` is missing/empty.
        """
        if not config.endpoint:
            raise ValueError("LLMTTSProvider requires a non-empty endpoint")
        if not config.credential:
            raise ValueError("LLMTTSProvider requires a non-empty credential")
        extra = config.extra or {}
        model_name = extra.get("model_name")
        if not model_name:
            raise ValueError(
                "LLMTTSProvider requires extra.model_name to be set"
            )
        self.endpoint = config.endpoint
        self.credential = config.credential
        self.model_name = str(model_name)
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
        """Return an approximate token count for ``text``.

        Delegates to :func:`size_of_tokens` — ``ceil(len / 2)``.
        """
        return size_of_tokens(text)

    # ------------------------------------------------------------------
    # HTTP client lifecycle
    # ------------------------------------------------------------------

    def _get_client(self) -> httpx.AsyncClient:
        """Lazily instantiate the shared :class:`httpx.AsyncClient`."""
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
        """Synthesize a single text as ``(audio_bytes, duration_ms)``.

        Args:
            text: Non-empty text to synthesize.
            voice_id: Provider-specific voice identifier.

        Returns:
            ``(audio_bytes, duration_ms)`` with a non-negative duration.

        Raises:
            RateLimitError / PayloadTooLargeError / TransientError per
            the module docstring.
        """
        payload = self._build_request_body(inputs=[text], voice_id=voice_id)
        response = await self._post(payload)
        items = self._extract_items(response, expected=1)
        return items[0]

    async def synth_batch(
        self,
        texts: list[str],
        voice_id: str,
    ) -> list[tuple[bytes, int]]:
        """Synthesize a batch of texts in one upstream request.

        Args:
            texts: Non-empty list of texts. Empty list returns ``[]``
                without making an HTTP call.
            voice_id: Provider-specific voice identifier.

        Returns:
            A list of ``(audio_bytes, duration_ms)`` aligned 1:1 with
            ``texts``.

        Raises:
            RateLimitError / PayloadTooLargeError / TransientError per
            the module docstring.
        """
        if not texts:
            return []
        payload = self._build_request_body(inputs=list(texts), voice_id=voice_id)
        response = await self._post(payload)
        return self._extract_items(response, expected=len(texts))

    # ------------------------------------------------------------------
    # Helpers — request
    # ------------------------------------------------------------------

    def _build_request_body(
        self,
        *,
        inputs: list[str],
        voice_id: str,
    ) -> dict[str, Any]:
        """Construct the synth endpoint request body.

        Uses the common ``{"model": ..., "inputs": [...], "voice": ...}``
        shape. Vendors with a different schema can subclass and override.
        """
        return {
            "model": self.model_name,
            "inputs": inputs,
            "voice": voice_id,
        }

    async def _post(self, payload: dict[str, Any]) -> httpx.Response:
        """POST the synthesis request and map HTTP errors to signals."""
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
                "LLM tts request timed out",
                context={"provider_type": self.provider_type},
            ) from exc
        except httpx.HTTPError as exc:
            raise TransientError(
                f"LLM tts HTTP error: {exc}",
                context={"provider_type": self.provider_type},
            ) from exc

        self._raise_for_status(response)
        return response

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
                "LLM tts upstream returned HTTP 429",
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
                "LLM tts upstream rejected request as too large",
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )
        if any(hint in lowered for hint in _RATE_LIMIT_HINTS):
            raise RateLimitError(
                "LLM tts upstream reported rate limiting",
                retry_after=_parse_retry_after(response),
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )
        raise TransientError(
            f"LLM tts upstream returned HTTP {status}",
            context={
                "provider_type": self.provider_type,
                "status_code": status,
            },
        )

    @staticmethod
    def _safe_body_text(response: httpx.Response) -> str:
        """Return the response body as text, swallowing decode errors."""
        try:
            return response.text or ""
        except Exception:  # pragma: no cover - defensive
            return ""

    def _extract_items(
        self,
        response: httpx.Response,
        *,
        expected: int,
    ) -> list[tuple[bytes, int]]:
        """Pull ``(audio_bytes, duration_ms)`` pairs from the response.

        Supports three shapes:
            1. JSON object ``{"audio_base64", "duration_ms"}`` — treated
               as a single-item list.
            2. JSON list of such objects.
            3. Raw audio body when the response ``Content-Type`` starts
               with ``audio/``; duration falls back to ``0`` or the
               ``X-Audio-Duration-Ms`` header when present. Only valid
               for ``expected == 1``.

        Args:
            response: The upstream HTTP response (already validated 2xx).
            expected: Exact number of items required. Any mismatch raises
                :class:`TransientError` so the scheduler retries.

        Returns:
            A list of ``(bytes, int)`` pairs.

        Raises:
            TransientError: On any parsing / size mismatch.
        """
        content_type = (
            response.headers.get("content-type", "") if response.headers else ""
        ).lower()

        # Shape 3: raw audio body.
        if expected == 1 and content_type.startswith("audio/"):
            audio = response.content or b""
            duration_ms = 0
            duration_header = (
                response.headers.get("X-Audio-Duration-Ms")
                if response.headers
                else None
            )
            if duration_header is not None:
                try:
                    duration_ms = max(0, int(float(str(duration_header).strip())))
                except (TypeError, ValueError):
                    duration_ms = 0
            return [(audio, duration_ms)]

        # Shapes 1 and 2: JSON.
        try:
            body = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            raise TransientError(
                "LLM tts response was not valid JSON",
                context={"provider_type": self.provider_type},
            ) from exc

        if isinstance(body, dict):
            items_raw: list[Any] = [body]
        elif isinstance(body, list):
            items_raw = list(body)
        else:
            raise TransientError(
                "LLM tts response was neither a JSON object nor array",
                context={"provider_type": self.provider_type},
            )

        if len(items_raw) != expected:
            raise TransientError(
                "LLM tts response item count mismatch",
                context={
                    "provider_type": self.provider_type,
                    "expected": expected,
                    "actual": len(items_raw),
                },
            )

        results: list[tuple[bytes, int]] = []
        for item in items_raw:
            results.append(self._parse_item(item))
        return results

    def _parse_item(self, item: Any) -> tuple[bytes, int]:
        """Parse one ``{"audio_base64", "duration_ms"}`` dict."""
        if not isinstance(item, dict):
            raise TransientError(
                "LLM tts item was not a JSON object",
                context={"provider_type": self.provider_type},
            )
        audio_b64 = item.get("audio_base64")
        if not isinstance(audio_b64, str) or not audio_b64:
            raise TransientError(
                "LLM tts item missing audio_base64",
                context={"provider_type": self.provider_type},
            )
        try:
            audio = base64.b64decode(audio_b64, validate=False)
        except (binascii.Error, ValueError) as exc:
            raise TransientError(
                "LLM tts item audio_base64 could not be decoded",
                context={"provider_type": self.provider_type},
            ) from exc
        duration_raw = item.get("duration_ms")
        if isinstance(duration_raw, bool) or not isinstance(
            duration_raw, (int, float)
        ):
            raise TransientError(
                "LLM tts item missing numeric duration_ms",
                context={"provider_type": self.provider_type},
            )
        duration_ms = int(duration_raw)
        if duration_ms < 0:
            raise TransientError(
                "LLM tts item reported negative duration_ms",
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


__all__ = ["LLMTTSProvider"]
