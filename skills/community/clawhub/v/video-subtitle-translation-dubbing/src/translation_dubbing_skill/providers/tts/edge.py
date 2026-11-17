"""Microsoft Edge Read-Aloud TTS provider.

Wraps the `edge-tts` Python library (which in turn talks to Microsoft's
free Read-Aloud service) as a ``TTSProvider`` the skill can use. Unlike
:class:`WebTTSProvider` this provider doesn't make a raw HTTP request —
``edge-tts`` handles the bespoke WebSocket protocol internally and we
just receive the resulting MP3 bytes.

Design decisions
----------------

* ``supports_batch = False`` — the Edge endpoint is single-shot, so the
  scheduler runs one ``synth`` call per subtitle entry.
* ``payload_unit = "chars"`` — Edge measures text length in characters.
* The service is unauthenticated, but the skill's manifest requires
  every provider config to carry a ``credential`` string. We therefore
  accept any non-empty string (e.g. ``"none"``) as a credential and
  ignore it.
* On repeated transient WebSocket errors we raise
  :class:`TransientError` so the adaptive scheduler will retry with
  backoff — matching the behaviour of every other provider.

Requirements: R6.4, R7.3, R12.2.
"""

from __future__ import annotations

import asyncio
import io
from typing import Any, ClassVar, Literal

from translation_dubbing_skill.models import ProviderConfig
from translation_dubbing_skill.providers.registry import register
from translation_dubbing_skill.scheduler.signals import TransientError
from translation_dubbing_skill.scheduler.sizing import size_of_chars


@register(kind="tts", provider_type="edge")
class EdgeTTSProvider:
    """Microsoft Edge Read-Aloud TTS via the ``edge-tts`` Python library."""

    provider_type: ClassVar[str] = "edge"
    supports_batch: ClassVar[bool] = False
    payload_unit: ClassVar[Literal["chars", "tokens"]] = "chars"

    # Edge voice for simplified Chinese that most users recognise; the
    # caller can still override per invocation or via extras.default_voice.
    # We pick a male voice by default because the skill's target content
    # (long-form commentary / explainers) reads more naturally in a
    # lower-register voice than in the higher-pitched Xiaoxiao.
    _DEFAULT_VOICE: ClassVar[str] = "zh-CN-YunxiNeural"

    def __init__(self) -> None:
        self.default_voice: str = self._DEFAULT_VOICE
        # Optional prosody controls passed straight through to edge-tts.
        self.rate: str = "+0%"
        self.volume: str = "+0%"
        self.pitch: str = "+0Hz"

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def initialize(self, config: ProviderConfig) -> None:
        """Pick up optional prosody defaults from the manifest's extras.

        Edge is unauthenticated so ``config.credential`` is ignored; we
        still accept the dataclass as-is because the skill shape
        requires it.
        """
        extra = config.extra or {}
        default_voice = extra.get("default_voice")
        if isinstance(default_voice, str) and default_voice:
            self.default_voice = default_voice
        for attr in ("rate", "volume", "pitch"):
            value = extra.get(attr)
            if isinstance(value, str) and value:
                setattr(self, attr, value)

    # ------------------------------------------------------------------
    # Sizing
    # ------------------------------------------------------------------

    def size_of(self, text: str) -> int:
        return size_of_chars(text)

    # ------------------------------------------------------------------
    # Synthesis
    # ------------------------------------------------------------------

    async def synth(self, text: str, voice_id: str) -> tuple[bytes, int]:
        """Synthesize one subtitle entry.

        Returns:
            ``(mp3_bytes, duration_ms)`` — Edge delivers MP3 directly. We
            measure the duration by decoding the MP3 via ``pydub`` after
            streaming finishes; this adds a small CPU cost but keeps
            ``duration_ms`` accurate so the aligner can compute atempo
            rates correctly.

        Raises:
            TransientError: On any ``edge-tts`` failure (network blip,
                invalid voice, throttling). The scheduler retries with
                backoff — a transient error here is the correct signal
                because the Edge service does not publish a stable
                status-code contract.
        """
        # Import lazily so the rest of the skill can be used without
        # installing edge-tts.
        try:
            import edge_tts  # type: ignore[import-not-found]
        except ImportError as exc:  # pragma: no cover — dev dep
            raise TransientError(
                "edge-tts is not installed; pip install edge-tts",
                context={"provider_type": self.provider_type},
            ) from exc

        # Multi-language voice mapping table
        voice_mapping = {
            "zh-cn": "zh-CN-YunxiNeural",
            "zh": "zh-CN-YunxiNeural",
            "en": "en-US-GuyNeural",
            "en-us": "en-US-GuyNeural",
            "ja": "ja-JP-KeitaNeural",
            "ja-jp": "ja-JP-KeitaNeural",
            "es": "es-ES-AlvaroNeural",
            "es-es": "es-ES-AlvaroNeural",
            "fr": "fr-FR-EloiseNeural",
            "fr-fr": "fr-FR-EloiseNeural",
            "de": "de-DE-KillianNeural",
            "de-de": "de-DE-KillianNeural",
            "ko": "ko-KR-SunHiNeural",
            "ko-kr": "ko-KR-SunHiNeural",
            "it": "it-IT-DiegoNeural",
            "it-it": "it-IT-DiegoNeural",
            "ru": "ru-RU-DmitryNeural",
            "ru-ru": "ru-RU-DmitryNeural",
            "pt": "pt-BR-AntonioNeural",
            "pt-br": "pt-BR-AntonioNeural"
        }

        # Resolve voice id based on target mapping if matching key
        requested_voice = voice_id or self.default_voice
        voice = voice_mapping.get(requested_voice.lower(), requested_voice)

        communicator = edge_tts.Communicate(
            text,
            voice,
            rate=self.rate,
            volume=self.volume,
            pitch=self.pitch,
        )

        audio_buffer = io.BytesIO()
        try:
            async for chunk in communicator.stream():
                if chunk["type"] == "audio":
                    audio_buffer.write(chunk["data"])
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            # edge-tts's exception hierarchy is not stable; treat any
            # failure as transient so the scheduler can retry.
            raise TransientError(
                f"edge-tts stream failed: {exc}",
                context={
                    "provider_type": self.provider_type,
                    "voice": voice,
                },
            ) from exc

        audio = audio_buffer.getvalue()
        if not audio:
            raise TransientError(
                "edge-tts returned no audio payload",
                context={
                    "provider_type": self.provider_type,
                    "voice": voice,
                },
            )

        # Edge returns MP3; downstream (aligner) expects WAV. Decode the
        # MP3 via pydub and re-export as WAV so the provider contract
        # matches :class:`LLMTTSProvider` / :class:`WebTTSProvider`. The
        # re-export is also where we get ``duration_ms`` for free.
        try:
            from pydub import AudioSegment  # type: ignore[import-not-found]

            segment = AudioSegment.from_file(io.BytesIO(audio), format="mp3")
            duration_ms = int(len(segment))
            wav_buffer = io.BytesIO()
            segment.export(wav_buffer, format="wav")
            wav_bytes = wav_buffer.getvalue()
        except Exception as exc:
            raise TransientError(
                f"failed to transcode edge-tts audio to WAV: {exc}",
                context={"provider_type": self.provider_type},
            ) from exc

        return wav_bytes, max(0, duration_ms)


__all__ = ["EdgeTTSProvider"]
