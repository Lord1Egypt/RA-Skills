#!/usr/bin/env python3
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable, Dict, Optional


API_URL = "https://api.senseaudio.cn/v1/t2a_v2"


class SenseAudioError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        raw_body: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.raw_body = raw_body
        self.trace_id = trace_id


@dataclass
class TTSResult:
    audio_bytes: bytes
    trace_id: Optional[str]
    extra_info: Optional[Dict[str, object]]
    model_used: Optional[str] = None


def _parse_json_audio(body: str, *, model_used: Optional[str] = None) -> TTSResult:
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise SenseAudioError("Failed to parse non-stream TTS response.", raw_body=body) from exc

    base_resp = payload.get("base_resp") or {}
    status_code = base_resp.get("status_code")
    status_msg = base_resp.get("status_msg")
    trace_id = payload.get("trace_id")
    if status_code not in (None, 0):
        raise SenseAudioError(
            status_msg or "SenseAudio returned an error.",
            status_code=status_code,
            trace_id=trace_id,
            raw_body=body,
        )

    data = payload.get("data") or {}
    audio_hex = data.get("audio")
    if not audio_hex:
        raise SenseAudioError("No audio data returned.", trace_id=trace_id, raw_body=body)
    return TTSResult(
        audio_bytes=bytes.fromhex(audio_hex),
        trace_id=trace_id,
        extra_info=payload.get("extra_info"),
        model_used=model_used,
    )


def _candidate_models(requested_model: str, voice_id: str) -> list[str]:
    if requested_model != "auto":
        return [requested_model]
    if voice_id.startswith("vc-"):
        return ["SenseAudio-TTS-1.5", "SenseAudio-TTS-1.0"]
    return ["SenseAudio-TTS-1.0"]


def _supports_capability_error(exc: SenseAudioError) -> bool:
    haystack = f"{exc} {exc.raw_body or ''}".lower()
    return "model does not support this capability" in haystack


def _build_request(
    *,
    api_key: str,
    payload: dict,
    accept: Optional[str] = None,
) -> urllib.request.Request:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "AudioClaw-Continuous-Voice/1.0",
    }
    if accept:
        headers["Accept"] = accept
    return urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )


def _validate_payload_base(payload: dict, *, raw_body: Optional[str] = None) -> tuple[Optional[str], Optional[Dict[str, object]]]:
    base_resp = payload.get("base_resp") or {}
    status_code = base_resp.get("status_code")
    status_msg = base_resp.get("status_msg")
    trace_id = payload.get("trace_id")
    if status_code not in (None, 0):
        raise SenseAudioError(
            status_msg or "SenseAudio returned an error.",
            status_code=status_code,
            trace_id=trace_id,
            raw_body=raw_body,
        )
    return trace_id, payload.get("extra_info")


def synthesize(
    *,
    api_key: str,
    text: str,
    voice_id: str,
    audio_format: str = "mp3",
    sample_rate: int = 32000,
    model: str = "auto",
    speed: float = 1.0,
    volume: float = 1.0,
    pitch: int = 0,
    timeout: int = 120,
) -> TTSResult:
    last_exc: Optional[SenseAudioError] = None
    for candidate_model in _candidate_models(model, voice_id):
        payload = {
            "model": candidate_model,
            "text": text,
            "stream": False,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": volume,
                "pitch": pitch,
            },
            "audio_setting": {
                "format": audio_format,
                "sample_rate": sample_rate,
            },
        }
        request = _build_request(api_key=api_key, payload=payload)

        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8", "replace")
                return _parse_json_audio(body, model_used=candidate_model)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            error = SenseAudioError(
                f"HTTP {exc.code}: {body}",
                status_code=exc.code,
                raw_body=body,
            )
            last_exc = error
            if voice_id.startswith("vc-") and _supports_capability_error(error):
                continue
            raise error from exc
        except urllib.error.URLError as exc:
            raise SenseAudioError(f"Network error: {exc}") from exc
    raise last_exc or SenseAudioError("No compatible TTS model found.")


def stream_synthesize(
    *,
    api_key: str,
    text: str,
    voice_id: str,
    audio_format: str = "pcm",
    sample_rate: int = 32000,
    model: str = "auto",
    speed: float = 1.0,
    volume: float = 1.0,
    pitch: int = 0,
    timeout: int = 120,
    on_chunk: Optional[Callable[[bytes], None]] = None,
) -> TTSResult:
    last_exc: Optional[SenseAudioError] = None
    for candidate_model in _candidate_models(model, voice_id):
        payload = {
            "model": candidate_model,
            "text": text,
            "stream": True,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": volume,
                "pitch": pitch,
            },
            "audio_setting": {
                "format": audio_format,
                "sample_rate": sample_rate,
            },
        }
        request = _build_request(api_key=api_key, payload=payload, accept="text/event-stream")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                streamed_chunks: list[bytes] = []
                final_audio: Optional[bytes] = None
                trace_id: Optional[str] = None
                extra_info: Optional[Dict[str, object]] = None

                for raw in response:
                    line = raw.decode("utf-8", "replace").strip()
                    if not line or not line.startswith("data: "):
                        continue
                    body = line[6:]
                    try:
                        event = json.loads(body)
                    except json.JSONDecodeError as exc:
                        raise SenseAudioError("Failed to parse stream TTS response.", raw_body=body) from exc

                    trace_id, extra_info = _validate_payload_base(event, raw_body=body)
                    data = event.get("data") or {}
                    audio_hex = str(data.get("audio") or "")
                    status = int(data.get("status") or 0)
                    chunk = bytes.fromhex(audio_hex) if audio_hex else b""

                    if status == 2:
                        final_audio = chunk
                        continue

                    if chunk:
                        streamed_chunks.append(chunk)
                        if on_chunk is not None:
                            on_chunk(chunk)

                audio_bytes = final_audio if final_audio is not None else b"".join(streamed_chunks)
                if not audio_bytes:
                    raise SenseAudioError("No audio data returned from stream.", trace_id=trace_id)
                return TTSResult(
                    audio_bytes=audio_bytes,
                    trace_id=trace_id,
                    extra_info=extra_info,
                    model_used=candidate_model,
                )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            error = SenseAudioError(
                f"HTTP {exc.code}: {body}",
                status_code=exc.code,
                raw_body=body,
            )
            last_exc = error
            if voice_id.startswith("vc-") and _supports_capability_error(error):
                continue
            raise error from exc
        except urllib.error.URLError as exc:
            raise SenseAudioError(f"Network error: {exc}") from exc
    raise last_exc or SenseAudioError("No compatible TTS model found.")
