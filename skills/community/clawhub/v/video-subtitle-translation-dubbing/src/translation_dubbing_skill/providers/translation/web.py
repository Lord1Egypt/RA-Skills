"""Third-party web-API translation provider.

Concrete :class:`TranslationProvider` that targets a conventional REST
``/translate`` endpoint. The provider exposes both a single-entry
:meth:`translate` call (matching the common single-string REST shape) and
a batch wrapper :meth:`translate_batch` that iterates entries one by one —
most third-party translation APIs do not offer a batch endpoint, so the
wrapper preserves ordering without fanning out concurrently (the adaptive
scheduler handles concurrency).

Design notes
------------

- ``supports_batch = True`` at the class level so the scheduler can feed
  multi-entry batches; the batch method internally iterates entry-by-entry.
  This mirrors the "supports batch if the third-party API supports batch,
  otherwise falls back to single-entry mode" behaviour described in the
  task (R12.14). Subclasses that truly support a batch endpoint can
  override :meth:`translate_batch` to issue one request per batch.
- ``payload_unit = "chars"`` — character-denominated pricing is standard
  across Google/Azure/DeepL-style APIs. ``size_of`` delegates to
  :func:`size_of_chars`.
- Error mapping (R12.6, R12.7, R12.12):
    - HTTP 429 → :class:`RateLimitError` carrying ``Retry-After`` if set.
    - HTTP 413 / "text too long" / "query too long" business errors →
      :class:`PayloadTooLargeError`.
    - ``httpx.TimeoutException``, 5xx, malformed JSON → :class:`TransientError`.

Requirements: R5.4, R7.1, R7.2, R12.1, R12.12, R12.14.
"""

from __future__ import annotations

import json
from typing import Any, ClassVar, Literal

import httpx

from translation_dubbing_skill.models import ProviderConfig, SubtitleEntry
from translation_dubbing_skill.providers.registry import register
from translation_dubbing_skill.scheduler.signals import (
    PayloadTooLargeError,
    RateLimitError,
    TransientError,
)
from translation_dubbing_skill.scheduler.sizing import size_of_chars

