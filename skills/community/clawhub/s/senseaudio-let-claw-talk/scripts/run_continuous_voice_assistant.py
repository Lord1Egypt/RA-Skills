#!/usr/bin/env python3
import argparse
import collections
import contextlib
import difflib
import json
import math
import os
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
import wave
from pathlib import Path
from typing import Optional

from local_senseaudio_asr import ASRRequest, transcribe as local_asr_transcribe
from local_senseaudio_tts import synthesize as local_tts_synthesize, stream_synthesize as local_tts_stream_synthesize
from local_voice_catalog import all_voices, find_voice, load_clone_voices, save_clone_voices, upsert_clone_voice
from local_wespeaker_client import (
    clear_profile as wespeaker_clear_profile,
    ensure_service as ensure_wespeaker_service,
    get_log_path as get_wespeaker_log_path,
    health as wespeaker_health,
    profile_status as wespeaker_profile_status,
    stop_service as stop_wespeaker_service,
    verify_audio as wespeaker_verify_audio,
    enroll_audio as wespeaker_enroll_audio,
)

try:
    import numpy as np
except Exception:
    np = None

try:
    import sounddevice as sd
except Exception:
    sd = None

try:
    import webrtcvad
except Exception:
    webrtcvad = None

try:
    import miniaudio
except Exception:
    miniaudio = None


CURRENT_FILE = Path(__file__).resolve()


def get_workspace_root() -> Path:
    env_workspace = os.getenv("AUDIOCLAW_WORKSPACE", "").strip()
    if env_workspace:
        path = Path(env_workspace).expanduser().resolve()
        if path.exists():
            return path

    for parent in CURRENT_FILE.parents:
        if parent.name == "workspace":
            return parent

    return (Path.home() / ".audioclaw" / "workspace").resolve()


WORKSPACE_ROOT = get_workspace_root()
SCRIPT_DIR = CURRENT_FILE.parent
MIC_SOURCE = SCRIPT_DIR / "macos_mic_capture.swift"
MIC_BINARY = SCRIPT_DIR / "macos_mic_capture"
AUDIO_STATE_DIR = WORKSPACE_ROOT / "state" / "audio" / "voiceclaw"
PREFERENCES_PATH = WORKSPACE_ROOT / "state" / "voiceclaw_preferences.json"
RUNTIME_STATE_PATH = WORKSPACE_ROOT / "state" / "voiceclaw_runtime_state.json"
CLONE_VOICES_PATH = WORKSPACE_ROOT / "state" / "voiceclaw_clone_voices.json"
TTS_VALIDATION_CACHE_PATH = WORKSPACE_ROOT / "state" / "voiceclaw_tts_validation_cache.json"
SHARED_CREDENTIALS_PATH = WORKSPACE_ROOT / "state" / "senseaudio_credentials.json"
WESPEAKER_GUIDE_PATH = CURRENT_FILE.parent.parent / "references" / "wespeaker_user_setup.md"
DEFAULT_AGENT = Path("/Applications/商汤输入法AudioClaw.app/Contents/Resources/claws/picoclaw/audioclaw-darwin-amd64")
SYSTEM_SOUND_DIR = Path("/System/Library/Sounds")
STATUS_SOUNDS = {
    "activated": SYSTEM_SOUND_DIR / "Glass.aiff",
    "heard": SYSTEM_SOUND_DIR / "Pop.aiff",
    "listen": SYSTEM_SOUND_DIR / "Morse.aiff",
    "thinking": SYSTEM_SOUND_DIR / "Tink.aiff",
    "error": SYSTEM_SOUND_DIR / "Basso.aiff",
    "exit": SYSTEM_SOUND_DIR / "Submarine.aiff",
}
WESPEAKER_ENROLL_EXAMPLE = "今天下午我会把会议纪要整理好，然后发给团队确认。"
LEGACY_SPOKEN_STYLE_PROMPT = (
    "你现在正通过本机语音助手直接对用户说话。"
    "默认请用自然、口语化、很简短的中文回答，先直接给结论。"
    "不要使用 Markdown 标题、项目符号、表格或代码块。"
    "一般控制在 1 到 3 句，除非用户明确要求展开。"
    "优先用短句，少解释，不要重复用户问题，不要铺垫。"
    "如果必须补充信息，也请像真人聊天那样顺着说，不要念清单。"
)
DEFAULT_SPOKEN_STYLE_PROMPT = (
    "你现在通过语音助手直接对用户说话。"
    "请用自然、简短、口语化的中文回答，先说结论。"
    "默认 1 到 2 句，不要复述问题，不要用 Markdown 或清单。"
    "少解释，少铺垫，少套话，像真人接话一样往下说。"
    "如果用户刚打断过你，就顺着他这句接，不要重新讲一大段上一轮内容。"
)


class StreamingPlaybackInterrupted(Exception):
    pass


PREFERENCE_KEYS = (
    "voice_id",
    "emotion",
    "tts_speed",
    "senseaudio_streaming_tts",
    "senseaudio_streaming_backend",
    "wake_asr_model",
    "wake_phrase",
    "sleep_phrase",
    "wake_sticky_seconds",
    "interrupt_playback",
    "interrupt_grace_seconds",
    "interrupt_min_speech_seconds",
    "interrupt_speech_threshold_db",
    "silence_seconds",
    "min_speech_seconds",
    "speech_threshold_db",
    "vad_mode",
    "spoken_style_prompt",
    "status_sounds",
    "speaker_verification_backend",
    "wespeaker_threshold",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Continuous voice wrapper around audioclaw agent.")
    parser.add_argument("--agent-bin", default=str(DEFAULT_AGENT))
    parser.add_argument("--session", default="voiceclaw:default")
    parser.add_argument("--agent-retries", type=int, default=3)
    parser.add_argument("--agent-retry-delay-seconds", type=float, default=1.5)
    parser.add_argument("--asr-model", default=os.getenv("SENSEAUDIO_ASR_MODEL", "sense-asr-deepthink"))
    parser.add_argument("--wake-asr-model", default=os.getenv("SENSEAUDIO_WAKE_ASR_MODEL", "sense-asr-lite"))
    parser.add_argument("--voice-id", default="male_0004_a")
    parser.add_argument("--emotion", default="calm")
    parser.add_argument("--tts-mode", choices=["say", "senseaudio", "none"], default="say")
    parser.add_argument("--tts-speed", type=float, default=1.25)
    parser.add_argument(
        "--senseaudio-streaming-tts",
        dest="senseaudio_streaming_tts",
        action="store_true",
        default=os.getenv("VOICECLAW_SENSEAUDIO_STREAMING_TTS", "1").strip().lower() not in {"0", "false", "no"},
    )
    parser.add_argument("--no-senseaudio-streaming-tts", dest="senseaudio_streaming_tts", action="store_false")
    parser.add_argument(
        "--senseaudio-streaming-backend",
        choices=["auto", "pcm", "miniaudio"],
        default=os.getenv("VOICECLAW_SENSEAUDIO_STREAMING_BACKEND", "auto"),
    )
    parser.add_argument("--say-voice", default="")
    parser.add_argument("--input-file", default="")
    parser.add_argument("--capture-backend", choices=["auto", "python", "swift"], default="auto")
    parser.add_argument("--wake-phrase", default=os.getenv("VOICECLAW_WAKE_PHRASE", "贾维斯"))
    parser.add_argument("--no-wake-phrase", dest="wake_phrase", action="store_const", const="")
    parser.add_argument("--sleep-phrase", default=os.getenv("VOICECLAW_SLEEP_PHRASE", "贾维斯休息"))
    parser.add_argument("--no-sleep-phrase", dest="sleep_phrase", action="store_const", const="")
    parser.add_argument("--wake-sticky-seconds", type=float, default=90.0)
    parser.add_argument("--interrupt-playback", dest="interrupt_playback", action="store_true")
    parser.add_argument("--no-interrupt-playback", dest="interrupt_playback", action="store_false")
    parser.add_argument("--interrupt-grace-seconds", type=float, default=1.2)
    parser.add_argument("--interrupt-min-speech-seconds", type=float, default=0.35)
    parser.add_argument("--interrupt-speech-threshold-db", type=float, default=-16.0)
    parser.add_argument("--spoken-style-prompt", default=os.getenv("VOICECLAW_SPOKEN_STYLE_PROMPT", DEFAULT_SPOKEN_STYLE_PROMPT))
    parser.add_argument("--preferences-file", default=str(PREFERENCES_PATH))
    parser.add_argument("--status-sounds", dest="status_sounds", action="store_true")
    parser.add_argument("--no-status-sounds", dest="status_sounds", action="store_false")
    parser.add_argument("--sample-rate", type=int, default=16000)
    parser.add_argument("--max-wait-seconds", type=float, default=30.0)
    parser.add_argument("--max-record-seconds", type=float, default=25.0)
    parser.add_argument("--silence-seconds", type=float, default=1.6)
    parser.add_argument("--min-speech-seconds", type=float, default=0.25)
    parser.add_argument("--speech-threshold-db", type=float, default=-27.0)
    parser.add_argument("--vad-mode", type=int, choices=[0, 1, 2, 3], default=1)
    parser.add_argument("--frame-ms", type=int, choices=[10, 20, 30], default=20)
    parser.add_argument("--padding-ms", type=int, default=300)
    parser.add_argument("--cooldown-seconds", type=float, default=0.3)
    parser.add_argument("--post-reply-cooldown-seconds", type=float, default=0.02)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--skip-self-check", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--speaker-verification-backend", choices=["none", "wespeaker"], default=os.getenv("VOICECLAW_SPEAKER_BACKEND", "none"))
    parser.add_argument("--wespeaker-threshold", type=float, default=float(os.getenv("VOICECLAW_WESPEAKER_THRESHOLD", "0.72")))
    parser.add_argument("--wespeaker-host", default=os.getenv("VOICECLAW_WESPEAKER_HOST", "127.0.0.1"))
    parser.add_argument("--wespeaker-port", type=int, default=int(os.getenv("VOICECLAW_WESPEAKER_PORT", "18567")))
    parser.add_argument("--wespeaker-model", default=os.getenv("VOICECLAW_WESPEAKER_MODEL", "chinese"))
    parser.add_argument("--wespeaker-state-dir", default=str(WORKSPACE_ROOT / "state" / "wespeaker"))
    parser.add_argument(
        "--wespeaker-python",
        default=os.getenv("VOICECLAW_WESPEAKER_PYTHON", str(WORKSPACE_ROOT / "tools" / "wespeaker" / ".venv" / "bin" / "python")),
    )
    parser.add_argument("--wespeaker-service-script", default=str(SCRIPT_DIR / "local_wespeaker_service.py"))
    parser.set_defaults(status_sounds=True, interrupt_playback=True)
    return parser.parse_args()


