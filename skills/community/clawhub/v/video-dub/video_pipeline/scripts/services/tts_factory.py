import os

from services.azure_tts_provider import AzureTTSProvider
from services.edge_tts_provider import EdgeTTSProvider
from services.tts_base import TTSProvider
from services.volcengine_tts_provider import VolcengineTTSProvider
from services.windows_sapi_tts_provider import WindowsSapiTTSProvider


def _resolve_edge_voice(voice_type: str | None) -> str:
    candidate = (voice_type or "").strip()
    if candidate.startswith(("zh-", "en-", "ja-", "ko-")) and candidate.endswith("Neural"):
        return candidate
    return os.getenv("EDGE_TTS_VOICE", "zh-CN-YunjianNeural")


def build_tts_provider(provider_name: str | None = None, voice_type: str | None = None) -> TTSProvider:
    resolved_provider = (provider_name or os.getenv("TTS_PROVIDER") or "edge").strip().lower()

    if resolved_provider == "volcengine":
        return VolcengineTTSProvider(voice_type=voice_type)
    if resolved_provider == "azure":
        return AzureTTSProvider(voice=voice_type)
    if resolved_provider == "edge":
        return EdgeTTSProvider(voice=_resolve_edge_voice(voice_type))
    if resolved_provider in {"windows_sapi", "sapi"}:
        return WindowsSapiTTSProvider(
            voice=voice_type or os.getenv("WINDOWS_SAPI_TTS_VOICE", "Microsoft Huihui Desktop")
        )

    raise ValueError(f"Unsupported TTS provider: {resolved_provider}")