# Business error keywords indicating request text exceeded the provider's
# per-call character limit.
_PAYLOAD_LIMIT_HINTS: tuple[str, ...] = (
    "text too long",
    "query too long",
    "input too long",
    "input_too_long",
    "string too long",
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


@register(kind="translation", provider_type="web")
class WebTranslationProvider:
    """Translation provider backed by a generic REST translate endpoint.

    The request shape follows the common pattern::

        POST {endpoint}
        Authorization: Bearer {credential}
        {"q": "<text>", "source": "<src>", "target": "<tgt>"}

    The response is expected to carry the translated string either at
    ``translatedText`` (Google-style), ``data.translations[0].translatedText``
    (Google v2-style), ``translation``, or ``text``. Providers that differ
    can subclass and override :meth:`_extract_translation`.

    Attributes:
        provider_type: Stable registry key ``"web"``.
        supports_batch: ``True`` — the batch wrapper iterates internally.
        payload_unit: ``"chars"``.
        endpoint: Translate endpoint URL.
        credential: Bearer token; also redacted in error logs.
        source_language / target_language: BCP-47 tags parsed from
            ``extra.language_pair`` (e.g. ``"en-zh"``).
    """

    provider_type: ClassVar[str] = "web"
    supports_batch: ClassVar[bool] = True
    payload_unit: ClassVar[Literal["chars", "tokens"]] = "chars"

    def __init__(self) -> None:
        self.endpoint: str = ""
        self.credential: str = ""
        self.source_language: str = "en"
        self.target_language: str = "zh"
        self._timeout_s: float = _DEFAULT_TIMEOUT_S
        self._client: httpx.AsyncClient | None = None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def initialize(self, config: ProviderConfig) -> None:
        """Configure endpoint / credential / language pair.

        Reads ``config.endpoint``, ``config.credential`` and
        ``config.extra["language_pair"]``. The language pair is expected
        in ``"<src>-<tgt>"`` form (e.g. ``"en-zh"``). When omitted the
        provider defaults to ``en → zh``.

        Args:
            config: Validated provider configuration.

        Raises:
            ValueError: If ``endpoint`` or ``credential`` is missing.
        """
        if not config.endpoint:
            raise ValueError("WebTranslationProvider requires a non-empty endpoint")
        if not config.credential:
            raise ValueError(
                "WebTranslationProvider requires a non-empty credential"
            )
        self.endpoint = config.endpoint
        self.credential = config.credential

        pair = (config.extra.get("language_pair") if config.extra else None) or "en-zh"
        src, _, tgt = str(pair).partition("-")
        if src and tgt:
            self.source_language = src
            self.target_language = tgt

        timeout_raw = config.extra.get("timeout_s") if config.extra else None
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
    # Translation
    # ------------------------------------------------------------------

    async def translate_batch(
        self,
        entries: list[SubtitleEntry],
        target_language: str = "zh-CN",
    ) -> list[SubtitleEntry]:
        """Translate ``entries`` by iterating one request per entry.

        Most third-party translate APIs are single-text; the batch method
        preserves ordering without concurrent fan-out. Providers whose
        API supports true batching should override this method. Empty or
        whitespace-only text is returned as an empty translation without
        making an HTTP call — the coordinator's fast path never routes
        empty entries here, but defensive behaviour keeps the contract.

        Args:
            entries: Subtitle entries to translate. May be empty.
            target_language: BCP-47 target language tag. Defaults to
                ``"zh-CN"``; the value configured via ``language_pair``
                takes precedence for the wire protocol.

        Returns:
            Translated entries aligned 1:1 with ``entries``.

        Raises:
            RateLimitError: On HTTP 429 or equivalent business error.
            PayloadTooLargeError: On HTTP 413 / text-size rejection.
            TransientError: On timeout, 5xx, or malformed response.
        """
        if not entries:
            return []

        out: list[SubtitleEntry] = []
        for entry in entries:
            if not entry.text or entry.text.strip() == "":
                out.append(
                    SubtitleEntry(
                        index=entry.index,
                        start_ms=entry.start_ms,
                        end_ms=entry.end_ms,
                        text="",
                    )
                )
                continue

            translated_text = await self._translate_one(entry.text)
            out.append(
                SubtitleEntry(
                    index=entry.index,
                    start_ms=entry.start_ms,
                    end_ms=entry.end_ms,
                    text=translated_text,
                )
            )
        return out

    async def translate(
        self,
        entries: list[SubtitleEntry],
        target_language: str = "zh-CN",
    ) -> list[SubtitleEntry]:
        """Compatibility alias; delegates to :meth:`translate_batch`."""
        return await self.translate_batch(entries, target_language)

    # ------------------------------------------------------------------
    # Helpers — single-entry request
    # ------------------------------------------------------------------

    async def _translate_one(self, text: str) -> str:
        """Issue a single-text translate request.

        Args:
            text: Non-empty source text.

        Returns:
            The translated string.

        Raises:
            RateLimitError / PayloadTooLargeError / TransientError as
            documented on :meth:`translate_batch`.
        """
        payload = {
            "q": text,
            "source": self.source_language,
            "target": self.target_language,
        }
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
                "Web translation request timed out",
                context={"provider_type": self.provider_type},
            ) from exc
        except httpx.HTTPError as exc:
            raise TransientError(
                f"Web translation HTTP error: {exc}",
                context={"provider_type": self.provider_type},
            ) from exc

        self._raise_for_status(response)

        try:
            body = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            raise TransientError(
                "Web translation response was not valid JSON",
                context={"provider_type": self.provider_type},
            ) from exc

        return self._extract_translation(body)

    # ------------------------------------------------------------------
    # Helpers — error + response parsing
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
                "Web translation upstream returned HTTP 429",
                retry_after=_parse_retry_after(response),
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )

        if status == 413 or any(hint in lowered for hint in _PAYLOAD_LIMIT_HINTS):
            raise PayloadTooLargeError(
                "Web translation upstream rejected request as too large",
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )

        if any(hint in lowered for hint in _RATE_LIMIT_HINTS):
            raise RateLimitError(
                "Web translation upstream reported rate limiting",
                retry_after=_parse_retry_after(response),
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )

        raise TransientError(
            f"Web translation upstream returned HTTP {status}",
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

    def _extract_translation(self, body: Any) -> str:
        """Pull the translated string out of the response body.

        Supports several common shapes:
            * ``{"translatedText": "..."}``
            * ``{"translation": "..."}``
            * ``{"text": "..."}``
            * ``{"data": {"translations": [{"translatedText": "..."}]}}``

        Args:
            body: Parsed JSON response body.

        Returns:
            The translated string.

        Raises:
            TransientError: If no known field contains a string value.
        """
        if isinstance(body, dict):
            for key in ("translatedText", "translation", "text"):
                value = body.get(key)
                if isinstance(value, str):
                    return value

            data = body.get("data")
            if isinstance(data, dict):
                translations = data.get("translations")
                if isinstance(translations, list) and translations:
                    first = translations[0]
                    if isinstance(first, dict):
                        value = first.get("translatedText")
                        if isinstance(value, str):
                            return value

        raise TransientError(
            "Web translation response did not contain a translated string",
            context={"provider_type": self.provider_type},
        )


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


__all__ = ["WebTranslationProvider"]