def print_status(text: str) -> None:
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def play_status_sound(kind: str, args: argparse.Namespace) -> None:
    if not args.status_sounds:
        return
    sound_path = STATUS_SOUNDS.get(kind)
    if not sound_path or not sound_path.exists():
        return
    subprocess.run(
        ["/usr/bin/afplay", str(sound_path)],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def run_json(command: list[str], *, check: bool = True) -> dict:
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    stdout = (completed.stdout or "").strip()
    stderr = (completed.stderr or "").strip()
    if check and completed.returncode != 0:
        raise RuntimeError(stderr or stdout or f"Command failed: {' '.join(command)}")
    if not stdout:
        return {"status": "empty", "returncode": completed.returncode, "stderr": stderr}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Expected JSON but got: {stdout[:400]}") from exc


def load_shared_credentials() -> dict:
    try:
        payload = json.loads(SHARED_CREDENTIALS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    return {str(k): str(v) for k, v in payload.items() if isinstance(k, str) and isinstance(v, (str, int, float))}


def resolve_api_key(purpose: str) -> str:
    shared = load_shared_credentials()
    if purpose == "asr":
        candidates = [
            os.getenv("AUDIOCLAW_ASR_API_KEY", ""),
            os.getenv("SENSEAUDIO_ASR_API_KEY", ""),
            os.getenv("AUDIOCLAW_VOICE_API_KEY", ""),
            os.getenv("SENSEAUDIO_API_KEY", ""),
            str(shared.get("AUDIOCLAW_ASR_API_KEY") or ""),
            str(shared.get("SENSEAUDIO_ASR_API_KEY") or ""),
            str(shared.get("SENSEAUDIO_API_KEY") or ""),
        ]
    else:
        candidates = [
            os.getenv("AUDIOCLAW_TTS_API_KEY", ""),
            os.getenv("AUDIOCLAW_VOICE_API_KEY", ""),
            os.getenv("SENSEAUDIO_TTS_API_KEY", ""),
            os.getenv("SENSEAUDIO_API_KEY", ""),
            str(shared.get("AUDIOCLAW_TTS_API_KEY") or ""),
            str(shared.get("SENSEAUDIO_TTS_API_KEY") or ""),
            str(shared.get("SENSEAUDIO_API_KEY") or ""),
        ]

    for value in candidates:
        value = str(value or "").strip()
        if value and not value.startswith("v2.public."):
            return value
    raise RuntimeError(f"Missing usable SenseAudio {purpose.upper()} API key.")


def preference_defaults() -> dict:
    return {
        "voice_id": "male_0004_a",
        "emotion": "calm",
        "tts_speed": 1.25,
        "senseaudio_streaming_tts": os.getenv("VOICECLAW_SENSEAUDIO_STREAMING_TTS", "1").strip().lower() not in {"0", "false", "no"},
        "senseaudio_streaming_backend": os.getenv("VOICECLAW_SENSEAUDIO_STREAMING_BACKEND", "auto"),
        "wake_asr_model": os.getenv("SENSEAUDIO_WAKE_ASR_MODEL", "sense-asr-lite"),
        "wake_phrase": os.getenv("VOICECLAW_WAKE_PHRASE", "贾维斯"),
        "sleep_phrase": os.getenv("VOICECLAW_SLEEP_PHRASE", "贾维斯休息"),
        "wake_sticky_seconds": 90.0,
        "interrupt_playback": True,
        "interrupt_grace_seconds": 1.2,
        "interrupt_min_speech_seconds": 0.35,
        "interrupt_speech_threshold_db": -16.0,
        "silence_seconds": 1.6,
        "min_speech_seconds": 0.25,
        "speech_threshold_db": -27.0,
        "vad_mode": 1,
        "spoken_style_prompt": os.getenv("VOICECLAW_SPOKEN_STYLE_PROMPT", DEFAULT_SPOKEN_STYLE_PROMPT),
        "status_sounds": True,
        "speaker_verification_backend": os.getenv("VOICECLAW_SPEAKER_BACKEND", "none"),
        "wespeaker_threshold": float(os.getenv("VOICECLAW_WESPEAKER_THRESHOLD", "0.72")),
    }


def get_preferences_path(args: argparse.Namespace) -> Path:
    return Path(str(args.preferences_file)).expanduser().resolve()


def load_preferences(args: argparse.Namespace) -> dict:
    path = get_preferences_path(args)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload


def load_tts_validation_cache() -> dict:
    if not TTS_VALIDATION_CACHE_PATH.exists():
        return {}
    try:
        payload = json.loads(TTS_VALIDATION_CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def save_tts_validation_cache(payload: dict) -> None:
    TTS_VALIDATION_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TTS_VALIDATION_CACHE_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def get_cached_tts_validation(voice_id: str) -> Optional[dict]:
    cache = load_tts_validation_cache()
    item = cache.get(str(voice_id or "").strip())
    if not isinstance(item, dict):
        return None
    expires_at = float(item.get("expires_at") or 0.0)
    if expires_at <= time.time():
        return None
    return item


def remember_tts_validation(voice_id: str, error: Optional[str]) -> None:
    cache = load_tts_validation_cache()
    now = time.time()
    success = error is None
    ttl = 24 * 3600 if success else 20 * 60
    cache[str(voice_id or "").strip()] = {
        "ok": success,
        "error": str(error or ""),
        "updated_at": now,
        "expires_at": now + ttl,
    }
    save_tts_validation_cache(cache)


def save_preferences(args: argparse.Namespace) -> Path:
    path = get_preferences_path(args)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {key: getattr(args, key) for key in PREFERENCE_KEYS if hasattr(args, key)}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def clear_preferences(args: argparse.Namespace) -> Path:
    path = get_preferences_path(args)
    if path.exists():
        path.unlink()
    defaults = preference_defaults()
    for key, value in defaults.items():
        if hasattr(args, key):
            setattr(args, key, value)
    return path


def apply_preferences(args: argparse.Namespace) -> dict:
    loaded = load_preferences(args)
    defaults = preference_defaults()
    for key in PREFERENCE_KEYS:
        if key not in loaded or not hasattr(args, key):
            continue
        value = loaded[key]
        default = defaults.get(key)
        if isinstance(default, bool):
            value = bool(value)
        elif isinstance(default, int) and not isinstance(default, bool):
            value = int(value)
        elif isinstance(default, float):
            value = float(value)
        elif isinstance(default, str):
            value = str(value)
            if key == "spoken_style_prompt" and value == LEGACY_SPOKEN_STYLE_PROMPT:
                value = DEFAULT_SPOKEN_STYLE_PROMPT
        setattr(args, key, value)
    return loaded


def get_runtime_state_path() -> Path:
    return RUNTIME_STATE_PATH


def build_runtime_summary(args: argparse.Namespace, speaker_profile: dict) -> dict:
    clone_data = load_voice_catalog()
    return {
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "wake_phrase": args.wake_phrase,
        "sleep_phrase": args.sleep_phrase,
        "wake_sticky_seconds": float(args.wake_sticky_seconds),
        "tts": {
            "mode": args.tts_mode,
            "streaming": bool(getattr(args, "senseaudio_streaming_tts", False)),
            "streaming_backend": str(getattr(args, "senseaudio_streaming_backend", "auto")),
            "voice_id": args.voice_id,
            "voice_label": describe_voice(args.voice_id, clone_data),
            "emotion": args.emotion,
            "speed": float(args.tts_speed),
        },
        "capture": {
            "silence_seconds": float(args.silence_seconds),
            "speech_threshold_db": float(args.speech_threshold_db),
            "vad_mode": int(args.vad_mode),
            "asr_model": args.asr_model,
            "wake_asr_model": args.wake_asr_model,
        },
        "interrupt": {
            "enabled": bool(args.interrupt_playback),
            "grace_seconds": float(args.interrupt_grace_seconds),
            "min_speech_seconds": float(args.interrupt_min_speech_seconds),
            "speech_threshold_db": float(args.interrupt_speech_threshold_db),
        },
        "memory": {
            "preferences_file": str(get_preferences_path(args)),
        },
        "speaker_verification": {
            "backend": args.speaker_verification_backend,
            "wespeaker_threshold": float(args.wespeaker_threshold),
            "status": speaker_profile.get("wespeaker", {}),
        },
    }


def save_runtime_state(args: argparse.Namespace, speaker_profile: dict) -> Path:
    path = get_runtime_state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_runtime_summary(args, speaker_profile)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def format_runtime_summary(args: argparse.Namespace, speaker_profile: dict) -> str:
    clone_data = load_voice_catalog()
    parts = [
        f"唤醒词是“{args.wake_phrase or '无'}”",
        f"睡眠词是“{args.sleep_phrase or '无'}”",
        f"音色是 {describe_voice(args.voice_id, clone_data)}",
        f"语速是 {float(args.tts_speed):.2f}",
        f"流式播报{'开启' if getattr(args, 'senseaudio_streaming_tts', False) else '关闭'}",
        f"流式后端是 {getattr(args, 'senseaudio_streaming_backend', 'auto')}",
        f"打断{'开启' if args.interrupt_playback else '关闭'}",
        f"静音收尾 {float(args.silence_seconds):.1f} 秒",
        f"起录阈值 {float(args.speech_threshold_db):.1f}dB",
        f"最短语音 {float(args.min_speech_seconds):.2f} 秒",
    ]
    if args.speaker_verification_backend == "wespeaker":
        status = speaker_profile.get("wespeaker") or {}
        sample_count = int(status.get("sample_count") or 0)
        if sample_count > 0:
            parts.append(f"WeSpeaker 声纹验证开启，已录入 {sample_count} 段样本")
        else:
            parts.append("WeSpeaker 声纹验证开启，但还没录入声音样本")
    return "现在的设置是：" + "，".join(parts) + "。"


def read_wave_mono(audio_path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(audio_path), "rb") as wf:
        channels = wf.getnchannels()
        sample_rate = wf.getframerate()
        sample_width = wf.getsampwidth()
        frames = wf.readframes(wf.getnframes())

    if sample_width != 2:
        raise RuntimeError("Only 16-bit PCM WAV is supported for speaker lock.")

    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
    if channels > 1:
        audio = audio.reshape(-1, channels).mean(axis=1)
    audio /= 32768.0
    return audio, sample_rate


def resample_audio(audio: np.ndarray, sample_rate: int, target_rate: int = 16000) -> tuple[np.ndarray, int]:
    if sample_rate == target_rate:
        return audio, sample_rate
    if audio.size == 0:
        return audio, target_rate
    duration = audio.shape[0] / float(sample_rate)
    source_times = np.linspace(0.0, duration, num=audio.shape[0], endpoint=False)
    target_length = max(1, int(round(duration * target_rate)))
    target_times = np.linspace(0.0, duration, num=target_length, endpoint=False)
    resampled = np.interp(target_times, source_times, audio).astype(np.float32)
    return resampled, target_rate


def hz_to_mel(hz: np.ndarray) -> np.ndarray:
    return 2595.0 * np.log10(1.0 + hz / 700.0)


def mel_to_hz(mel: np.ndarray) -> np.ndarray:
    return 700.0 * (10 ** (mel / 2595.0) - 1.0)


def build_mel_filterbank(sample_rate: int, n_fft: int, n_mels: int = 26) -> np.ndarray:
    low_mel = hz_to_mel(np.array([0.0], dtype=np.float32))[0]
    high_mel = hz_to_mel(np.array([sample_rate / 2.0], dtype=np.float32))[0]
    mel_points = np.linspace(low_mel, high_mel, n_mels + 2)
    hz_points = mel_to_hz(mel_points)
    bins = np.floor((n_fft + 1) * hz_points / sample_rate).astype(int)

    filters = np.zeros((n_mels, n_fft // 2 + 1), dtype=np.float32)
    for i in range(1, n_mels + 1):
        left = bins[i - 1]
        center = bins[i]
        right = bins[i + 1]
        if center <= left:
            center = left + 1
        if right <= center:
            right = center + 1
        for j in range(left, min(center, filters.shape[1])):
            filters[i - 1, j] = (j - left) / float(max(1, center - left))
        for j in range(center, min(right, filters.shape[1])):
            filters[i - 1, j] = (right - j) / float(max(1, right - center))
    return filters


def build_dct_basis(n_mfcc: int, n_mels: int) -> np.ndarray:
    basis = np.zeros((n_mfcc, n_mels), dtype=np.float32)
    scale = math.pi / float(n_mels)
    for i in range(n_mfcc):
        for j in range(n_mels):
            basis[i, j] = math.cos((j + 0.5) * i * scale)
    return basis


def compute_simple_speaker_signature(audio: np.ndarray, sample_rate: int) -> Optional[np.ndarray]:
    if np is None or audio.size < max(1, int(sample_rate * 0.18)):
        return None

    audio = audio.astype(np.float32)
    abs_audio = np.abs(audio)
    chunk_count = 8
    chunk_size = max(1, audio.shape[0] // chunk_count)
    chunk_means = []
    chunk_stds = []
    for index in range(chunk_count):
        start = index * chunk_size
        end = audio.shape[0] if index == chunk_count - 1 else min(audio.shape[0], start + chunk_size)
        chunk = audio[start:end]
        if chunk.size == 0:
            chunk = audio[-chunk_size:]
        chunk_means.append(float(np.mean(np.abs(chunk))))
        chunk_stds.append(float(np.std(chunk)))

    coarse = audio
    if coarse.shape[0] > 4096:
        coarse = coarse[:4096]
    spectrum = np.abs(np.fft.rfft(coarse, n=1024)).astype(np.float32)
    if spectrum.size == 0:
        return None
    band_count = 6
    band_edges = np.linspace(0, spectrum.shape[0], band_count + 1, dtype=int)
    band_energies = []
    for start, end in zip(band_edges[:-1], band_edges[1:]):
        band = spectrum[start:end]
        band_energies.append(float(np.mean(band)) if band.size else 0.0)

    vector = np.array(
        [
            float(np.mean(abs_audio)),
            float(np.std(audio)),
            float(np.max(audio) - np.min(audio)),
            float(np.mean(np.abs(np.diff(audio)))) if audio.shape[0] > 1 else 0.0,
            float(np.mean(np.abs(np.diff(np.sign(audio))))) if audio.shape[0] > 1 else 0.0,
            float(np.percentile(abs_audio, 75)),
            float(np.percentile(abs_audio, 95)),
            float(audio.shape[0] / float(sample_rate)),
            *chunk_means,
            *chunk_stds,
            *band_energies,
        ],
        dtype=np.float32,
    )
    norm = float(np.linalg.norm(vector))
    if norm <= 1e-6 or math.isnan(norm):
        return None
    return vector / norm


def compute_speaker_signature(audio_path: Path) -> Optional[np.ndarray]:
    if np is None:
        return None
    audio, sample_rate = read_wave_mono(audio_path)
    audio, sample_rate = resample_audio(audio, sample_rate, 16000)
    if audio.size < sample_rate * 0.25:
        return None

    edge_threshold = max(0.0035, float(np.percentile(np.abs(audio), 60)) * 0.25)
    active = np.where(np.abs(audio) >= edge_threshold)[0]
    if active.size > 0:
        start = max(0, int(active[0]) - int(0.05 * sample_rate))
        end = min(audio.shape[0], int(active[-1]) + int(0.05 * sample_rate))
        audio = audio[start:end]
    if audio.size < sample_rate * 0.2:
        return None

    simple_signature = compute_simple_speaker_signature(audio, sample_rate)

    audio = audio - float(np.mean(audio))
    audio = np.append(audio[:1], audio[1:] - 0.97 * audio[:-1]).astype(np.float32)

    frame_length = int(0.025 * sample_rate)
    hop_length = int(0.01 * sample_rate)
    n_fft = 512
    n_mels = 26
    n_mfcc = 13
    window = np.hamming(frame_length).astype(np.float32)
    mel_filters = build_mel_filterbank(sample_rate, n_fft, n_mels)
    dct_basis = build_dct_basis(n_mfcc, n_mels)
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sample_rate).astype(np.float32)

    frames = []
    for start in range(0, max(1, audio.shape[0] - frame_length + 1), hop_length):
        frame = audio[start : start + frame_length]
        if frame.shape[0] < frame_length:
            frame = np.pad(frame, (0, frame_length - frame.shape[0]))
        frames.append(frame)
    if not frames:
        return None

    frames_arr = np.stack(frames).astype(np.float32)
    rms = np.sqrt(np.mean(np.square(frames_arr), axis=1))
    voiced_threshold = max(0.004, float(np.percentile(rms, 35)))
    voiced_mask = rms >= voiced_threshold
    if np.count_nonzero(voiced_mask) < max(3, int(frames_arr.shape[0] * 0.18)):
        voiced_mask = rms >= max(0.0025, float(np.mean(rms)) * 0.85)
    voiced_frames = frames_arr[voiced_mask]
    if voiced_frames.size == 0:
        voiced_frames = frames_arr

    windowed = voiced_frames * window[None, :]
    spectrum = np.abs(np.fft.rfft(windowed, n=n_fft, axis=1)).astype(np.float32)
    power = np.square(spectrum)
    mel_energy = np.maximum(power @ mel_filters.T, 1e-6)
    log_mel = np.log(mel_energy)
    mfcc = log_mel @ dct_basis.T
    mfcc = mfcc[:, 1:13]

    centroid = np.sum(spectrum * freqs[None, :], axis=1) / np.maximum(np.sum(spectrum, axis=1), 1e-6)
    flatness = np.exp(np.mean(np.log(np.maximum(spectrum, 1e-6)), axis=1)) / np.maximum(np.mean(spectrum, axis=1), 1e-6)
    zcr = np.mean(np.abs(np.diff(np.sign(voiced_frames), axis=1)), axis=1)

    vector = np.concatenate(
        [
            np.mean(mfcc, axis=0),
            np.std(mfcc, axis=0),
            np.array(
                [
                    float(np.mean(centroid)),
                    float(np.std(centroid)),
                    float(np.mean(flatness)),
                    float(np.std(flatness)),
                    float(np.mean(zcr)),
                    float(np.std(zcr)),
                ],
                dtype=np.float32,
            ),
        ]
    ).astype(np.float32)

    norm = float(np.linalg.norm(vector))
    if norm <= 1e-6:
        return simple_signature
    return vector / norm


def compare_speaker_similarity(audio_path: Path, profile: dict) -> Optional[float]:
    candidate = compute_speaker_signature(audio_path)
    if candidate is None:
        return None
    reference = np.array(profile.get("signature") or [], dtype=np.float32)
    if reference.size == 0:
        return None
    ref_norm = float(np.linalg.norm(reference))
    if ref_norm <= 1e-6:
        return None
    reference = reference / ref_norm
    return float(np.dot(candidate, reference))


def combine_speaker_signatures(signatures: list[np.ndarray]) -> Optional[np.ndarray]:
    if not signatures:
        return None
    lengths = [int(sig.shape[0]) for sig in signatures if getattr(sig, "shape", None)]
    if not lengths:
        return None
    target_len = max(set(lengths), key=lengths.count)
    normalized = []
    for sig in signatures:
        if sig.shape[0] == target_len:
            normalized.append(sig.astype(np.float32))
        elif sig.shape[0] > target_len:
            normalized.append(sig[:target_len].astype(np.float32))
        else:
            padded = np.zeros(target_len, dtype=np.float32)
            padded[: sig.shape[0]] = sig.astype(np.float32)
            normalized.append(padded)
    merged = np.mean(np.stack(normalized), axis=0).astype(np.float32)
    norm = float(np.linalg.norm(merged))
    if norm <= 1e-6:
        return None
    return merged / norm


def effective_capture_backend(args: argparse.Namespace) -> str:
    if args.capture_backend == "python":
        return "python"
    if args.capture_backend == "swift":
        return "swift"
    if sd is not None and webrtcvad is not None and np is not None:
        return "python"
    return "swift"


def preferred_fallback_voice_ids(*voice_ids: str) -> list[str]:
    candidates = [*voice_ids, "male_0004_a", "male_0018_a", "child_0001_a"]
    unique = []
    for voice_id in candidates:
        voice_id = str(voice_id or "").strip()
        if voice_id and voice_id not in unique:
            unique.append(voice_id)
    return unique


def ensure_mic_binary(debug: bool) -> Path:
    if not MIC_SOURCE.exists():
        raise SystemExit(f"Mic capture source not found: {MIC_SOURCE}")
    needs_build = not MIC_BINARY.exists() or MIC_BINARY.stat().st_mtime < MIC_SOURCE.stat().st_mtime
    if needs_build:
        if debug:
            print_status(f"[build] compiling {MIC_SOURCE.name}")
        command = [
            "swiftc",
            "-O",
            str(MIC_SOURCE),
            "-o",
            str(MIC_BINARY),
            "-framework",
            "AVFoundation",
        ]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "swiftc failed")
    return MIC_BINARY


def rms_db(frame_bytes: bytes) -> float:
    samples = np.frombuffer(frame_bytes, dtype=np.int16).astype(np.float32)
    if samples.size == 0:
        return -120.0
    rms = float(np.sqrt(np.mean(np.square(samples))))
    if rms <= 0:
        return -120.0
    return 20.0 * math.log10(rms / 32768.0)


def write_wav(audio_path: Path, frames: list[bytes], sample_rate: int) -> None:
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(audio_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))


def capture_utterance_python(args: argparse.Namespace, audio_path: Path) -> dict:
    if sd is None or webrtcvad is None or np is None:
        raise RuntimeError("Python capture backend requires numpy, sounddevice, and webrtcvad.")

    sample_rate = int(args.sample_rate)
    frame_ms = int(args.frame_ms)
    frame_samples = sample_rate * frame_ms // 1000
    if frame_samples <= 0:
        raise RuntimeError("Invalid frame size.")

    vad = webrtcvad.Vad(args.vad_mode)
    padding_frames = max(1, int(args.padding_ms / frame_ms))
    silence_frames = max(1, int(args.silence_seconds * 1000 / frame_ms))
    min_speech_frames = max(1, int(math.ceil(args.min_speech_seconds * 1000 / frame_ms)))
    max_wait_frames = max(1, int(args.max_wait_seconds * 1000 / frame_ms))
    max_record_frames = max(1, int(args.max_record_seconds * 1000 / frame_ms))

    preroll = collections.deque(maxlen=padding_frames)
    captured_frames: list[bytes] = []
    speech_started = False
    speech_frames = 0
    consecutive_speech = 0
    silence_run = 0
    stop_reason = "wait_timeout"

    def frame_generator():
        with sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=frame_samples,
            channels=1,
            dtype="int16",
        ) as stream:
            for _ in range(max_wait_frames + max_record_frames + padding_frames + 5):
                data, overflowed = stream.read(frame_samples)
                if overflowed and args.debug:
                    print_status("[listen] input overflowed once")
                yield bytes(data)

    for idx, frame in enumerate(frame_generator(), start=1):
        level_db = rms_db(frame)
        is_speech = False
        try:
            is_speech = vad.is_speech(frame, sample_rate) and level_db >= args.speech_threshold_db
        except Exception:
            is_speech = level_db >= args.speech_threshold_db

        if not speech_started:
            preroll.append(frame)
            if is_speech:
                consecutive_speech += 1
            else:
                consecutive_speech = 0

            if consecutive_speech >= 2:
                speech_started = True
                stop_reason = "silence"
                captured_frames.extend(list(preroll))
                speech_frames += consecutive_speech
                silence_run = 0
                continue

            if idx >= max_wait_frames:
                return {
                    "status": "no_speech",
                    "error": "No speech detected.",
                    "returncode": 2,
                }
            continue

        captured_frames.append(frame)
        if is_speech:
            speech_frames += 1
            silence_run = 0
        else:
            silence_run += 1

        if speech_frames >= min_speech_frames and silence_run >= silence_frames:
            stop_reason = "silence"
            break
        if len(captured_frames) >= max_record_frames:
            stop_reason = "max_record"
            break

    if not captured_frames:
        return {
            "status": "no_speech",
            "error": "No speech detected.",
            "returncode": 2,
        }

    write_wav(audio_path, captured_frames, sample_rate)
    size = audio_path.stat().st_size
    duration_seconds = len(captured_frames) * frame_samples / sample_rate
    return {
        "status": "ok",
        "path": str(audio_path),
        "duration_seconds": duration_seconds,
        "size_bytes": size,
        "speech_detected": True,
        "stop_reason": stop_reason,
        "backend": "python",
        "returncode": 0,
    }


def detect_interrupt_speech(args: argparse.Namespace, *, timeout_seconds: float = 0.0) -> bool:
    if sd is None or webrtcvad is None or np is None:
        return False

    sample_rate = int(args.sample_rate)
    frame_ms = int(args.frame_ms)
    frame_samples = sample_rate * frame_ms // 1000
    vad = webrtcvad.Vad(args.vad_mode)
    consecutive = 0
    required = max(2, int(math.ceil(max(0.04, args.interrupt_min_speech_seconds) * 1000 / frame_ms)))
    threshold_db = max(float(args.interrupt_speech_threshold_db), float(args.speech_threshold_db))
    if timeout_seconds <= 0:
        timeout_seconds = args.max_record_seconds
    max_frames = max(1, int(timeout_seconds * 1000 / frame_ms))

    try:
        with sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=frame_samples,
            channels=1,
            dtype="int16",
        ) as stream:
            for _ in range(max_frames):
                data, overflowed = stream.read(frame_samples)
                if overflowed and args.debug:
                    print_status("[interrupt] input overflowed once")
                frame = bytes(data)
                level_db = rms_db(frame)
                try:
                    is_speech = vad.is_speech(frame, sample_rate) and level_db >= threshold_db
                except Exception:
                    is_speech = level_db >= threshold_db
                if is_speech:
                    consecutive += 1
                    if consecutive >= required:
                        return True
                else:
                    consecutive = 0
    except Exception as exc:
        if args.debug:
            print_status(f"[interrupt] monitor unavailable: {exc}")
    return False


def capture_utterance(args: argparse.Namespace, audio_path: Path) -> dict:
    if args.capture_backend in {"auto", "python"} and sd is not None and webrtcvad is not None and np is not None:
        try:
            return capture_utterance_python(args, audio_path)
        except Exception as exc:
            if args.capture_backend == "python":
                raise
            if args.debug:
                print_status(f"[listen] python backend failed, fallback to swift: {exc}")

    mic_binary = ensure_mic_binary(args.debug)
    command = [
        str(mic_binary),
        "--output",
        str(audio_path),
        "--sample-rate",
        str(args.sample_rate),
        "--max-wait-seconds",
        str(args.max_wait_seconds),
        "--max-record-seconds",
        str(args.max_record_seconds),
        "--silence-seconds",
        str(args.silence_seconds),
        "--min-speech-seconds",
        str(args.min_speech_seconds),
        "--speech-threshold-db",
        str(args.speech_threshold_db),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    stdout = (completed.stdout or "").strip()
    if not stdout:
        raise RuntimeError(completed.stderr.strip() or "Mic capture returned no output.")
    payload = json.loads(stdout)
    payload["returncode"] = completed.returncode
    if args.debug and completed.stderr:
        print_status(f"[mic stderr] {completed.stderr.strip()}")
    return payload


def transcribe(audio_path: Path, args: argparse.Namespace, *, model_override: str = "") -> str:
    api_key = resolve_api_key("asr")
    result = local_asr_transcribe(
        ASRRequest(
            audio_path=audio_path,
            model=model_override or args.asr_model,
            response_format="json",
        ),
        api_key,
    )
    return str(result.transcript or "").strip()


def trim_context_text(text: str, *, limit: int = 120) -> str:
    compact = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(compact) <= limit:
        return compact
    return compact[: max(0, limit - 1)].rstrip() + "…"


def normalize_for_echo_compare(text: str) -> str:
    normalized = str(text or "").lower()
    normalized = re.sub(r"[`*_>#|\-\[\]\(\)~]", " ", normalized)
    normalized = re.sub(r"\s+", "", normalized)
    return normalized.strip()


def transcript_looks_like_recent_echo(text: str, conversation_state: Optional[dict]) -> bool:
    raw = str(text or "").strip()
    if not raw:
        return False
    state = conversation_state or {}
    recent_reply_at = float(state.get("last_reply_finished_at") or 0.0)
    if recent_reply_at <= 0 or (time.time() - recent_reply_at) > 6.0:
        return False
    last_spoken = str(state.get("last_spoken_text") or "").strip()
    if not last_spoken:
        return False
    current = normalize_for_echo_compare(raw)
    previous = normalize_for_echo_compare(last_spoken)
    if len(current) < 24 or len(previous) < 24:
        return False
    ratio = difflib.SequenceMatcher(None, current[:4000], previous[:4000]).ratio()
    if ratio >= 0.72:
        return True
    if len(current) >= 40 and current in previous:
        return True
    if len(previous) >= 40 and previous in current:
        return True
    return False


def extract_json_object(text: str) -> Optional[dict]:
    raw = str(text or "").strip()
    if not raw:
        return None
    candidates = [raw]
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", raw, flags=re.DOTALL)
    candidates.extend(fenced)
    brace_match = re.search(r"(\{.*\})", raw, flags=re.DOTALL)
    if brace_match:
        candidates.append(brace_match.group(1))
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except Exception:
            continue
        if isinstance(payload, dict):
            return payload
    return None


def build_agent_message(text: str, args: argparse.Namespace, conversation_state: Optional[dict] = None) -> str:
    style_prompt = str(args.spoken_style_prompt or "").strip()
    parts: list[str] = []
    if style_prompt:
        parts.append(style_prompt)

    if conversation_state and conversation_state.get("pending_interruption_context"):
        previous_user = trim_context_text(conversation_state.get("last_user_text") or "")
        previous_reply = trim_context_text(conversation_state.get("last_agent_reply_text") or "")
        interruption_hint = (
            "补充上下文：上一轮你的语音播报到一半被用户打断了。"
            "请优先把这次用户的新话当作接话来理解；如果明显是在换新问题，就直接切换，不要重复上一轮的开场和铺垫。"
        )
        if previous_user:
            interruption_hint += f" 上一轮用户刚刚说的是：{previous_user}。"
        if previous_reply:
            interruption_hint += f" 你上一轮正在说的是：{previous_reply}。"
        parts.append(interruption_hint)

    parts.append(f"用户刚刚口头说：{text}")
    return "\n\n".join(part for part in parts if part)


def normalize_reply_for_speech(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_lines: list[str] = []
    for line in lines:
        line = re.sub(r"^#{1,6}\s*", "", line)
        line = re.sub(r"^\s*[-*•]+\s*", "", line)
        line = re.sub(r"^\s*\d+\.\s*", "", line)
        line = line.replace("`", "")
        cleaned_lines.append(line.strip())

    if not cleaned_lines:
        return text.strip()

    merged = "。".join(line for line in cleaned_lines if line)
    merged = re.sub(r"[ \t]+", " ", merged)
    merged = re.sub(r"。{2,}", "。", merged)
    merged = merged.replace("：。", "：")
    merged = re.sub(r"\s*([。！？；，、])\s*", r"\1", merged)
    return merged.strip()


def extract_agent_reply(output: str) -> str:
    clean = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", output)
    lines = [line.rstrip() for line in clean.splitlines() if line.strip()]
    for index in range(len(lines) - 1, -1, -1):
        line = lines[index]
        if line.startswith("🦞 "):
            first_line = line[2:].strip()
            tail = lines[index + 1 :]
            return "\n".join([first_line] + tail).strip()
    for index in range(len(lines) - 1, -1, -1):
        line = lines[index]
        if "Response:" in line:
            first_line = line.split("Response:", 1)[1].strip()
            tail = lines[index + 1 :]
            return "\n".join([first_line] + tail).strip()
    if lines:
        return lines[-1].strip()
    return ""


def summarize_agent_error(stderr: str, stdout: str) -> str:
    combined = "\n".join(part for part in [stderr.strip(), stdout.strip()] if part.strip())
    if not combined:
        return "audioclaw agent failed"
    lines = [line.strip() for line in combined.splitlines() if line.strip()]
    meaningful = [
        line for line in lines
        if "invalid skill from workspace" not in line
        and "invalid skill from builtin" not in line
        and not line.startswith("Usage:")
        and not line.startswith("Flags:")
        and "agent [flags]" not in line
        and "help for agent" not in line
        and not line.startswith("-")
    ]
    if meaningful:
        return meaningful[-1]
    return lines[-1]


def is_transient_agent_error(message: str) -> bool:
    lowered = message.lower()
    transient_markers = [
        "unexpected eof",
        "failed to parse json response",
        "failed to decode response",
        "llm call failed after retries",
        "connection reset by peer",
        "timeout",
        "temporarily unavailable",
    ]
    return any(marker in lowered for marker in transient_markers)


def ask_agent(text: str, args: argparse.Namespace, conversation_state: Optional[dict] = None) -> str:
    message = build_agent_message(text, args, conversation_state)
    command = [
        str(Path(args.agent_bin).expanduser()),
        "agent",
        "--session",
        args.session,
        "--message",
        message,
    ]
    last_error = "audioclaw agent failed"

    for attempt in range(1, max(1, args.agent_retries) + 1):
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode == 0:
            reply = extract_agent_reply(completed.stdout)
            if reply:
                return reply
            last_error = "Could not extract agent reply from CLI output."
        else:
            last_error = summarize_agent_error(completed.stderr, completed.stdout)

        if attempt < max(1, args.agent_retries) and is_transient_agent_error(last_error):
            if args.debug:
                print_status(f"[agent] transient failure, retry {attempt}/{args.agent_retries}: {last_error}")
            time.sleep(max(0.0, args.agent_retry_delay_seconds))
            continue
        break

    raise RuntimeError(last_error)


def looks_like_voice_control(text: str) -> bool:
    normalized = normalize_wake_phrase(text)
    cues = (
        "音色",
        "声音",
        "男声",
        "女声",
        "女生",
        "女性",
        "御姐",
        "温柔",
        "青年",
        "青叔",
        "萌娃",
        "小孩",
        "台妹",
        "克隆音色",
        "换个",
        "切到",
        "切换",
        "改成",
        "换成",
    )
    return any(token in normalized for token in cues)


def resolve_voice_change_with_agent(text: str, args: argparse.Namespace, clone_data: dict) -> Optional[dict]:
    voices = all_voices(clone_data)
    options = []
    for voice in voices[:40]:
        voice_id = str(voice.get("voice_id") or "").strip()
        name = str(voice.get("name") or "").strip()
        if voice_id:
            options.append(f"{name}:{voice_id}" if name else voice_id)
    prompt = (
        "你是一个语音助手音色路由器。"
        "请根据用户这句中文口语，判断他是不是想切换语音音色。"
        "如果是，请从给定候选里选一个最合适的 voice_id。"
        "如果不是，返回 none。"
        "只返回单行 JSON，不要解释。"
        '格式必须是 {"action":"switch","voice_id":"...","reason":"..."} '
        '或者 {"action":"none"}。'
        f"\n候选音色：{'; '.join(options)}"
        f"\n用户原话：{text}"
    )
    command = [
        str(Path(args.agent_bin).expanduser()),
        "agent",
        "--session",
        f"{args.session}:voice_router",
        "--message",
        prompt,
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return None
    payload = extract_json_object(extract_agent_reply(completed.stdout) or completed.stdout)
    if not payload:
        return None
    if str(payload.get("action") or "").strip().lower() != "switch":
        return None
    voice_id = str(payload.get("voice_id") or "").strip()
    if not voice_id:
        return None
    voice = find_voice(voice_id, clone_data)
    if voice:
        return voice
    if voice_id.startswith("vc-"):
        return {"voice_id": voice_id, "name": "Cloned Voice", "source": "agent_clone"}
    return None


def validate_voice_choice(args: argparse.Namespace, voice_id: str) -> Optional[str]:
    if args.tts_mode != "senseaudio":
        return None
    cached = get_cached_tts_validation(voice_id)
    if cached is not None:
        if bool(cached.get("ok")):
            return None
        return str(cached.get("error") or "cached validation failed")
    try:
        api_key = resolve_api_key("tts")
        local_tts_synthesize(
            api_key=api_key,
            text="收到",
            voice_id=voice_id,
            speed=float(args.tts_speed),
            timeout=30,
        )
        remember_tts_validation(voice_id, None)
        return None
    except Exception as exc:
        error = str(exc)
        remember_tts_validation(voice_id, error)
        return error


def pick_working_voice(args: argparse.Namespace, requested_voice_id: str) -> tuple[Optional[str], Optional[str]]:
    failures = []
    for voice_id in preferred_fallback_voice_ids(requested_voice_id, args.voice_id):
        error = validate_voice_choice(args, voice_id)
        if error is None:
            return voice_id, None
        failures.append(f"{voice_id}: {error}")
    return None, failures[-1] if failures else "No working voice found."


def run_startup_self_check(args: argparse.Namespace) -> dict:
    report = {
        "python": sys.executable,
        "capture_backend": effective_capture_backend(args),
        "warnings": [],
        "fatal_errors": [],
    }

    if not Path(args.agent_bin).exists():
        report["fatal_errors"].append(f"AudioClaw CLI 不存在：{args.agent_bin}")

    if report["capture_backend"] == "python":
        missing = []
        if np is None:
            missing.append("numpy")
        if sd is None:
            missing.append("sounddevice")
        if webrtcvad is None:
            missing.append("webrtcvad")
        if missing:
            report["fatal_errors"].append(f"Python 录音后端缺少依赖：{', '.join(missing)}")
    elif not MIC_SOURCE.exists():
        report["fatal_errors"].append(f"Swift 录音器源码不存在：{MIC_SOURCE}")

    try:
        resolve_api_key("asr")
    except Exception as exc:
        report["fatal_errors"].append(f"ASR API key 不可用：{exc}")

    if args.tts_mode == "senseaudio":
        try:
            resolve_api_key("tts")
        except Exception as exc:
            report["fatal_errors"].append(f"TTS API key 不可用：{exc}")
        else:
            working_voice_id, voice_error = pick_working_voice(args, args.voice_id)
            if working_voice_id and working_voice_id != args.voice_id:
                clone_data = load_voice_catalog()
                report["warnings"].append(
                    f"当前音色 {describe_voice(args.voice_id, clone_data)} 不可用，已自动切到 {describe_voice(working_voice_id, clone_data)}。"
                )
                args.voice_id = working_voice_id
            elif not working_voice_id and voice_error:
                report["warnings"].append(f"当前音色暂时不可用：{voice_error}")
        if getattr(args, "senseaudio_streaming_tts", False) and sd is None:
            report["warnings"].append("流式 TTS 已开启，但 sounddevice 不可用，运行时会自动回退到整段播报。")
        if (
            getattr(args, "senseaudio_streaming_tts", False)
            and getattr(args, "senseaudio_streaming_backend", "auto") in {"auto", "miniaudio"}
            and miniaudio is None
        ):
            report["warnings"].append("未检测到 miniaudio，流式 TTS 会回退到 PCM 直放。可选安装：python3 -m pip install --user miniaudio")

    if args.speaker_verification_backend == "wespeaker":
        if not Path(args.wespeaker_python).exists():
            report["fatal_errors"].append(
                f"WeSpeaker Python 不存在：{args.wespeaker_python}。请先按指南准备用户级环境：{WESPEAKER_GUIDE_PATH}"
            )
        if not Path(args.wespeaker_service_script).exists():
            report["fatal_errors"].append(f"WeSpeaker service 脚本不存在：{args.wespeaker_service_script}")
        if not report["fatal_errors"]:
            try:
                status = ensure_wespeaker_service(args, autostart=True, timeout=90.0)
                profile = wespeaker_profile_status(args, "default")
                sample_count = int(profile.get("sample_count") or 0)
                if sample_count > 0:
                    report["warnings"].append(f"WeSpeaker 已就绪，当前已录入 {sample_count} 段声音样本。")
                else:
                    report["warnings"].append(
                        f"WeSpeaker 已就绪，但还没有可用声音档案。可以说“录入我的声音”开始建档。"
                    )
                if status and status.get("model"):
                    report["warnings"].append(f"WeSpeaker 后台模型已预热：{status['model']}")
            except Exception as exc:
                report["fatal_errors"].append(f"WeSpeaker 后台服务不可用：{exc}")

    return report


def wait_for_playback_or_interrupt(proc: subprocess.Popen, args: argparse.Namespace) -> bool:
    if not args.interrupt_playback:
        proc.wait()
        return False

    interrupted = False
    stop_event = threading.Event()

    def monitor() -> None:
        nonlocal interrupted
        if args.interrupt_grace_seconds > 0:
            time.sleep(max(0.0, args.interrupt_grace_seconds))
            if proc.poll() is not None:
                return
        if detect_interrupt_speech(args, timeout_seconds=args.max_record_seconds):
            interrupted = True
            stop_event.set()

    watcher = threading.Thread(target=monitor, daemon=True)
    watcher.start()

    while proc.poll() is None:
        if stop_event.is_set():
            try:
                proc.terminate()
            except Exception:
                pass
            break
        time.sleep(0.05)

    try:
        proc.wait(timeout=1)
    except Exception:
        pass
    return interrupted


class SenseAudioChunkSource(miniaudio.StreamableSource if miniaudio is not None else object):  # type: ignore[misc]
    def __init__(self) -> None:
        self._buffer = bytearray()
        self._lock = threading.Lock()
        self._finished = False
        self._closed = False

    def feed(self, chunk: bytes) -> None:
        if not chunk:
            return
        with self._lock:
            self._buffer.extend(chunk)

    def finish(self) -> None:
        self._finished = True

    def read(self, num_bytes: int) -> bytes:
        while True:
            if self._closed:
                return b""
            with self._lock:
                if self._buffer:
                    take = min(num_bytes, len(self._buffer))
                    chunk = bytes(self._buffer[:take])
                    del self._buffer[:take]
                    return chunk
                finished = self._finished
            if finished:
                return b""
            time.sleep(0.01)

    def close(self) -> None:
        self._closed = True
        self._finished = True


def select_streaming_backend(args: argparse.Namespace) -> str:
    configured = str(getattr(args, "senseaudio_streaming_backend", "auto") or "auto").strip().lower()
    if configured == "miniaudio":
        return "miniaudio" if miniaudio is not None else "pcm"
    if configured == "pcm":
        return "pcm"
    if miniaudio is not None:
        return "miniaudio"
    return "pcm"


def speak_streaming_senseaudio_miniaudio(spoken_text: str, args: argparse.Namespace) -> bool:
    if miniaudio is None:
        raise RuntimeError("miniaudio 不可用，无法启用 MP3 流式解码。")

    api_key = resolve_api_key("tts")
    last_error: Optional[Exception] = None

    for candidate_voice_id in preferred_fallback_voice_ids(args.voice_id):
        stop_event = threading.Event()
        interrupted = False
        first_chunk_at: Optional[float] = None
        chunk_count = 0
        stream_started_at = time.time()
        source = SenseAudioChunkSource()
        producer_error: list[Exception] = []

        def monitor() -> None:
            nonlocal interrupted
            if not args.interrupt_playback:
                return
            if args.interrupt_grace_seconds > 0:
                time.sleep(max(0.0, args.interrupt_grace_seconds))
                if stop_event.is_set():
                    return
            if detect_interrupt_speech(args, timeout_seconds=args.max_record_seconds):
                interrupted = True
                stop_event.set()
                source.close()

        def producer() -> None:
            nonlocal first_chunk_at, chunk_count
            try:
                def on_chunk(chunk: bytes) -> None:
                    nonlocal first_chunk_at, chunk_count
                    if stop_event.is_set():
                        raise StreamingPlaybackInterrupted()
                    if not chunk:
                        return
                    if first_chunk_at is None:
                        first_chunk_at = time.time()
                    chunk_count += 1
                    source.feed(chunk)

                result = local_tts_stream_synthesize(
                    api_key=api_key,
                    text=spoken_text,
                    voice_id=candidate_voice_id,
                    audio_format="mp3",
                    sample_rate=32000,
                    speed=float(args.tts_speed),
                    on_chunk=on_chunk,
                )
                if chunk_count == 0 and result.audio_bytes and not stop_event.is_set():
                    source.feed(result.audio_bytes)
            except StreamingPlaybackInterrupted:
                pass
            except Exception as exc:
                producer_error.append(exc)
            finally:
                source.finish()

        watcher = threading.Thread(target=monitor, daemon=True)
        producer_thread = threading.Thread(target=producer, daemon=True)
        watcher.start()
        producer_thread.start()

        try:
            with miniaudio.PlaybackDevice(
                output_format=miniaudio.SampleFormat.SIGNED16,
                nchannels=2,
                sample_rate=32000,
                buffersize_msec=80,
                app_name="AudioClaw",
            ) as device:
                stream = miniaudio.stream_any(
                    source,
                    source_format=miniaudio.FileFormat.MP3,
                    output_format=miniaudio.SampleFormat.SIGNED16,
                    nchannels=2,
                    sample_rate=32000,
                    frames_to_read=1024,
                )
                device.start(stream)
                while True:
                    if stop_event.is_set():
                        device.stop()
                        raise StreamingPlaybackInterrupted()
                    if producer_error:
                        device.stop()
                        raise producer_error[0]
                    if not producer_thread.is_alive() and device.callback_generator is None:
                        break
                    time.sleep(0.03)
        except StreamingPlaybackInterrupted:
            source.close()
            producer_thread.join(timeout=0.5)
            watcher.join(timeout=0.2)
            return True
        except Exception as exc:
            last_error = exc
            stop_event.set()
            source.close()
            producer_thread.join(timeout=0.5)
            watcher.join(timeout=0.2)
            continue

        stop_event.set()
        producer_thread.join(timeout=0.5)
        watcher.join(timeout=0.2)

        if candidate_voice_id != args.voice_id:
            clone_data = load_voice_catalog()
            print_status(
                f"[tts] 当前音色不可用，已临时回退到 {describe_voice(candidate_voice_id, clone_data)}。"
            )
            args.voice_id = candidate_voice_id
        if args.debug:
            first_chunk_ms = (
                round((first_chunk_at - stream_started_at) * 1000.0, 1)
                if first_chunk_at is not None
                else None
            )
            print_status(
                f"[tts] SenseAudio 流式播报已完成：backend=miniaudio, chunks={chunk_count}"
                + (f"，首包 {first_chunk_ms}ms" if first_chunk_ms is not None else "")
            )
        return interrupted

    raise last_error or RuntimeError("No working voice found for miniaudio streaming TTS.")


def speak_streaming_senseaudio(spoken_text: str, args: argparse.Namespace) -> bool:
    if sd is None:
        raise RuntimeError("sounddevice 不可用，无法启用流式 TTS 播放。")

    api_key = resolve_api_key("tts")
    last_error: Optional[Exception] = None

    for candidate_voice_id in preferred_fallback_voice_ids(args.voice_id):
        stop_event = threading.Event()
        interrupted = False
        first_chunk_at: Optional[float] = None
        chunk_count = 0
        pending_tail = b""
        stream_started_at = time.time()

        def monitor() -> None:
            nonlocal interrupted
            if not args.interrupt_playback:
                return
            if args.interrupt_grace_seconds > 0:
                time.sleep(max(0.0, args.interrupt_grace_seconds))
                if stop_event.is_set():
                    return
            if detect_interrupt_speech(args, timeout_seconds=args.max_record_seconds):
                interrupted = True
                stop_event.set()

        watcher = threading.Thread(target=monitor, daemon=True)
        watcher.start()

        try:
            with sd.RawOutputStream(
                samplerate=32000,
                blocksize=0,
                channels=2,
                dtype="int16",
            ) as stream:
                def on_chunk(chunk: bytes) -> None:
                    nonlocal first_chunk_at, chunk_count, pending_tail
                    if stop_event.is_set():
                        raise StreamingPlaybackInterrupted()
                    if not chunk:
                        return
                    if first_chunk_at is None:
                        first_chunk_at = time.time()
                    chunk_count += 1
                    payload = pending_tail + chunk
                    remainder = len(payload) % 4
                    if remainder:
                        pending_tail = payload[-remainder:]
                        payload = payload[:-remainder]
                    else:
                        pending_tail = b""
                    if payload:
                        stream.write(payload)
                    if stop_event.is_set():
                        raise StreamingPlaybackInterrupted()

                result = local_tts_stream_synthesize(
                    api_key=api_key,
                    text=spoken_text,
                    voice_id=candidate_voice_id,
                    audio_format="pcm",
                    sample_rate=32000,
                    speed=float(args.tts_speed),
                    on_chunk=on_chunk,
                )

                if chunk_count == 0 and result.audio_bytes and not stop_event.is_set():
                    payload = pending_tail + result.audio_bytes
                    remainder = len(payload) % 4
                    if remainder:
                        payload += b"\x00" * (4 - remainder)
                    stream.write(payload)
                    pending_tail = b""
                if pending_tail and not stop_event.is_set():
                    payload = pending_tail
                    remainder = len(payload) % 4
                    if remainder:
                        payload += b"\x00" * (4 - remainder)
                    stream.write(payload)
                    pending_tail = b""
        except StreamingPlaybackInterrupted:
            return True
        except Exception as exc:
            last_error = exc
            stop_event.set()
            watcher.join(timeout=0.2)
            continue

        stop_event.set()
        watcher.join(timeout=0.2)

        if candidate_voice_id != args.voice_id:
            clone_data = load_voice_catalog()
            print_status(
                f"[tts] 当前音色不可用，已临时回退到 {describe_voice(candidate_voice_id, clone_data)}。"
            )
            args.voice_id = candidate_voice_id
        if args.debug:
            first_chunk_ms = (
                round((first_chunk_at - stream_started_at) * 1000.0, 1)
                if first_chunk_at is not None
                else None
            )
            print_status(
                f"[tts] SenseAudio 流式播报已完成：chunks={chunk_count}"
                + (f"，首包 {first_chunk_ms}ms" if first_chunk_ms is not None else "")
            )
        return interrupted

    raise last_error or RuntimeError("No working voice found for streaming TTS.")


def speak(text: str, args: argparse.Namespace, turn_id: int) -> bool:
    spoken_text = normalize_reply_for_speech(text)
    if args.tts_mode == "none":
        return False
    if args.tts_mode == "say":
        command = ["say"]
        if args.say_voice:
            command.extend(["-v", args.say_voice])
        command.append(spoken_text)
        proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return wait_for_playback_or_interrupt(proc, args)

    if getattr(args, "senseaudio_streaming_tts", False):
        backend = select_streaming_backend(args)
        try:
            if backend == "miniaudio":
                return speak_streaming_senseaudio_miniaudio(spoken_text, args)
            return speak_streaming_senseaudio(spoken_text, args)
        except Exception as exc:
            if args.debug:
                print_status(f"[tts] 流式播报失败（backend={backend}），回退到整段播报：{exc}")

    AUDIO_STATE_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = AUDIO_STATE_DIR / f"voiceclaw_reply_{turn_id:04d}.mp3"
    api_key = resolve_api_key("tts")
    result = None
    used_voice_id = args.voice_id
    last_error = None
    for candidate_voice_id in preferred_fallback_voice_ids(args.voice_id):
        try:
            result = local_tts_synthesize(
                api_key=api_key,
                text=spoken_text,
                voice_id=candidate_voice_id,
                speed=float(args.tts_speed),
            )
            used_voice_id = candidate_voice_id
            break
        except Exception as exc:
            last_error = exc
            continue
    if result is None:
        raise last_error or RuntimeError("No working voice found for current reply.")
    if used_voice_id != args.voice_id:
        clone_data = load_voice_catalog()
        print_status(
            f"[tts] 当前音色不可用，已临时回退到 {describe_voice(used_voice_id, clone_data)}。"
        )
        args.voice_id = used_voice_id
    audio_path.write_bytes(result.audio_bytes)
    proc = subprocess.Popen(
        ["/usr/bin/afplay", str(audio_path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return wait_for_playback_or_interrupt(proc, args)


def should_exit(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized in {"退出", "停止", "结束", "exit", "quit", "stop"}


def normalize_wake_phrase(text: str) -> str:
    return re.sub(r"\s+", "", text.strip().lower())


def strip_spoken_tail(text: str, marker: str) -> str:
    index = text.find(marker)
    if index < 0:
        return ""
    value = text[index + len(marker) :].strip(" ：:，,。!！?？\"'“”")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def should_report_settings(text: str) -> bool:
    normalized = normalize_wake_phrase(text)
    triggers = ("当前设置", "现在什么设置", "我的偏好", "你记住了什么", "当前状态", "现在什么音色", "当前音色")
    return any(token in normalized for token in triggers)


def refresh_wespeaker_status(args: argparse.Namespace, speaker_profile: dict) -> dict:
    if args.speaker_verification_backend != "wespeaker":
        speaker_profile["wespeaker"] = {"enabled": False}
        return speaker_profile["wespeaker"]
    status = wespeaker_health(args, timeout=2.0) or {}
    profile = {}
    with contextlib.suppress(Exception):
        profile = wespeaker_profile_status(args, "default")
    speaker_profile["wespeaker"] = {
        "enabled": True,
        "service_ready": bool(status.get("ok")),
        "model": status.get("model", ""),
        "sample_count": int(profile.get("sample_count") or 0),
        "threshold": float(args.wespeaker_threshold),
    }
    return speaker_profile["wespeaker"]


def should_handle_wespeaker_command(text: str) -> bool:
    normalized = normalize_wake_phrase(text)
    triggers = (
        "wespeaker",
        "录入我的声音",
        "录制我的声音",
        "录我的声音",
        "记录我的声音",
        "重录我的声音",
        "重新录我的声音",
        "取消录入",
        "开始录入",
        "录入吧",
        "开始吧",
        "开启声纹验证",
        "关闭声纹验证",
        "关闭只听我模式",
        "关闭只听我",
        "退出只听我模式",
        "退出只听我",
        "取消只听我模式",
        "取消只听我",
        "不要只听我",
        "别只听我",
        "声纹验证",
        "只听我模式",
        "只听我",
        "停止后台声纹",
        "启动后台声纹",
        "预热声纹",
    )
    return any(token in normalized for token in triggers)


def format_wespeaker_setup_error(exc: Exception) -> str:
    detail = str(exc).strip() or "WeSpeaker 环境不可用"
    return (
        f"WeSpeaker 现在还没法启动：{detail}。"
        f"请先按这个指南准备用户环境：{WESPEAKER_GUIDE_PATH}"
    )


def handle_wespeaker_enrollment(
    audio_path: Path,
    args: argparse.Namespace,
    speaker_profile: dict,
    runtime_flags: dict,
    transcript: str,
) -> str:
    total = int(runtime_flags.get("wespeaker_enroll_total") or 1)
    remaining = int(runtime_flags.get("wespeaker_enroll_remaining") or 0)
    if remaining <= 0:
        return "当前没有待处理的 WeSpeaker 录音任务。"
    normalized = normalize_wake_phrase(transcript)
    control_tokens = {
        "录入吧",
        "开始吧",
        "开始录入",
        "录吧",
        "开始",
        "好",
        "好的",
        "行",
        "可以",
        "嗯",
        "啊",
    }
    if normalized in control_tokens:
        return f"我准备好了。从下一句开始，请直接读这句示例：{WESPEAKER_ENROLL_EXAMPLE}"
    reset = bool(runtime_flags.get("wespeaker_enroll_reset"))
    result = wespeaker_enroll_audio(
        args,
        audio_path,
        profile_name="default",
        reset=reset,
        max_samples=max(1, total),
        timeout=30.0,
    )
    runtime_flags["wespeaker_enroll_reset"] = False
    runtime_flags["wespeaker_enroll_remaining"] = max(0, remaining - 1)
    refresh_wespeaker_status(args, speaker_profile)
    sample_count = int(result.get("sample_count") or 0)
    if runtime_flags["wespeaker_enroll_remaining"] > 0:
        left = int(runtime_flags["wespeaker_enroll_remaining"])
        return f"已记录第 {sample_count} 段声音样本，还需要 {left} 段。请直接再读一遍这句：{WESPEAKER_ENROLL_EXAMPLE}"
    return f"好的，WeSpeaker 声音档案已经录好了。现在一共保存了 {sample_count} 段样本，后面你可以直接继续用。"


def handle_wespeaker_command(
    text: str,
    args: argparse.Namespace,
    speaker_profile: dict,
    runtime_flags: dict,
) -> Optional[str]:
    normalized = normalize_wake_phrase(text)
    if not should_handle_wespeaker_command(text):
        return None

    if "取消录入" in normalized:
        runtime_flags["wespeaker_enroll_remaining"] = 0
        runtime_flags["wespeaker_enroll_reset"] = False
        return "好的，已取消这次 WeSpeaker 声音录入。"

    if any(token in normalized for token in ("停止后台声纹", "关闭后台声纹", "停止wespeaker服务")):
        stopped = stop_wespeaker_service(args)
        refresh_wespeaker_status(args, speaker_profile)
        if stopped:
            return "好的，WeSpeaker 后台服务已经停止。"
        return "WeSpeaker 后台服务当前没有在运行。"

    if any(token in normalized for token in ("启动后台声纹", "预热声纹", "预热wespeaker", "启动wespeaker服务")):
        try:
            ensure_wespeaker_service(args, autostart=True, timeout=90.0)
        except Exception as exc:
            return format_wespeaker_setup_error(exc)
        refresh_wespeaker_status(args, speaker_profile)
        return "好的，WeSpeaker 后台服务已经启动并预热好了。"

    if any(token in normalized for token in ("关闭声纹验证", "关闭只听我模式", "关闭只听我", "退出只听我模式", "退出只听我", "取消只听我模式", "取消只听我", "不要只听我", "别只听我", "关闭wespeaker", "禁用wespeaker")):
        args.speaker_verification_backend = "none"
        save_preferences(args)
        refresh_wespeaker_status(args, speaker_profile)
        return "好的，已经关闭 WeSpeaker 声纹验证，后面不会再按声音过滤指令。"

    if any(token in normalized for token in ("开启声纹验证", "开启wespeaker", "启用wespeaker", "只听我模式", "只听我")):
        args.speaker_verification_backend = "wespeaker"
        try:
            ensure_wespeaker_service(args, autostart=True, timeout=90.0)
        except Exception as exc:
            args.speaker_verification_backend = "none"
            return format_wespeaker_setup_error(exc)
        save_preferences(args)
        status = refresh_wespeaker_status(args, speaker_profile)
        if int(status.get("sample_count") or 0) <= 0:
            return "好的，已经开启 WeSpeaker 声纹验证。现在后台也预热好了，不过你还没录入声音样本。可以直接说“录入我的声音”。"
        return "好的，已经开启 WeSpeaker 声纹验证，后台模型也已经预热好了。"

    if any(token in normalized for token in ("录入我的声音", "录制我的声音", "录我的声音", "记录我的声音", "重录我的声音", "重新录我的声音")):
        args.speaker_verification_backend = "wespeaker"
        try:
            ensure_wespeaker_service(args, autostart=True, timeout=90.0)
        except Exception as exc:
            args.speaker_verification_backend = "none"
            return format_wespeaker_setup_error(exc)
        if "重录" in normalized or "重新录" in normalized:
            wespeaker_clear_profile(args, "default")
        runtime_flags["wespeaker_enroll_total"] = 1
        runtime_flags["wespeaker_enroll_remaining"] = 1
        runtime_flags["wespeaker_enroll_reset"] = True
        save_preferences(args)
        refresh_wespeaker_status(args, speaker_profile)
        return f"好的，接下来只需要录 1 句。从下一句开始，请直接读这句示例：{WESPEAKER_ENROLL_EXAMPLE}"

    if any(token in normalized for token in ("wespeaker状态", "声纹状态", "查看wespeaker状态", "查看声纹状态")):
        if args.speaker_verification_backend != "wespeaker":
            return "当前还没有开启 WeSpeaker 声纹验证。"
        try:
            ensure_wespeaker_service(args, autostart=True, timeout=90.0)
        except Exception as exc:
            return format_wespeaker_setup_error(exc)
        status = refresh_wespeaker_status(args, speaker_profile)
        sample_count = int(status.get("sample_count") or 0)
        return (
            f"当前 WeSpeaker 后台已经就绪，阈值是 {float(args.wespeaker_threshold):.2f}。"
            f"现在保存了 {sample_count} 段声音样本。"
        )

    return None


def should_filter_by_wespeaker(args: argparse.Namespace, speaker_profile: dict) -> bool:
    if args.speaker_verification_backend != "wespeaker":
        return False
    status = refresh_wespeaker_status(args, speaker_profile)
    return bool(status.get("service_ready")) and int(status.get("sample_count") or 0) > 0


def wespeaker_should_accept(audio_path: Path, args: argparse.Namespace, speaker_profile: dict) -> tuple[bool, Optional[str]]:
    if not should_filter_by_wespeaker(args, speaker_profile):
        return True, None
    result = wespeaker_verify_audio(
        args,
        audio_path,
        profile_name="default",
        threshold=float(args.wespeaker_threshold),
        timeout=20.0,
    )
    refresh_wespeaker_status(args, speaker_profile)
    score = float(result.get("score") or 0.0)
    match = bool(result.get("match"))
    if match:
        return True, None
    return False, f"[wespeaker] 本轮声音相似度 {score:.3f}，低于阈值 {float(args.wespeaker_threshold):.2f}，已忽略这条指令。"


def load_voice_catalog() -> dict:
    return load_clone_voices(CLONE_VOICES_PATH)


def describe_voice(voice_id: str, clone_data: dict) -> str:
    voice = find_voice(voice_id, clone_data)
    if not voice:
        return voice_id
    return f"{voice.get('name') or voice_id}（{voice.get('voice_id') or voice_id}）"


def list_voice_brief(clone_data: dict, limit: int = 10) -> str:
    voices = all_voices(clone_data)
    preferred_ids = [
        "male_0004_a",
        "male_0018_a",
        "female_0006_a",
        "male_0027_a",
        "male_0027_b",
        "female_0033_a",
        "child_0001_a",
        "male_0028_a",
    ]
    prioritized = []
    for voice_id in preferred_ids:
        voice = find_voice(voice_id, clone_data)
        if voice and voice not in prioritized:
            prioritized.append(voice)
    for voice in voices:
        if voice not in prioritized:
            prioritized.append(voice)
    items = [
        f"{voice.get('name')}（{voice.get('voice_id')}）"
        for voice in prioritized[:limit]
    ]
    return "你现在可以换这些常用音色：" + "，".join(items) + "。如果你要，我也可以直接帮你切换。"


def extract_voice_query(text: str) -> str:
    patterns = [
        r"^(?:换成|换到|切换到|切到|切成|改成|改用|音色改成|声音改成|换个音色用|换个)\s*([A-Za-z0-9_\-一-龥]+)$",
        r"^(?:用|使用)\s*([A-Za-z0-9_\-一-龥]+)(?:这个)?(?:音色|声音)?$",
        r"^(?:默认音色是|记住默认音色是|以后用|以后都用|默认用)\s*([A-Za-z0-9_\-一-龥]+)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = str(match.group(1) or "").strip()
            value = re.sub(r"(这个)?(音色|声音)$", "", value).strip()
            return value
    return ""


def should_list_voices(text: str) -> bool:
    normalized = normalize_wake_phrase(text)
    triggers = ("列出音色", "有哪些音色", "可用音色", "有什么声音", "音色列表", "有哪些声音")
    return any(token in normalized for token in triggers)


def resolve_voice_change(text: str, clone_data: dict) -> Optional[dict]:
    query = extract_voice_query(text)
    if not query:
        return None
    aliases = {
        "男声": "male_0004_a",
        "默认男声": "male_0004_a",
        "女声": "female_0006_a",
        "女生": "female_0006_a",
        "女性": "female_0006_a",
        "默认女声": "female_0006_a",
        "御姐": "female_0006_a",
        "温柔御姐": "female_0006_a",
        "温柔女声": "female_0006_a",
        "沙哑青年": "male_0018_a",
        "沙哑男声": "male_0018_a",
        "可靠青叔": "male_0028_a",
        "青叔": "male_0028_a",
        "萌娃": "child_0001_a",
        "小孩": "child_0001_a",
        "台妹": "female_0033_a",
    }
    query = aliases.get(query, query)
    if query.startswith("vc-"):
        return {"voice_id": query, "name": "Cloned Voice", "source": "explicit_clone"}
    return find_voice(query, clone_data)


def should_register_clone_voice(text: str) -> bool:
    normalized = normalize_wake_phrase(text)
    return "注册克隆音色" in normalized or "记住克隆音色" in normalized or "添加克隆音色" in normalized


def parse_clone_voice_registration(text: str) -> Optional[dict]:
    match = re.search(
        r"(?:注册克隆音色|记住克隆音色|添加克隆音色)\s*(vc-[A-Za-z0-9_\-]+)(?:\s*(?:叫|名称是|名字是)\s*([A-Za-z0-9_\-一-龥]+))?",
        text,
    )
    if not match:
        return None
    voice_id = str(match.group(1) or "").strip()
    name = str(match.group(2) or "").strip()
    if not voice_id:
        return None
    return {"voice_id": voice_id, "name": name}


def wants_remembered_voice(text: str) -> bool:
    normalized = normalize_wake_phrase(text)
    return any(token in normalized for token in ("记住默认音色", "默认音色", "以后都用", "以后用", "默认用"))


def handle_voice_command(text: str, args: argparse.Namespace) -> Optional[str]:
    clone_data = load_voice_catalog()

    if should_register_clone_voice(text):
        payload = parse_clone_voice_registration(text)
        if not payload:
            return "你可以直接说，比如“注册克隆音色 vc-123456 叫 我的声音”。"
        upsert_clone_voice(clone_data, voice_id=payload["voice_id"], name=payload["name"])
        save_clone_voices(CLONE_VOICES_PATH, clone_data)
        return f"好的，我记住了这个克隆音色：{describe_voice(payload['voice_id'], clone_data)}。后面你可以直接让我切到它。"

    if should_list_voices(text):
        return list_voice_brief(clone_data)

    voice = resolve_voice_change(text, clone_data)
    if not voice:
        normalized = normalize_wake_phrase(text)
        if looks_like_voice_control(text):
            voice = resolve_voice_change_with_agent(text, args, clone_data)
        if voice is None:
            normalized = normalize_wake_phrase(text)
        else:
            normalized = ""
    if not voice:
        if "换音色" in normalized or "换个声音" in normalized or "切换音色" in normalized:
            return list_voice_brief(clone_data)
        return None

    voice_id = str(voice.get("voice_id") or "").strip()
    if not voice_id:
        return None

    if voice_id.startswith("vc-") and not find_voice(voice_id, clone_data):
        upsert_clone_voice(clone_data, voice_id=voice_id, name=str(voice.get("name") or "Cloned Voice"))
        save_clone_voices(CLONE_VOICES_PATH, clone_data)
        clone_data = load_voice_catalog()

    validation_error = validate_voice_choice(args, voice_id)
    if validation_error is not None:
        working_voice_id, _ = pick_working_voice(args, voice_id)
        if working_voice_id and working_voice_id != voice_id:
            args.voice_id = working_voice_id
            return (
                f"{describe_voice(voice_id, clone_data)} 当前不可用。"
                f"我先帮你切到 {describe_voice(working_voice_id, clone_data)}，这样能保证继续正常说话。"
            )
        return f"{describe_voice(voice_id, clone_data)} 当前不可用，我先保留现在这个能正常工作的音色。"

    args.voice_id = voice_id
    if wants_remembered_voice(text):
        save_preferences(args)
        return f"好的，我记住了。以后默认用 {describe_voice(args.voice_id, clone_data)}。"
    return f"好的，这一轮开始我会用 {describe_voice(args.voice_id, clone_data)} 来说话。"


def handle_preference_command(text: str, args: argparse.Namespace) -> Optional[str]:
    normalized = normalize_wake_phrase(text)

    if any(token in normalized for token in ("清除偏好", "重置偏好", "恢复默认", "忘掉偏好")):
        clear_preferences(args)
        return "好的，已清除已记住的偏好，恢复默认设置。"

    if "记住当前偏好" in text or "保存当前偏好" in text:
        save_preferences(args)
        return "好的，我记住了当前偏好。之后启动时会自动加载。"

    if any(token in normalized for token in ("记住不要打断", "以后不要打断", "关闭打断", "别打断我", "不要打断我")):
        args.interrupt_playback = False
        args.interrupt_grace_seconds = max(1.5, float(args.interrupt_grace_seconds))
        args.interrupt_min_speech_seconds = max(0.45, float(args.interrupt_min_speech_seconds))
        args.interrupt_speech_threshold_db = max(-14.0, float(args.interrupt_speech_threshold_db))
        save_preferences(args)
        return "好的，我记住了。以后默认不主动打断播报，打断也会更迟钝一些。"

    if any(token in normalized for token in ("记住多等一下再截断", "记住不要太快截断", "记住说完后多等一下")):
        args.silence_seconds = max(1.8, float(args.silence_seconds))
        save_preferences(args)
        return f"好的，我记住了。以后我会多等一点再判断你说完了，现在是 {args.silence_seconds:.1f} 秒。"

    if any(token in normalized for token in ("记住开启打断", "以后开启打断", "允许打断", "可以打断", "打开打断")):
        args.interrupt_playback = True
        save_preferences(args)
        return "好的，我记住了。以后默认允许你插话打断播报。"

    speed_match = re.search(r"语速(?:调到|改成|设为|用|保持在)?\s*([0-9]+(?:\.[0-9]+)?)", text)
    if ("记住" in text or "以后" in text or "默认" in text) and speed_match:
        speed = max(0.5, min(2.0, float(speed_match.group(1))))
        args.tts_speed = round(speed, 2)
        save_preferences(args)
        return f"好的，我记住了。以后默认语速是 {args.tts_speed:.2f}。"

    if ("记住" in text or "以后" in text) and "唤醒词" in text:
        value = strip_spoken_tail(text, "唤醒词")
        if value:
            args.wake_phrase = value
            save_preferences(args)
            return f"好的，我记住了。以后默认唤醒词是“{args.wake_phrase}”。"

    if ("记住" in text or "以后" in text) and "睡眠词" in text:
        value = strip_spoken_tail(text, "睡眠词")
        if value:
            args.sleep_phrase = value
            save_preferences(args)
            return f"好的，我记住了。以后默认睡眠词是“{args.sleep_phrase}”。"

    if any(token in normalized for token in ("口语一点", "更口语化", "说话自然一点")) and ("记住" in text or "以后" in text):
        args.spoken_style_prompt = DEFAULT_SPOKEN_STYLE_PROMPT
        save_preferences(args)
        return "好的，我记住了。以后我会尽量用更自然、更口语化的方式回答。"

    if any(token in normalized for token in ("更简短一点", "以后简短一点", "记住简短一点", "回答短一点")):
        args.spoken_style_prompt = (
            "你现在正通过本机语音助手直接对用户说话。"
            "请用非常简短、很口语的中文回答。"
            "优先一句话说清楚，必要时最多两句。"
            "不要铺垫，不要复述用户问题，不要念清单。"
        )
        save_preferences(args)
        return "好的，我记住了。以后我会答得更短一点。"

    if any(token in normalized for token in ("展开一点", "详细一点", "以后详细一点", "记住详细一点")):
        args.spoken_style_prompt = (
            "你现在正通过本机语音助手直接对用户说话。"
            "请用自然、口语化的中文回答，先给结论，再补充关键细节。"
            "一般控制在 2 到 4 句，不要用 Markdown 或清单。"
        )
        save_preferences(args)
        return "好的，我记住了。以后我会稍微展开一点说。"

    return None


def extend_wake_window(args: argparse.Namespace, armed_until: float) -> float:
    wake_phrase = str(args.wake_phrase or "").strip()
    if not wake_phrase:
        return armed_until
    refreshed_until = time.time() + max(0.0, float(args.wake_sticky_seconds))
    return max(armed_until, refreshed_until)


def matched_phrase(text: str, phrase: str) -> bool:
    phrase = str(phrase or "").strip()
    if not phrase:
        return False
    return normalize_wake_phrase(phrase) in normalize_wake_phrase(text)


def is_short_filler_utterance(text: str) -> bool:
    normalized = normalize_wake_phrase(text)
    if not normalized:
        return True
    filler_tokens = {
        "啊",
        "嗯",
        "呃",
        "诶",
        "喂",
        "欸",
        "哎",
        "嗨",
        "在吗",
        "听到吗",
        "能听到吗",
        "你好",
    }
    if normalized in filler_tokens:
        return True
    if len(normalized) <= 1:
        return True
    return False


def apply_wake_phrase(transcript: str, args: argparse.Namespace, armed_until: float) -> tuple[bool, str, float, bool]:
    wake_phrase = str(args.wake_phrase or "").strip()
    if not wake_phrase:
        return True, transcript, armed_until, False

    now = time.time()
    normalized_text = normalize_wake_phrase(transcript)
    normalized_wake = normalize_wake_phrase(wake_phrase)

    if now <= armed_until:
        refreshed_until = now + max(0.0, float(args.wake_sticky_seconds))
        if normalized_text == normalized_wake or (
            normalized_text.startswith(normalized_wake)
            and is_short_filler_utterance(normalized_text[len(normalized_wake):])
        ):
            return True, "", refreshed_until, False
        return True, transcript, refreshed_until, False

    if normalized_text == normalized_wake or normalized_text.startswith(normalized_wake):
        pattern = re.escape(wake_phrase)
        cleaned = re.sub(pattern, "", transcript, flags=re.IGNORECASE).strip(" ,，。！!？?：:")
        if is_short_filler_utterance(cleaned):
            cleaned = ""
        return True, cleaned, now + max(0.0, float(args.wake_sticky_seconds)), True

    return False, "", armed_until, False


def should_use_wake_asr(args: argparse.Namespace, armed_until: float) -> bool:
    wake_phrase = str(args.wake_phrase or "").strip()
    if not wake_phrase:
        return False
    return time.time() > armed_until


def format_wake_asr_status(model_name: str) -> str:
    normalized = str(model_name or "").strip().lower()
    if "lite" in normalized or "light" in normalized:
        return f"[asr] 正在用轻量模型识别唤醒词（{model_name}）..."
    return f"[asr] 正在识别唤醒词（{model_name}）..."


def should_sleep(text: str, args: argparse.Namespace) -> bool:
    return matched_phrase(text, str(args.sleep_phrase or "").strip())


def emit_reply(
    reply: str,
    args: argparse.Namespace,
    turn_id: int,
    armed_until: float,
    speaker_profile: dict,
) -> tuple[float, bool]:
    print_status(f"[claw] {reply}")
    save_runtime_state(args, speaker_profile)
    interrupted = False
    try:
        interrupted = speak(reply, args, turn_id)
        armed_until = extend_wake_window(args, armed_until)
        if interrupted:
            play_status_sound("heard", args)
            print_status("[interrupt] 已检测到新语音，已打断当前播报。")
    except Exception as exc:
        armed_until = extend_wake_window(args, armed_until)
        play_status_sound("error", args)
        print_status(f"[tts] 播报失败，已保留文字回复: {exc}")
    return armed_until, interrupted


def main() -> int:
    args = parse_args()
    loaded_preferences = apply_preferences(args)
    speaker_profile = {}
    runtime_flags = {
        "wespeaker_enroll_total": 0,
        "wespeaker_enroll_remaining": 0,
        "wespeaker_enroll_reset": False,
    }
    conversation_state = {
        "last_user_text": "",
        "last_agent_reply_text": "",
        "pending_interruption_context": False,
        "last_reply_finished_at": 0.0,
        "last_spoken_text": "",
    }

    if not Path(args.agent_bin).exists():
        raise SystemExit(f"AudioClaw CLI not found: {args.agent_bin}")

    self_check = {"warnings": [], "fatal_errors": [], "python": sys.executable, "capture_backend": effective_capture_backend(args)}
    if not args.skip_self_check:
        self_check = run_startup_self_check(args)
        print_status(
            f"[startup] 自检完成：Python={self_check['python']}，录音后端={self_check['capture_backend']}，主 ASR={args.asr_model}，休眠唤醒 ASR={args.wake_asr_model}。"
        )
        for warning in self_check["warnings"]:
            print_status(f"[startup] 提示：{warning}")
        if self_check["fatal_errors"]:
            for message in self_check["fatal_errors"]:
                print_status(f"[startup] 错误：{message}")
            raise SystemExit("SenseAudio-Let-Claw-Talk 启动自检失败，请先修复上面的错误。")

    refresh_wespeaker_status(args, speaker_profile)

    stop_requested = False

    def handle_signal(_signum, _frame):
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    print_status("SenseAudio-Let-Claw-Talk mode")
    if loaded_preferences:
        print_status(
            f"已加载偏好：语速 {float(args.tts_speed):.2f}，打断 {'开启' if args.interrupt_playback else '关闭'}。"
        )
    if args.speaker_verification_backend == "wespeaker":
        wespeaker_state = speaker_profile.get("wespeaker") or {}
        if wespeaker_state.get("service_ready"):
            print_status(
                f"WeSpeaker 已预热：阈值 {float(args.wespeaker_threshold):.2f}，已录入 {int(wespeaker_state.get('sample_count') or 0)} 段样本。"
            )
        else:
            print_status(f"WeSpeaker 已启用，但后台暂时还没就绪。日志：{get_wespeaker_log_path(args)}")
    save_runtime_state(args, speaker_profile)
    if args.wake_phrase:
        print_status(f"开始持续监听。当前处于休眠状态，请先说唤醒词“{args.wake_phrase}”。说“退出”或按 Ctrl+C 结束。")
        if args.sleep_phrase:
            print_status(f"说“{args.sleep_phrase}”可立即回到休眠状态。")
    else:
        print_status("开始持续监听。说“退出”或按 Ctrl+C 结束。")

    turn_id = 0
    armed_until = 0.0
    while not stop_requested:
        turn_id += 1
        with tempfile.TemporaryDirectory(prefix="voiceclaw_") as tempdir:
            capture: dict
            if args.input_file:
                audio_path = Path(args.input_file).expanduser().resolve()
                if not audio_path.exists():
                    raise SystemExit(f"Input audio not found: {audio_path}")
                capture = {"status": "ok", "path": str(audio_path), "debug_source": "input_file"}
                print_status(f"\n[input] 使用现成音频: {audio_path}")
            else:
                audio_path = Path(tempdir) / f"utterance_{turn_id:04d}.wav"
                print_status("\n[listen] 正在等待你开口...")
                play_status_sound("listen", args)
                capture = capture_utterance(args, audio_path)

            status = str(capture.get("status") or "")

            if status == "no_speech":
                if args.debug:
                    print_status("[listen] 没检测到语音，继续监听。")
                time.sleep(args.cooldown_seconds)
                continue
            if status != "ok":
                error = str(capture.get("error") or "unknown capture error")
                raise SystemExit(f"Mic capture failed: {error}")

            if args.debug:
                print_status(f"[listen] captured {capture}")

            use_wake_asr = should_use_wake_asr(args, armed_until)
            active_asr_model = args.wake_asr_model if use_wake_asr else args.asr_model
            if use_wake_asr:
                print_status(format_wake_asr_status(active_asr_model))
            else:
                print_status(f"[asr] 正在识别（{active_asr_model}）...")
            transcript = transcribe(audio_path, args, model_override=active_asr_model).strip()
            if not transcript:
                print_status("[asr] 没识别到有效文本，继续监听。")
                play_status_sound("error", args)
                time.sleep(args.cooldown_seconds)
                continue
            if transcript_looks_like_recent_echo(transcript, conversation_state):
                print_status("[echo] 检测到与最近播报高度相似的回录，已忽略本轮语音。")
                play_status_sound("error", args)
                time.sleep(args.cooldown_seconds)
                continue

            if should_exit(transcript):
                print_status(f"[you] {transcript}")
                play_status_sound("exit", args)
                print_status("已收到退出指令，结束监听。")
                break
            if should_sleep(transcript, args):
                print_status(f"[you] {transcript}")
                armed_until = 0.0
                play_status_sound("heard", args)
                if args.wake_phrase:
                    print_status(f"[wake] 已进入休眠。下次请先说“{args.wake_phrase}”。")
                else:
                    print_status("[wake] 已进入休眠。")
                save_runtime_state(args, speaker_profile)
                time.sleep(args.cooldown_seconds)
                continue

            allowed, transcript, armed_until, just_activated = apply_wake_phrase(transcript, args, armed_until)
            if not allowed:
                if args.wake_phrase:
                    print_status(f"[wake] 仍在休眠状态，请先说“{args.wake_phrase}”。")
                elif args.debug:
                    print_status("[wake] 未命中唤醒词，忽略本轮语音。")
                time.sleep(args.cooldown_seconds)
                continue
            if just_activated:
                play_status_sound("activated", args)
            if args.wake_phrase and just_activated:
                if not transcript:
                    print_status("[wake] 已唤醒，请继续说。")
                    time.sleep(args.cooldown_seconds)
                    continue
            if not transcript:
                if args.debug:
                    print_status("[wake] 已在待命，继续说内容就行。")
                time.sleep(args.cooldown_seconds)
                continue
            print_status(f"[you] {transcript}")

            if int(runtime_flags.get("wespeaker_enroll_remaining") or 0) > 0:
                try:
                    reply = handle_wespeaker_enrollment(audio_path, args, speaker_profile, runtime_flags, transcript)
                except Exception as exc:
                    play_status_sound("error", args)
                    runtime_flags["wespeaker_enroll_remaining"] = 0
                    runtime_flags["wespeaker_enroll_reset"] = False
                    reply = f"WeSpeaker 录音建档失败：{exc}"
                conversation_state["last_user_text"] = transcript
                conversation_state["last_agent_reply_text"] = reply
                conversation_state["pending_interruption_context"] = False
                conversation_state["last_spoken_text"] = normalize_reply_for_speech(reply)
                armed_until, _ = emit_reply(reply, args, turn_id, armed_until, speaker_profile)
                conversation_state["last_reply_finished_at"] = time.time()
                time.sleep(args.post_reply_cooldown_seconds)
                continue

            if should_report_settings(transcript):
                reply = format_runtime_summary(args, speaker_profile)
                conversation_state["last_user_text"] = transcript
                conversation_state["last_agent_reply_text"] = reply
                conversation_state["pending_interruption_context"] = False
                conversation_state["last_spoken_text"] = normalize_reply_for_speech(reply)
                armed_until, _ = emit_reply(reply, args, turn_id, armed_until, speaker_profile)
                conversation_state["last_reply_finished_at"] = time.time()
                time.sleep(args.post_reply_cooldown_seconds)
                continue

            wespeaker_reply = handle_wespeaker_command(transcript, args, speaker_profile, runtime_flags)
            if wespeaker_reply:
                conversation_state["last_user_text"] = transcript
                conversation_state["last_agent_reply_text"] = wespeaker_reply
                conversation_state["pending_interruption_context"] = False
                conversation_state["last_spoken_text"] = normalize_reply_for_speech(wespeaker_reply)
                armed_until, _ = emit_reply(wespeaker_reply, args, turn_id, armed_until, speaker_profile)
                conversation_state["last_reply_finished_at"] = time.time()
                time.sleep(args.post_reply_cooldown_seconds)
                continue

            preference_reply = handle_preference_command(transcript, args)
            if preference_reply:
                conversation_state["last_user_text"] = transcript
                conversation_state["last_agent_reply_text"] = preference_reply
                conversation_state["pending_interruption_context"] = False
                conversation_state["last_spoken_text"] = normalize_reply_for_speech(preference_reply)
                armed_until, _ = emit_reply(preference_reply, args, turn_id, armed_until, speaker_profile)
                conversation_state["last_reply_finished_at"] = time.time()
                time.sleep(args.post_reply_cooldown_seconds)
                continue

            voice_reply = handle_voice_command(transcript, args)
            if voice_reply:
                conversation_state["last_user_text"] = transcript
                conversation_state["last_agent_reply_text"] = voice_reply
                conversation_state["pending_interruption_context"] = False
                conversation_state["last_spoken_text"] = normalize_reply_for_speech(voice_reply)
                armed_until, _ = emit_reply(voice_reply, args, turn_id, armed_until, speaker_profile)
                conversation_state["last_reply_finished_at"] = time.time()
                time.sleep(args.post_reply_cooldown_seconds)
                continue

            try:
                allowed_by_wespeaker, wespeaker_reason = wespeaker_should_accept(audio_path, args, speaker_profile)
            except Exception as exc:
                play_status_sound("error", args)
                print_status(f"[wespeaker] 本轮声纹校验失败，先跳过过滤：{exc}")
                allowed_by_wespeaker = True
                wespeaker_reason = None
            if not allowed_by_wespeaker:
                play_status_sound("error", args)
                if wespeaker_reason:
                    print_status(wespeaker_reason)
                save_runtime_state(args, speaker_profile)
                time.sleep(args.cooldown_seconds)
                continue

            print_status("[agent] 正在思考...")
            play_status_sound("thinking", args)
            try:
                reply = ask_agent(transcript, args, conversation_state)
            except Exception as exc:
                armed_until = extend_wake_window(args, armed_until)
                play_status_sound("error", args)
                print_status(f"[agent] 本轮回复失败，但持续监听仍保持开启: {exc}")
                save_runtime_state(args, speaker_profile)
                time.sleep(args.cooldown_seconds)
                continue
            conversation_state["last_user_text"] = transcript
            conversation_state["last_agent_reply_text"] = reply
            conversation_state["pending_interruption_context"] = False
            conversation_state["last_spoken_text"] = normalize_reply_for_speech(reply)
            armed_until, interrupted = emit_reply(reply, args, turn_id, armed_until, speaker_profile)
            conversation_state["last_reply_finished_at"] = time.time()
            conversation_state["pending_interruption_context"] = bool(interrupted)

            if args.once:
                break
            if args.input_file:
                break

            time.sleep(args.post_reply_cooldown_seconds)

    print_status("SenseAudio-Let-Claw-Talk 已退出。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
