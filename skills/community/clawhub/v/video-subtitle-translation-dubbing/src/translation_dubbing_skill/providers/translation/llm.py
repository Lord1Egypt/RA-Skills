"""LLM-based translation provider.

Concrete :class:`TranslationProvider` that delegates translation to a
large-language-model chat/completions HTTP endpoint. One HTTP request
carries a whole batch of subtitle entries as a JSON array; the model is
asked to return a same-length JSON array whose items pair ``id`` with the
simplified-Chinese ``translation``.

Design notes
------------

- ``supports_batch = True`` — a single request translates the whole batch
  (R12.1). The scheduler's ``batch_size`` therefore controls how many
  entries fan into one HTTP request.
- ``payload_unit = "tokens"`` — LLM pricing/limits are token-denominated.
  The ``size_of`` estimate uses a coarse ``ceil(len / 2)`` heuristic
  (see :func:`translation_dubbing_skill.scheduler.sizing.size_of_tokens`);
  subclasses with a real tokenizer may override it.
- Error mapping (R12.6, R12.7, R12.12):
    - HTTP 429 or business rate-limit body → :class:`RateLimitError`
      carrying ``retry_after`` from the ``Retry-After`` header when
      present.
    - HTTP 413 / ``context_length_exceeded`` / ``maximum context length``
      / ``input too long`` business errors → :class:`PayloadTooLargeError`
      so the scheduler shrinks ``payload_size`` and re-slices.
    - ``httpx.TimeoutException``, 5xx, malformed JSON, id/length
      mismatch → :class:`TransientError` so the scheduler retries with
      backoff.

Requirements: R5.4, R7.1, R7.2, R12.1, R12.6, R12.7, R12.12.
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
from translation_dubbing_skill.scheduler.sizing import size_of_tokens

# Business error keywords indicating the request exceeded the model's
# context window or input-size limit. Matched case-insensitively on the
# response body; kept conservative so unrelated 400s fall through to
# ``TransientError``.
_CONTEXT_OVERFLOW_HINTS: tuple[str, ...] = (
    "context_length_exceeded",
    "context length exceeded",
    "maximum context length",
    "input is too long",
    "input_too_long",
    "string too long",
    "payload too large",
    "request entity too large",
)

# Business error keywords indicating rate limiting via a non-429 status.
_RATE_LIMIT_HINTS: tuple[str, ...] = (
    "rate_limit",
    "rate limit",
    "too many requests",
    "quota",
)

_DEFAULT_TIMEOUT_S: float = 180.0


@register(kind="translation", provider_type="llm")
class LLMTranslationProvider:
    """Translation provider backed by a chat-completions LLM endpoint.

    Instances are created by :class:`ProviderRegistry` via a zero-argument
    constructor, then configured via :meth:`initialize`. All HTTP work
    goes through a single :class:`httpx.AsyncClient` created on first
    request; callers are not expected to manage the client's lifecycle.

    Attributes:
        provider_type: Stable registry key ``"llm"``.
        supports_batch: ``True`` — one request translates the whole batch.
        payload_unit: ``"tokens"`` — size estimates drive batching.
        endpoint: Chat endpoint URL (set by :meth:`initialize`).
        credential: Bearer token passed in ``Authorization`` (set by
            :meth:`initialize`).
        model_name: LLM model identifier (set by :meth:`initialize`).
    """

    provider_type: ClassVar[str] = "llm"
    supports_batch: ClassVar[bool] = True
    payload_unit: ClassVar[Literal["chars", "tokens"]] = "tokens"

    def __init__(self) -> None:
        self.endpoint: str = ""
        self.credential: str = ""
        self.model_name: str = ""
        self._timeout_s: float = _DEFAULT_TIMEOUT_S
        self._client: httpx.AsyncClient | None = None
        self._reasoning_split: Any = None
        self._request_body_overrides: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def initialize(self, config: ProviderConfig) -> None:
        """Configure endpoint/credential/model from the Manifest.

        Reads ``config.endpoint``, ``config.credential`` and
        ``config.extra["model_name"]``. Optional knobs in ``config.extra``:

        - ``timeout_s``: override the default 60-second HTTP timeout.
        - ``reasoning_split``: forwarded verbatim to the upstream as
          ``extra_body`` (MiniMax-compatible — when ``True`` the model
          puts its <think> content into a separate ``reasoning_details``
          field instead of embedding it in ``content``).
        - ``request_body_overrides``: free-form dict merged on top of the
          default request body. Useful for provider-specific extras
          (temperature, top_p, response_format, etc.) without having to
          subclass the provider.

        Args:
            config: Validated provider configuration.

        Raises:
            ValueError: If ``endpoint``, ``credential`` or
                ``extra.model_name`` is missing/empty.
        """
        if not config.endpoint:
            raise ValueError("LLMTranslationProvider requires a non-empty endpoint")
        if not config.credential:
            raise ValueError("LLMTranslationProvider requires a non-empty credential")
        model_name = config.extra.get("model_name") if config.extra else None
        if not model_name:
            raise ValueError(
                "LLMTranslationProvider requires extra.model_name to be set"
            )
        self.endpoint = config.endpoint
        self.credential = config.credential
        self.model_name = str(model_name)
        timeout_raw = config.extra.get("timeout_s") if config.extra else None
        if timeout_raw is not None:
            try:
                self._timeout_s = float(timeout_raw)
            except (TypeError, ValueError):
                self._timeout_s = _DEFAULT_TIMEOUT_S

        extra = config.extra or {}
        self._reasoning_split = extra.get("reasoning_split")
        overrides = extra.get("request_body_overrides")
        self._request_body_overrides = (
            dict(overrides) if isinstance(overrides, dict) else {}
        )

    # ------------------------------------------------------------------
    # Sizing
    # ------------------------------------------------------------------

    def size_of(self, text: str) -> int:
        """Return an approximate token count for ``text``.

        Delegates to :func:`size_of_tokens` — ``ceil(len / 2)`` — which is
        good enough for batching decisions. Providers with a real
        tokenizer can subclass and override.
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
    # Translation
    # ------------------------------------------------------------------

    async def translate_batch(
        self,
        entries: list[SubtitleEntry],
        target_language: str = "zh-CN",
        source_language: str = "en",
    ) -> list[SubtitleEntry]:
        """Translate ``entries`` in one LLM call.

        See module docstring for the full wire protocol. On success the
        returned list mirrors ``entries`` in order, ``index``,
        ``start_ms`` and ``end_ms``; only ``text`` is replaced with the
        model's ``translation`` for the matching ``id``.

        Args:
            entries: Subtitle entries to translate. May be empty (returns
                an empty list without making any HTTP call).
            target_language: BCP-47 target language tag. Default
                ``"zh-CN"``.
            source_language: BCP-47 source language tag. Default
                ``"en"``.

        Returns:
            Translated entries aligned 1:1 with ``entries``.

        Raises:
            RateLimitError: On HTTP 429 or equivalent business error.
            PayloadTooLargeError: On HTTP 413 / context-window overflow /
                LLM "input too long" business error.
            TransientError: On timeout, 5xx, JSON parse error, or
                id/length mismatch in the model's response.
        """
        if not entries:
            return []

        payload = self._build_request_body(entries, target_language, source_language)
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
                "LLM translation request timed out",
                context={"provider_type": self.provider_type},
            ) from exc
        except httpx.HTTPError as exc:
            raise TransientError(
                f"LLM translation HTTP error: {exc}",
                context={"provider_type": self.provider_type},
            ) from exc

        self._raise_for_status(response)

        try:
            body = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            raise TransientError(
                "LLM translation response was not valid JSON",
                context={"provider_type": self.provider_type},
            ) from exc

        items = self._extract_items(body)
        return self._merge_translations(entries, items)

    async def translate(
        self,
        entries: list[SubtitleEntry],
        target_language: str = "zh-CN",
        source_language: str = "en",
    ) -> list[SubtitleEntry]:
        """Compatibility alias; delegates to :meth:`translate_batch`."""
        return await self.translate_batch(entries, target_language, source_language)

    # ------------------------------------------------------------------
    # Helpers — request construction
    # ------------------------------------------------------------------

    def _build_request_body(
        self,
        entries: list[SubtitleEntry],
        target_language: str,
        source_language: str = "en",
    ) -> dict[str, Any]:
        """Construct the chat-completions request body.

        The user-role message instructs the model to translate each item
        in the JSON array and return a same-length JSON array pairing
        ``id`` with ``translation``. The prompt is intentionally
        hard-lined — no markdown fences, no commentary, no keys other
        than ``id`` / ``translation`` — so downstream parsers can rely
        on a stable shape even from models that like to chat.

        ``self._reasoning_split`` (when set) is forwarded as an
        ``extra_body`` field; MiniMax M2.x interprets this as "move
        <think> content out of ``content`` into ``reasoning_details``".
        Non-MiniMax providers ignore unknown top-level fields, so
        including it unconditionally is safe.

        ``self._request_body_overrides`` is merged last so callers can
        inject provider-specific knobs (``temperature``, ``top_p``,
        ``response_format`` etc.) without subclassing.
        """
        items = [{"id": entry.index, "text": entry.text} for entry in entries]
        system_prompt = (
            "You are a professional subtitle translator. "
            f"Translate every subtitle entry from source language '{source_language}' into "
            f"target language '{target_language}'. "
            "Preserve meaning, punctuation and tone. "
            "Output ONLY a raw JSON array matching the input order and length. "
            'Every element MUST be shaped as {"id": <input id>, "translation": '
            "<translated text>}. No commentary, no markdown fences, no "
            "<think> tags, no prose before or after the JSON."
        )
        user_prompt = (
            f"Translate this batch from {source_language} into {target_language} and return the JSON array:\n"
            f"{json.dumps(items, ensure_ascii=False)}"
        )
        body: dict[str, Any] = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        if self._reasoning_split is not None:
            # MiniMax M2.x: move <think> out of `content` into
            # `reasoning_details` for clean JSON parsing.
            body["reasoning_split"] = self._reasoning_split
        if self._request_body_overrides:
            body.update(self._request_body_overrides)
        return body

    # ------------------------------------------------------------------
    # Helpers — response parsing / error mapping
    # ------------------------------------------------------------------

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Translate non-2xx HTTP statuses to scheduler signal exceptions.

        Precedence:
            429 → :class:`RateLimitError` (with ``Retry-After`` if set).
            413 → :class:`PayloadTooLargeError`.
            Any 4xx body mentioning a context-overflow hint →
                :class:`PayloadTooLargeError`.
            Any 4xx body mentioning a rate-limit hint →
                :class:`RateLimitError`.
            5xx / other 4xx → :class:`TransientError`.
        """
        status = response.status_code
        if 200 <= status < 300:
            return

        body_text = self._safe_body_text(response)
        lowered = body_text.lower()

        if status == 429:
            raise RateLimitError(
                "LLM translation upstream returned HTTP 429",
                retry_after=_parse_retry_after(response),
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )

        if status == 413 or any(hint in lowered for hint in _CONTEXT_OVERFLOW_HINTS):
            raise PayloadTooLargeError(
                "LLM translation upstream rejected request as too large",
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )

        if any(hint in lowered for hint in _RATE_LIMIT_HINTS):
            raise RateLimitError(
                "LLM translation upstream reported rate limiting",
                retry_after=_parse_retry_after(response),
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )

        raise TransientError(
            f"LLM translation upstream returned HTTP {status}",
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

    def _extract_items(self, body: Any) -> list[dict[str, Any]]:
        """Pull the translation array out of the model's response.

        Supports the following shapes:

        1. The body is already a JSON array (bare-array response).
        2. Chat-completions-shaped body where the array lives in
           ``choices[0].message.content`` as a JSON-encoded string.
        3. MiniMax-style body with a ``base_resp.status_code`` field —
           non-zero codes are surfaced as transient failures with the
           upstream's human-readable ``status_msg`` attached.

        ``content`` is further post-processed before JSON parsing:

        - Any ``<think>...</think>`` prefix (emitted by MiniMax M2.x when
          ``reasoning_split`` is falsy) is stripped.
        - Markdown code fences (``` ```json ``` / ``` ``` ```) are
          unwrapped, since some models insist on them even when told
          not to.
        - Leading/trailing non-JSON chatter is sliced away by locating
          the first ``[`` and the last ``]``.

        Args:
            body: Parsed JSON response body.

        Returns:
            A list of ``{"id": ..., "translation": ...}`` dicts.

        Raises:
            TransientError: If the expected array cannot be located or
                parsed. The scheduler will retry.
        """
        # Shape 1: already an array.
        if isinstance(body, list):
            return body

        if not isinstance(body, dict):
            raise TransientError(
                "LLM translation response was neither a JSON object nor array",
                context={"provider_type": self.provider_type},
            )

        # MiniMax wraps every response in a ``base_resp`` envelope. A
        # non-zero status code means the request failed *at the business
        # layer* even if the HTTP status was 200 — surface it so the
        # scheduler's retry budget isn't wasted.
        base_resp = body.get("base_resp")
        if isinstance(base_resp, dict):
            raw_status = base_resp.get("status_code")
            try:
                status_code = int(raw_status) if raw_status is not None else 0
            except (TypeError, ValueError):
                status_code = 0
            if status_code != 0:
                status_msg = str(base_resp.get("status_msg") or "").strip()
                raise TransientError(
                    f"LLM translation upstream business error: "
                    f"base_resp.status_code={status_code} {status_msg!r}",
                    context={
                        "provider_type": self.provider_type,
                        "upstream_status_code": status_code,
                        "upstream_status_msg": status_msg,
                    },
                )

        choices = body.get("choices")
        if not isinstance(choices, list) or not choices:
            raise TransientError(
                "LLM translation response did not contain choices",
                context={"provider_type": self.provider_type},
            )
        first = choices[0]
        if not isinstance(first, dict):
            raise TransientError(
                "LLM translation response choice was not an object",
                context={"provider_type": self.provider_type},
            )
        message = first.get("message")
        if not isinstance(message, dict):
            raise TransientError(
                "LLM translation response message was not an object",
                context={"provider_type": self.provider_type},
            )
        content = message.get("content")
        if not isinstance(content, str):
            raise TransientError(
                "LLM translation response content was not a string",
                context={"provider_type": self.provider_type},
            )

        cleaned = _strip_think_and_fences(content)
        try:
            parsed = json.loads(cleaned)
        except (json.JSONDecodeError, ValueError):
            # Last-ditch salvage: slice out the first top-level JSON array.
            start = cleaned.find("[")
            end = cleaned.rfind("]")
            if start != -1 and end != -1 and end > start:
                candidate = cleaned[start : end + 1]
                try:
                    parsed = json.loads(candidate)
                except (json.JSONDecodeError, ValueError) as exc:
                    raise TransientError(
                        "LLM translation content was not valid JSON "
                        "after stripping markup",
                        context={
                            "provider_type": self.provider_type,
                            "content_preview": cleaned[:200],
                        },
                    ) from exc
            else:
                raise TransientError(
                    "LLM translation content was not valid JSON "
                    "after stripping markup",
                    context={
                        "provider_type": self.provider_type,
                        "content_preview": cleaned[:200],
                    },
                )

        if not isinstance(parsed, list):
            raise TransientError(
                "LLM translation response did not contain a translation array",
                context={
                    "provider_type": self.provider_type,
                    "parsed_type": type(parsed).__name__,
                },
            )
        return parsed

    def _merge_translations(
        self,
        entries: list[SubtitleEntry],
        items: list[Any],
    ) -> list[SubtitleEntry]:
        """Merge translated items back into the original entries.

        Validates:
            - ``len(items) == len(entries)``.
            - Every item is a dict with an ``id`` matching the
              corresponding entry's ``index`` and a string
              ``translation`` field (``""`` accepted when the input was
              whitespace-only; otherwise must be non-empty).

        Args:
            entries: Original subtitle entries, in order.
            items: Parsed items from the LLM response.

        Returns:
            A new list of subtitle entries whose ``text`` is the
            translation for each ``index`` / ``start_ms`` / ``end_ms``.

        Raises:
            TransientError: If the response violates any of the checks
                above. The scheduler will retry with backoff.
        """
        if len(items) != len(entries):
            raise TransientError(
                "LLM translation returned wrong number of items",
                context={
                    "provider_type": self.provider_type,
                    "expected": len(entries),
                    "actual": len(items),
                },
            )

        out: list[SubtitleEntry] = []
        for entry, item in zip(entries, items):
            if not isinstance(item, dict):
                raise TransientError(
                    "LLM translation item was not an object",
                    context={
                        "provider_type": self.provider_type,
                        "entry_index": entry.index,
                    },
                )
            item_id = item.get("id")
            # Accept both int and stringified int for id robustness.
            if item_id != entry.index and str(item_id) != str(entry.index):
                raise TransientError(
                    "LLM translation item id mismatch",
                    context={
                        "provider_type": self.provider_type,
                        "expected_id": entry.index,
                        "actual_id": item_id,
                    },
                )
            translation = item.get("translation")
            if not isinstance(translation, str):
                raise TransientError(
                    "LLM translation item missing translation string",
                    context={
                        "provider_type": self.provider_type,
                        "entry_index": entry.index,
                    },
                )
            out.append(
                SubtitleEntry(
                    index=entry.index,
                    start_ms=entry.start_ms,
                    end_ms=entry.end_ms,
                    text=translation,
                )
            )
        return out


def _parse_retry_after(response: httpx.Response) -> float | None:
    """Return the ``Retry-After`` header as seconds, or ``None``.

    Only the delta-seconds form is supported; HTTP-date form falls
    through to ``None`` so the scheduler's exponential-backoff path
    takes over.
    """
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


def _strip_think_and_fences(content: str) -> str:
    """Return ``content`` with ``<think>`` blocks and markdown fences removed.

    MiniMax M2.x routinely prefixes the actual JSON payload with a
    ``<think>...</think>`` block when ``reasoning_split`` is falsy; other
    reasoning-heavy models wrap their output in ``` ```json ... ``` ```
    fences even when instructed not to. Both are mechanical and safe to
    strip without altering the semantic JSON payload.

    The function is deliberately conservative: it only touches the first
    ``<think>`` block and any outermost fence pair, never anything
    inside the JSON payload itself.
    """
    text = content

    # Strip a leading <think>...</think> block if present (case-insensitive).
    lowered = text.lower()
    think_start = lowered.find("<think>")
    if think_start != -1:
        think_end = lowered.find("</think>", think_start + len("<think>"))
        if think_end != -1:
            text = text[:think_start] + text[think_end + len("</think>") :]
        else:
            # Unbalanced — drop everything up to the stray tag so at least
            # the tail (which is usually the real payload) has a chance.
            text = text[think_start + len("<think>") :]

    text = text.strip()

    # Strip an outermost ```...``` fence, optional ```json marker.
    if text.startswith("```"):
        # Remove leading ``` (plus optional language tag on the same line)
        # and trailing ``` if present. Anything between the two is
        # returned verbatim so numeric / array content is not touched.
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        if text.rstrip().endswith("```"):
            stripped = text.rstrip()
            text = stripped[: -len("```")]
        text = text.strip()

    return text


__all__ = ["LLMTranslationProvider"]
