"""MiniMax synchronous text-to-speech provider.

Concrete :class:`TTSProvider` targeting MiniMax's synchronous ``t2a_v2``
HTTP endpoint (``POST /v1/t2a_v2``). One request → one MP3, returned as
a hex-encoded string in ``data.audio``. This is the "逐条同步" path —
for 10k-char-plus monologues MiniMax offers an async endpoint, but the
skill's per-subtitle flow is a better match for this synchronous API.

Design decisions
----------------

* ``supports_batch = False`` — the synchronous endpoint is single-text,
  so the scheduler runs one ``synth`` call per subtitle entry.
* ``payload_unit = "chars"`` — MiniMax caps each request at 10k chars.
* Response shape: ``data.audio`` is **hex**, not base64. Decoding uses
  :func:`bytes.fromhex` rather than ``base64.b64decode``.
* The mp3 bytes are transcoded to WAV before returning so the
  :class:`AudioAligner` (which expects WAV) can ingest them without
  format gymnastics — matches :class:`EdgeTTSProvider` for symmetry.

Error mapping
-------------

* HTTP 429 → :class:`RateLimitError` (``Retry-After`` honoured).
* HTTP 413 / "text too long" business code → :class:`PayloadTooLargeError`.
* HTTP 5xx, timeouts, malformed JSON, ``base_resp.status_code != 0`` →
  :class:`TransientError`.

Requirements: R6.4, R7.3, R12.2, R12.6, R12.7.
"""

from __future__ import annotations

import io
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

_DEFAULT_TIMEOUT_S: float = 180.0


@register(kind="tts", provider_type="minimax")
class MiniMaxTTSProvider:
    """MiniMax synchronous T2A provider."""

    provider_type: ClassVar[str] = "minimax"
    supports_batch: ClassVar[bool] = False
    payload_unit: ClassVar[Literal["chars", "tokens"]] = "chars"

    # MiniMax 的一批中文男声 ID，下面两个在 speech-2.x 上都可用；
    # 文档地址 https://platform.minimaxi.com/docs/guides/system-voices。
    _DEFAULT_VOICE: ClassVar[str] = "audiobook_male_1"

    def __init__(self) -> None:
        self.endpoint: str = "https://api.minimaxi.com/v1/t2a_v2"
        self.credential: str = ""
        self.model_name: str = "speech-2.8-hd"
        self.default_voice: str = self._DEFAULT_VOICE
        self.speed: float = 1.0
        self.vol: float = 1.0
        self.pitch: float = 0.0
        self.language_boost: str = "auto"
        self._timeout_s: float = _DEFAULT_TIMEOUT_S
        self._client: httpx.AsyncClient | None = None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def initialize(self, config: ProviderConfig) -> None:
        """Configure endpoint / credential / model / voice + prosody defaults.

        Manifest ``extra`` keys:

        ========================= =====================================
        ``model_name``            override synthesis model (default
                                 ``speech-2.8-hd``).
        ``default_voice``        voice id when caller omits one.
        ``speed`` / ``vol`` /    per-voice prosody knobs, forwarded
        ``pitch``                verbatim to ``voice_setting``.
        ``language_boost``       MiniMax's language hint; ``"auto"``
                                 works for Chinese without special
                                 handling.
        ``timeout_s``            HTTP client timeout (default 180 s).
        ========================= =====================================

        Raises:
            ValueError: If ``endpoint`` or ``credential`` is missing /
                empty.
        """
        if not config.endpoint:
            raise ValueError("MiniMaxTTSProvider requires a non-empty endpoint")
        if not config.credential:
            raise ValueError("MiniMaxTTSProvider requires a non-empty credential")
        self.endpoint = config.endpoint
        self.credential = config.credential

        extra = config.extra or {}
        model = extra.get("model_name")
        if model:
            self.model_name = str(model)
        voice = extra.get("default_voice")
        if voice:
            self.default_voice = str(voice)
        # Prosody knobs — keep silent defaults; MiniMax tolerates floats.
        for key in ("speed", "vol", "pitch"):
            if key in extra:
                try:
                    setattr(self, key, float(extra[key]))
                except (TypeError, ValueError):
                    pass
        lb = extra.get("language_boost")
        if isinstance(lb, str) and lb:
            self.language_boost = lb
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
        """Return character count — MiniMax prices and caps per-character."""
        return size_of_chars(text)

    # ------------------------------------------------------------------
    # HTTP client lifecycle
    # ------------------------------------------------------------------

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout_s)
        return self._client

    async def aclose(self) -> None:
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
            voice_id: Voice id, either a system voice (e.g.
                ``"audiobook_male_1"``) or a cloned voice id. Empty
                strings fall back to ``self.default_voice``.

        Returns:
            ``(wav_bytes, duration_ms)`` — mp3 transcoded to WAV for
            aligner compatibility.

        Raises:
            RateLimitError / PayloadTooLargeError / TransientError
            per the module docstring.
        """
        voice = voice_id or self.default_voice
        # MiniMax validates ``voice_setting`` fields as int64 — passing
        # ``0.0`` where ``0`` is expected fails with
        # ``Mismatch type int64 with value number``. Coerce everything
        # to int (truncating toward zero, which matches what MiniMax's
        # own sample clients do).
        voice_setting = {
            "voice_id": voice,
            "speed": int(self.speed) if float(self.speed).is_integer() else self.speed,
            "vol": int(self.vol) if float(self.vol).is_integer() else self.vol,
            "pitch": int(self.pitch),
        }
        payload = {
            "model": self.model_name,
            "text": text,
            "stream": False,
            "language_boost": self.language_boost,
            "voice_setting": voice_setting,
            "audio_setting": {
                "sample_rate": 32000,
                "bitrate": 128000,
                "format": "mp3",
                "channel": 1,
            },
            "output_format": "hex",
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
                "MiniMax tts request timed out",
                context={"provider_type": self.provider_type},
            ) from exc
        except httpx.HTTPError as exc:
            raise TransientError(
                f"MiniMax tts HTTP error: {exc}",
                context={"provider_type": self.provider_type},
            ) from exc

        self._raise_for_status(response)

        try:
            body = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            raise TransientError(
                "MiniMax tts response was not valid JSON",
                context={"provider_type": self.provider_type},
            ) from exc

        self._raise_for_business_error(body)
        return self._parse_body(body)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Translate non-2xx HTTP statuses to scheduler signal exceptions."""
        status = response.status_code
        if 200 <= status < 300:
            return
        body_text = response.text or "" if response.text is not None else ""
        lowered = body_text.lower()
        if status == 429:
            raise RateLimitError(
                "MiniMax tts upstream returned HTTP 429",
                retry_after=_parse_retry_after(response),
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )
        if status == 413 or "text too long" in lowered or "character limit" in lowered:
            raise PayloadTooLargeError(
                "MiniMax tts upstream rejected request as too large",
                context={
                    "provider_type": self.provider_type,
                    "status_code": status,
                },
            )
        raise TransientError(
            f"MiniMax tts upstream returned HTTP {status}",
            context={
                "provider_type": self.provider_type,
                "status_code": status,
            },
        )

    def _raise_for_business_error(self, body: Any) -> None:
        """Surface non-zero ``base_resp.status_code`` as a signal exception.

        MiniMax returns HTTP 200 even on business errors; the real
        status lives in ``body.base_resp.status_code``. ``0`` means
        success. Known codes we classify specially:

        * ``1004`` — authentication failed → transient (the scheduler
          will retry, but if it persists the wrapper surfaces the
          message).
        * ``1008`` / ``1013`` — rate-limited / quota exceeded →
          :class:`RateLimitError`.
        * ``1029`` — text too long → :class:`PayloadTooLargeError`.
        """
        base = body.get("base_resp") if isinstance(body, dict) else None
        if not isinstance(base, dict):
            return
        try:
            code = int(base.get("status_code", 0))
        except (TypeError, ValueError):
            code = 0
        if code == 0:
            return
        msg = str(base.get("status_msg") or "").strip()

        if code in (1008, 1013) or "rate" in msg.lower():
            raise RateLimitError(
                f"MiniMax tts rate-limited (base_resp={code}): {msg}",
                context={
                    "provider_type": self.provider_type,
                    "upstream_status_code": code,
                    "upstream_status_msg": msg,
                },
            )
        if code == 1029 or "too long" in msg.lower():
            raise PayloadTooLargeError(
                f"MiniMax tts payload too large (base_resp={code}): {msg}",
                context={
                    "provider_type": self.provider_type,
                    "upstream_status_code": code,
                    "upstream_status_msg": msg,
                },
            )
        raise TransientError(
            f"MiniMax tts business error (base_resp={code}): {msg}",
            context={
                "provider_type": self.provider_type,
                "upstream_status_code": code,
                "upstream_status_msg": msg,
            },
        )

    def _parse_body(self, body: Any) -> tuple[bytes, int]:
        """Extract ``(wav_bytes, duration_ms)`` from a 2xx response body.

        The ``data.audio`` field is a hex-encoded mp3 string. We decode
        hex → mp3 bytes, then transcode to WAV via pydub so the
        downstream aligner can read it with its usual
        ``AudioSegment.from_file(BytesIO, format='wav')`` path.
        """
        if not isinstance(body, dict):
            raise TransientError(
                "MiniMax tts response was not a JSON object",
                context={"provider_type": self.provider_type},
            )
        data = body.get("data")
        if not isinstance(data, dict):
            raise TransientError(
                "MiniMax tts response missing data object",
                context={"provider_type": self.provider_type},
            )
        audio_hex = data.get("audio")
        if not isinstance(audio_hex, str) or not audio_hex:
            raise TransientError(
                "MiniMax tts response missing data.audio hex string",
                context={"provider_type": self.provider_type},
            )
        try:
            mp3_bytes = bytes.fromhex(audio_hex)
        except ValueError as exc:
            raise TransientError(
                "MiniMax tts data.audio was not valid hex",
                context={"provider_type": self.provider_type},
            ) from exc

        # Transcode mp3 → wav so the downstream aligner (pydub +
        # ``format="wav"`` decoding) can consume it as-is.
        try:
            from pydub import AudioSegment  # type: ignore[import-not-found]

            segment = AudioSegment.from_file(io.BytesIO(mp3_bytes), format="mp3")
            duration_ms = int(len(segment))
            wav_buffer = io.BytesIO()
            segment.export(wav_buffer, format="wav")
            wav_bytes = wav_buffer.getvalue()
        except Exception as exc:
            raise TransientError(
                f"failed to transcode MiniMax mp3 to WAV: {exc}",
                context={"provider_type": self.provider_type},
            ) from exc

        # Prefer the server-reported duration when present; it's the
        # most accurate. Fall back to the decoded wav length otherwise.
        extra_info = body.get("extra_info") if isinstance(body, dict) else None
        reported_duration_ms: int | None = None
        if isinstance(extra_info, dict):
            raw = extra_info.get("audio_length")
            try:
                reported_duration_ms = int(raw) if raw is not None else None
            except (TypeError, ValueError):
                reported_duration_ms = None

        final_duration = (
            reported_duration_ms
            if reported_duration_ms is not None and reported_duration_ms >= 0
            else duration_ms
        )
        return wav_bytes, max(0, final_duration)


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


__all__ = ["MiniMaxTTSProvider"]
