#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
from array import array
import contextlib
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import websockets

try:
    import sherpa_onnx
except ImportError:  # pragma: no cover - optional at runtime
    sherpa_onnx = None


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_PATH = WORKSPACE_ROOT / ".env"
DEFAULT_CONFIG_PATH = Path(__file__).with_name("config.example.json")
MIC_SWIFT_SOURCE = Path(__file__).with_name("mic_pcm_stream.swift")
MIC_SWIFT_BINARY = Path(__file__).with_name("mic_pcm_stream")
MIC_APP_BUNDLE_BINARY = Path(__file__).with_name("AudioClawOverlay.app") / "Contents" / "MacOS" / "mic_pcm_stream"
PROXY_ENV_KEYS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mic-only real-time bilingual subtitle prototype for SenseAudio.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_PATH))
    parser.add_argument("--run-id", default="", help="Stable identifier for the current overlay capture session.")
    parser.add_argument("--input-pcm-file", default="", help="Use an existing 16k mono PCM file instead of live mic capture.")
    parser.add_argument("--input-wav-file", default="", help="Use an existing WAV file and convert it to PCM before streaming.")
    parser.add_argument("--translation-enabled", action="store_true", help="Force-enable translated subtitles even if config disables them.")
    parser.add_argument("--no-translation", action="store_true", help="Disable translated subtitle stream.")
    parser.add_argument("--translation-only", action="store_true", help="Run only the translated subtitle stream.")
    parser.add_argument("--translation-target-language", default="", help="Override translated subtitle target language, e.g. zh, en, ja, ko, fr.")
    parser.add_argument("--local-fast-disabled", action="store_true", help="Disable local fast subtitles for this run.")
    parser.add_argument("--local-fast-model-dir", default="", help="Override sherpa-onnx local fast model directory for this run.")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'").strip('"')
    return values


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_api_key(env_values: dict[str, str]) -> str:
    for name in ("AUDIOCLAW_ASR_API_KEY", "SENSEAUDIO_API_KEY"):
        value = env_values.get(name, "").strip() or os.getenv(name, "").strip()
        if value.startswith("sk-"):
            return value
    raise SystemExit("No SenseAudio API key found in env file or process environment.")


def clear_proxy_env() -> None:
    for key in PROXY_ENV_KEYS:
        os.environ.pop(key, None)


def ensure_mic_binary(debug: bool) -> Path:
    if MIC_APP_BUNDLE_BINARY.exists() and os.access(MIC_APP_BUNDLE_BINARY, os.X_OK):
        return MIC_APP_BUNDLE_BINARY
    if not MIC_SWIFT_SOURCE.exists():
        raise SystemExit(f"Mic streaming source not found: {MIC_SWIFT_SOURCE}")
    needs_build = not MIC_SWIFT_BINARY.exists() or MIC_SWIFT_BINARY.stat().st_mtime < MIC_SWIFT_SOURCE.stat().st_mtime
    if needs_build:
        if debug:
            print(f"[build] compiling {MIC_SWIFT_SOURCE.name}")
        command = [
            "swiftc",
            "-O",
            str(MIC_SWIFT_SOURCE),
            "-o",
            str(MIC_SWIFT_BINARY),
            "-framework",
            "AVFoundation",
        ]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "swiftc failed")
    return MIC_SWIFT_BINARY


def wav_to_pcm(wav_path: Path) -> Path:
    with wave.open(str(wav_path), "rb") as wf:
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        sample_rate = wf.getframerate()
        if channels != 1 or sample_width != 2 or sample_rate != 16000:
            raise SystemExit(
                f"WAV must be 16kHz mono 16-bit PCM. Got channels={channels}, sample_width={sample_width}, sample_rate={sample_rate}."
            )
        fd, out_path = tempfile.mkstemp(prefix="senseaudio_pcm_", suffix=".pcm")
        os.close(fd)
        pcm_path = Path(out_path)
        pcm_path.write_bytes(wf.readframes(wf.getnframes()))
        return pcm_path


@dataclass
class SegmentEntry:
    source: str
    segment_id: int
    original: str | None = None
    translation: str | None = None
    timestamp_end: int | None = None
    last_emitted_original: str = ""
    last_emitted_translation: str = ""
    last_emitted_is_final: bool | None = None


@dataclass
class SubtitleState:
    log_path: Path
    expect_original: bool
    expect_translation: bool
    transcript_archive: "TranscriptArchive | None" = None
    segments: dict[str, SegmentEntry] = field(default_factory=dict)
    last_local_activity_monotonic: float = field(default_factory=time.monotonic)
    last_senseaudio_activity_monotonic: float = field(default_factory=time.monotonic)
    last_local_endpoint_monotonic: float = field(default_factory=time.monotonic)
    local_endpoint_count_since_senseaudio: int = 0

    def _entry(self, source: str, segment_id: int) -> SegmentEntry:
        key = f"{source}:{segment_id}"
        entry = self.segments.get(key)
        if entry is None:
            entry = SegmentEntry(source=source, segment_id=segment_id)
            self.segments[key] = entry
        return entry

    def update(self, channel: str, payload: dict[str, Any]) -> None:
        data = payload.get("data") or {}
        segment_id = int(data.get("segment_id") or 0)
        entry = self._entry("senseaudio", segment_id)
        text = str(data.get("text") or "").strip()
        translations = data.get("translations") or []
        translated_text = ""
        if isinstance(translations, list):
            for item in translations:
                if isinstance(item, dict):
                    candidate = str(item.get("text") or "").strip()
                    if candidate:
                        translated_text = candidate
                        break
        if channel == "translation":
            entry.translation = translated_text or text
        else:
            entry.original = text
            if translated_text:
                entry.translation = translated_text
        if data.get("timestamp_end") is not None:
            entry.timestamp_end = int(data["timestamp_end"])
        if text:
            self.last_senseaudio_activity_monotonic = time.monotonic()
            self.local_endpoint_count_since_senseaudio = 0
        if self.transcript_archive is not None and text:
            self.transcript_archive.record(segment_id=segment_id, text=text, payload=data)
        self.emit_if_ready(entry, is_final=True)

    def update_local_partial(self, segment_id: int, text: str, *, is_final: bool) -> None:
        if not self.expect_original:
            return
        entry = self._entry("local_fast", segment_id)
        entry.original = text.strip()
        if entry.original:
            self.last_local_activity_monotonic = time.monotonic()
            if self.transcript_archive is not None:
                self.transcript_archive.record_local_fast(segment_id=segment_id, text=entry.original)
        self.emit(entry, is_final=is_final)

    def mark_local_endpoint(self) -> None:
        self.last_local_endpoint_monotonic = time.monotonic()
        self.local_endpoint_count_since_senseaudio += 1

    def emit_if_ready(self, entry: SegmentEntry, *, is_final: bool) -> None:
        if self.expect_original and entry.original:
            # In bilingual mode, show original subtitles immediately and emit
            # another record later if/when translation arrives.
            self.emit(entry, is_final=is_final)
            return
        if self.expect_translation and not self.expect_original and entry.translation:
            self.emit(entry, is_final=is_final)

    def emit(self, entry: SegmentEntry, *, is_final: bool) -> None:
        original = entry.original or ""
        translation = entry.translation or ""
        if (
            original == entry.last_emitted_original
            and translation == entry.last_emitted_translation
            and is_final == entry.last_emitted_is_final
        ):
            return
        record = {
            "source": entry.source,
            "is_final": is_final,
            "segment_id": entry.segment_id,
            "original": original,
            "translation": translation,
            "timestamp_end": entry.timestamp_end,
            "emitted_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        print("")
        print(f"[{entry.source} segment {entry.segment_id}]")
        if entry.original:
            print(f"  original:    {entry.original}")
        if entry.translation:
            print(f"  translation: {entry.translation}")
        entry.last_emitted_original = original
        entry.last_emitted_translation = translation
        entry.last_emitted_is_final = is_final


@dataclass
class TranscriptSegment:
    sequence: int
    segment_id: int
    text: str
    timestamp_end: int | None
    updated_at: str


class TranscriptArchive:
    def __init__(self, run_dir: Path, model: str) -> None:
        self.run_dir = run_dir
        self.model = model
        self.created_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.segments: list[TranscriptSegment] = []
        self.local_fast_segments: dict[int, TranscriptSegment] = {}
        self.seen_segments: set[tuple[int, str, int | None]] = set()
        self.next_sequence = 0
        self.next_local_sequence = 0
        self.json_path = self.run_dir / "senseaudio_asr.json"
        self.jsonl_path = self.run_dir / "senseaudio_asr.jsonl"
        self.text_path = self.run_dir / "senseaudio_asr.txt"
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.write_snapshot()

    def record(self, *, segment_id: int, text: str, payload: dict[str, Any]) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        timestamp_end = int(payload["timestamp_end"]) if payload.get("timestamp_end") is not None else None
        key = (segment_id, cleaned, timestamp_end)
        if key in self.seen_segments:
            return
        self.seen_segments.add(key)
        segment = TranscriptSegment(
            sequence=self.next_sequence,
            segment_id=segment_id,
            text=cleaned,
            timestamp_end=timestamp_end,
            updated_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        )
        self.next_sequence += 1
        self.segments.append(segment)
        with self.jsonl_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "sequence": segment.sequence,
                "segment_id": segment.segment_id,
                "text": segment.text,
                "timestamp_end": segment.timestamp_end,
                "updated_at": segment.updated_at,
            }, ensure_ascii=False) + "\n")

    def record_local_fast(self, *, segment_id: int, text: str) -> None:
        cleaned = text.strip()
        if not cleaned:
            return
        existing = self.local_fast_segments.get(segment_id)
        if existing is not None:
            existing.text = cleaned
            existing.updated_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            return
        self.local_fast_segments[segment_id] = TranscriptSegment(
            sequence=self.next_local_sequence,
            segment_id=segment_id,
            text=cleaned,
            timestamp_end=None,
            updated_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        )
        self.next_local_sequence += 1

    def write_snapshot(self) -> None:
        ordered = sorted(
            self.segments,
            key=lambda segment: (
                segment.timestamp_end is None,
                segment.timestamp_end if segment.timestamp_end is not None else segment.sequence,
                segment.sequence,
            ),
        )
        local_ordered = [
            self.local_fast_segments[key]
            for key in sorted(self.local_fast_segments, key=lambda segment_id: self.local_fast_segments[segment_id].sequence)
        ]
        transcript_text = "\n".join(segment.text for segment in ordered)
        local_fast_text = "\n".join(segment.text for segment in local_ordered)
        payload = {
            "run_dir": str(self.run_dir),
            "created_at": self.created_at,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "model": self.model,
            "segment_count": len(ordered),
            "transcript_text": transcript_text,
            "local_fast_segment_count": len(local_ordered),
            "local_fast_transcript_text": local_fast_text,
            "segments": [
                {
                    "sequence": segment.sequence,
                    "segment_id": segment.segment_id,
                    "text": segment.text,
                    "timestamp_end": segment.timestamp_end,
                    "updated_at": segment.updated_at,
                }
                for segment in ordered
            ],
            "local_fast_segments": [
                {
                    "sequence": segment.sequence,
                    "segment_id": segment.segment_id,
                    "text": segment.text,
                    "updated_at": segment.updated_at,
                }
                for segment in local_ordered
            ],
        }
        self.json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        self.text_path.write_text(transcript_text, encoding="utf-8")

    def finalize(self) -> None:
        self.write_snapshot()


class LocalFastRecognizer:
    def __init__(self, config: dict[str, Any], sample_rate: int, debug: bool) -> None:
        if sherpa_onnx is None:
            raise RuntimeError("sherpa-onnx is not installed")
        model_dir = Path(str(config["model_dir"])).expanduser().resolve()
        tokens = model_dir / "tokens.txt"
        if not tokens.exists():
            raise RuntimeError(f"sherpa-onnx tokens.txt not found in {model_dir}")
        self.debug = debug
        self.sample_rate = sample_rate
        self.recognizer = self._create_recognizer(model_dir, tokens, config)
        self.stream = self.recognizer.create_stream()
        self.current_segment_id = 0
        self.last_text = ""

    def _create_recognizer(self, model_dir: Path, tokens: Path, config: dict[str, Any]) -> Any:
        common_kwargs = dict(
            tokens=str(tokens),
            num_threads=int(config.get("num_threads", 2)),
            provider=str(config.get("provider", "cpu")),
            enable_endpoint_detection=True,
            rule1_min_trailing_silence=float(config.get("rule1_min_trailing_silence", 1.2)),
            rule2_min_trailing_silence=float(config.get("rule2_min_trailing_silence", 0.5)),
            rule3_min_utterance_length=float(config.get("rule3_min_utterance_length", 8.0)),
        )

        ctc_model = self._first_existing(
            model_dir / "model.int8.onnx",
            model_dir / "model.onnx",
        )
        if ctc_model is not None:
            if self.debug:
                print(f"[local-fast] using zipformer2_ctc model {ctc_model}")
            return sherpa_onnx.OnlineRecognizer.from_zipformer2_ctc(
                model=str(ctc_model),
                **common_kwargs,
            )

        encoder = self._first_existing(
            model_dir / "encoder-epoch-99-avg-1.int8.onnx",
            model_dir / "encoder-epoch-99-avg-1.onnx",
            model_dir / "encoder-epoch-29-avg-9-with-averaged-model.int8.onnx",
            model_dir / "encoder-epoch-29-avg-9-with-averaged-model.onnx",
        )
        decoder = self._first_existing(
            model_dir / "decoder-epoch-99-avg-1.int8.onnx",
            model_dir / "decoder-epoch-99-avg-1.onnx",
            model_dir / "decoder-epoch-29-avg-9-with-averaged-model.int8.onnx",
            model_dir / "decoder-epoch-29-avg-9-with-averaged-model.onnx",
        )
        joiner = self._first_existing(
            model_dir / "joiner-epoch-99-avg-1.int8.onnx",
            model_dir / "joiner-epoch-99-avg-1.onnx",
            model_dir / "joiner-epoch-29-avg-9-with-averaged-model.int8.onnx",
            model_dir / "joiner-epoch-29-avg-9-with-averaged-model.onnx",
        )
        if encoder is not None and decoder is not None and joiner is not None:
            modeling_unit = "cjkchar"
            bpe_vocab = ""
            if (model_dir / "bpe.model").exists():
                modeling_unit = "bpe"
                bpe_vocab = str(model_dir / "bpe.model")
            if self.debug:
                print(f"[local-fast] using transducer model {model_dir.name}")
            return sherpa_onnx.OnlineRecognizer.from_transducer(
                encoder=str(encoder),
                decoder=str(decoder),
                joiner=str(joiner),
                modeling_unit=modeling_unit,
                bpe_vocab=bpe_vocab,
                **common_kwargs,
            )

        raise RuntimeError(f"supported sherpa-onnx model files not found in {model_dir}")

    @staticmethod
    def _first_existing(*candidates: Path) -> Path | None:
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def process_chunk(self, chunk: bytes, subtitle_state: SubtitleState) -> None:
        floats = self._pcm_to_floats(chunk)
        if not floats:
            return
        self.stream.accept_waveform(self.sample_rate, floats)
        self._drain(subtitle_state)

    def finish(self, subtitle_state: SubtitleState) -> None:
        self.stream.input_finished()
        self._drain(subtitle_state)
        self.last_text = ""

    def _drain(self, subtitle_state: SubtitleState) -> None:
        while self.recognizer.is_ready(self.stream):
            self.recognizer.decode_stream(self.stream)
            result = self.recognizer.get_result_all(self.stream)
            text = result.text.strip()
            if text and text != self.last_text:
                subtitle_state.update_local_partial(self.current_segment_id, text, is_final=False)
                self.last_text = text
            if self.recognizer.is_endpoint(self.stream):
                subtitle_state.mark_local_endpoint()
                if self.debug:
                    print(f"[local-fast] endpoint segment={self.current_segment_id}")
                self.recognizer.reset(self.stream)
                self.current_segment_id += 1
                self.last_text = ""

    @staticmethod
    def _pcm_to_floats(chunk: bytes) -> list[float]:
        if not chunk:
            return []
        ints = array("h")
        ints.frombytes(chunk[: len(chunk) - (len(chunk) % 2)])
        return [sample / 32768.0 for sample in ints]


class RealTimeASRClient:
    def __init__(
        self,
        *,
        name: str,
        endpoint: str,
        api_key: str,
        model: str,
        target_language: str | None,
        capture_config: dict[str, Any],
        debug: bool,
    ) -> None:
        self.name = name
        self.endpoint = endpoint
        self.api_key = api_key
        self.model = model
        self.target_language = target_language
        self.capture_config = capture_config
        self.debug = debug
        self.websocket: websockets.ClientConnection | None = None

    async def connect(self) -> None:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        self.websocket = await websockets.connect(
            self.endpoint,
            additional_headers=headers,
            max_size=2**20,
            proxy=None,
        )
        connected = json.loads(await self.websocket.recv())
        if connected.get("event") != "connected_success":
            raise RuntimeError(f"{self.name} connect failed: {connected}")
        if self.debug:
            print(f"[{self.name}] connected: {connected}")
        payload = {
            "event": "task_start",
            "model": self.model,
            "audio_setting": {
                "sample_rate": int(self.capture_config["sample_rate"]),
                "format": "pcm",
                "channel": 1,
            },
            "vad_setting": {
                "silence_duration": int(self.capture_config.get("silence_finalize_ms", 700)),
                "min_speech_duration": 300,
            },
            "transcription_setting": {
                "recognize_mode": str(self.capture_config.get("recognize_mode", "auto")),
            },
        }
        optional_vad_fields = {
            "min_speech_duration": self.capture_config.get("min_speech_duration_ms"),
            "soft_max_duration": self.capture_config.get("soft_max_duration_ms"),
            "hard_max_duration": self.capture_config.get("hard_max_duration_ms"),
            "soft_silence_duration": self.capture_config.get("soft_silence_duration_ms"),
            "threshold": self.capture_config.get("vad_threshold"),
        }
        for key, value in optional_vad_fields.items():
            if value is not None:
                payload["vad_setting"][key] = value
        if self.target_language:
            payload["transcription_setting"]["target_languages"] = [self.target_language]
        await self.websocket.send(json.dumps(payload, ensure_ascii=False))
        started = json.loads(await self.websocket.recv())
        if started.get("event") != "task_started":
            raise RuntimeError(f"{self.name} task_start failed: {started}")
        if self.debug:
            print(f"[{self.name}] started: {started}")

    async def send_audio(self, chunk: bytes) -> None:
        if self.websocket is None:
            raise RuntimeError("websocket not connected")
        await self.websocket.send(chunk)

    async def finish(self) -> None:
        if self.websocket is None:
            return
        await self.websocket.send(json.dumps({"event": "task_finish"}))

    async def close(self) -> None:
        if self.websocket is None:
            return
        await self.websocket.close()
        self.websocket = None

    async def receive_loop(self, subtitle_state: SubtitleState) -> None:
        if self.websocket is None:
            raise RuntimeError("websocket not connected")
        async for message in self.websocket:
            payload = json.loads(message)
            event = payload.get("event")
            if self.debug:
                print(f"[{self.name}] event={event} payload={payload}")
            if event == "result_final":
                subtitle_state.update(self.name, payload)
            elif event == "task_failed":
                raise RuntimeError(f"{self.name} failed: {payload}")
            elif event == "task_finished":
                return


async def iter_pcm_chunks_from_file(path: Path, chunk_bytes: int, sleep_seconds: float) -> Any:
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(chunk_bytes)
            if not chunk:
                break
            yield chunk
            await asyncio.sleep(sleep_seconds)


async def iter_pcm_chunks_from_process(
    command: list[str],
    chunk_bytes: int,
    debug: bool,
    stop_requested: asyncio.Event,
) -> Any:
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    assert process.stdout is not None
    assert process.stderr is not None

    async def drain_stderr() -> None:
        while True:
            line = await process.stderr.readline()
            if not line:
                break
            if debug:
                print(f"[mic stderr] {line.decode('utf-8', errors='replace').rstrip()}")

    stderr_task = asyncio.create_task(drain_stderr())
    pending = bytearray()
    try:
        while True:
            try:
                chunk = await asyncio.wait_for(process.stdout.read(chunk_bytes), timeout=0.25)
            except asyncio.TimeoutError:
                if stop_requested.is_set():
                    break
                # Keep the outer loop alive during silent periods so watchdog
                # logic can reconnect SenseAudio streams that self-finish while
                # we are still waiting for system audio to arrive.
                yield b""
                continue
            if not chunk:
                break
            pending.extend(chunk)
            while len(pending) >= chunk_bytes:
                yield bytes(pending[:chunk_bytes])
                del pending[:chunk_bytes]
        if pending:
            yield bytes(pending)
    finally:
        with contextlib.suppress(ProcessLookupError):
            process.send_signal(signal.SIGINT)
        try:
            await asyncio.wait_for(process.wait(), timeout=2.0)
        except asyncio.TimeoutError:
            with contextlib.suppress(ProcessLookupError):
                process.kill()
            await process.wait()
        await stderr_task


async def run() -> int:
    args = parse_args()
    clear_proxy_env()
    config = load_config(Path(args.config))
    env_values = load_env_file(Path(args.env_file))
    api_key = resolve_api_key(env_values)

    capture = config["capture"]
    asr = config["senseaudio"]["asr"]
    local_fast_cfg = dict(config.get("local_fast") or {})
    translation_cfg = config["translation"]
    runtime = config["runtime"]
    chunk_ms = int(capture["chunk_ms"])
    chunk_bytes = int(capture["sample_rate"]) * 2 * chunk_ms // 1000
    sleep_seconds = chunk_ms / 1000.0
    reconnect_backoff_ms = int(runtime.get("reconnect_backoff_ms", 1200))
    connect_max_attempts = int(runtime.get("connect_max_attempts", 4))
    watchdog_no_event_ms = int(runtime.get("watchdog_no_event_ms", 8000))
    local_activity_window_ms = int(runtime.get("local_activity_window_ms", 5000))
    watchdog_restart_cooldown_ms = int(runtime.get("watchdog_restart_cooldown_ms", 5000))
    watchdog_local_endpoint_streak = int(runtime.get("watchdog_local_endpoint_streak", 2))

    translation_enabled = (args.translation_enabled or bool(translation_cfg.get("enabled"))) and not args.no_translation
    if args.translation_target_language.strip():
        translation_cfg["target_language"] = args.translation_target_language.strip()
    if args.local_fast_disabled:
        local_fast_cfg["enabled"] = False
    if args.local_fast_model_dir.strip():
        local_fast_cfg["enabled"] = True
        local_fast_cfg["model_dir"] = args.local_fast_model_dir.strip()
    run_id = args.run_id.strip() or time.strftime("%Y%m%d-%H%M%S")
    run_dir = WORKSPACE_ROOT / "state" / "realtime_interpreter" / "runs" / run_id
    transcript_archive = TranscriptArchive(run_dir=run_dir, model=str(asr["model"]))
    subtitle_state = SubtitleState(
        log_path=Path(runtime["persist_log_path"]),
        expect_original=not args.translation_only,
        expect_translation=translation_enabled,
        transcript_archive=transcript_archive,
    )
    local_fast_enabled = bool(local_fast_cfg.get("enabled")) and not args.translation_only
    local_fast_recognizer: LocalFastRecognizer | None = None
    if local_fast_enabled:
        try:
            local_fast_recognizer = LocalFastRecognizer(local_fast_cfg, int(capture["sample_rate"]), args.debug)
            if args.debug:
                print("[local-fast] enabled")
        except Exception as exc:
            print(f"[local-fast] disabled: {exc}", file=sys.stderr)
            local_fast_recognizer = None
    stop_requested = asyncio.Event()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        with contextlib.suppress(NotImplementedError):
            loop.add_signal_handler(sig, stop_requested.set)

    async def start_clients() -> tuple[RealTimeASRClient | None, RealTimeASRClient | None, list[asyncio.Task[None]]]:
        original_client: RealTimeASRClient | None = None
        translated_client: RealTimeASRClient | None = None
        receive_tasks: list[asyncio.Task[None]] = []
        translation_strategy = str(translation_cfg.get("strategy") or "single_bilingual_stream").strip()
        single_bilingual_stream = (
            translation_enabled
            and not args.translation_only
            and translation_strategy != "parallel_dual_session"
        )

        original_attempted = False
        last_original_error: Exception | None = None
        for attempt in range(1, connect_max_attempts + 1):
            try:
                if not args.translation_only:
                    original_client = RealTimeASRClient(
                        name="original",
                        endpoint=str(asr["endpoint"]),
                        api_key=api_key,
                        model=str(asr["model"]),
                        target_language=str(translation_cfg["target_language"]) if single_bilingual_stream else None,
                        capture_config=capture,
                        debug=args.debug,
                    )
                    original_attempted = True
                    await original_client.connect()
                last_original_error = None
                break
            except Exception as exc:
                last_original_error = exc
                print(
                    f"[connect] original attempt {attempt}/{connect_max_attempts} failed: {exc}",
                    file=sys.stderr,
                )
                if attempt >= connect_max_attempts:
                    raise
                await asyncio.sleep(reconnect_backoff_ms / 1000.0)

        if original_attempted and last_original_error is not None:
            raise last_original_error

        if translation_enabled and not single_bilingual_stream:
            translated_client = RealTimeASRClient(
                name="translation",
                endpoint=str(asr["endpoint"]),
                api_key=api_key,
                model=str(asr["model"]),
                target_language=str(translation_cfg["target_language"]),
                capture_config=capture,
                debug=args.debug,
            )
            try:
                await translated_client.connect()
            except Exception as exc:
                if args.translation_only:
                    raise
                print(f"[translation] disabled after startup failure: {exc}", file=sys.stderr)
                translated_client = None
                subtitle_state.expect_translation = False

        if original_client is not None:
            receive_tasks.append(asyncio.create_task(original_client.receive_loop(subtitle_state)))
        if translated_client is not None:
            receive_tasks.append(asyncio.create_task(translated_client.receive_loop(subtitle_state)))
        return original_client, translated_client, receive_tasks

    async def finish_clients(
        original_client: RealTimeASRClient | None,
        translated_client: RealTimeASRClient | None,
        receive_tasks: list[asyncio.Task[None]],
    ) -> None:
        if original_client is not None:
            await original_client.finish()
        if translated_client is not None:
            await translated_client.finish()
        if receive_tasks:
            await asyncio.gather(*receive_tasks)

    async def abort_clients(
        original_client: RealTimeASRClient | None,
        translated_client: RealTimeASRClient | None,
        receive_tasks: list[asyncio.Task[None]],
    ) -> None:
        if original_client is not None:
            with contextlib.suppress(Exception):
                await original_client.close()
        if translated_client is not None:
            with contextlib.suppress(Exception):
                await translated_client.close()
        for task in receive_tasks:
            task.cancel()
        if receive_tasks:
            await asyncio.gather(*receive_tasks, return_exceptions=True)

    original_client, translated_client, receive_tasks = await start_clients()
    last_watchdog_restart_monotonic = 0.0

    temp_pcm_path: Path | None = None
    try:
        if args.input_wav_file:
            temp_pcm_path = wav_to_pcm(Path(args.input_wav_file).expanduser().resolve())
            chunk_source = iter_pcm_chunks_from_file(temp_pcm_path, chunk_bytes, sleep_seconds)
        elif args.input_pcm_file:
            chunk_source = iter_pcm_chunks_from_file(Path(args.input_pcm_file).expanduser().resolve(), chunk_bytes, sleep_seconds)
        else:
            mic_binary = ensure_mic_binary(args.debug)
            command = [str(mic_binary), "--sample-rate", str(capture["sample_rate"])]
            device_name = str(capture.get("input_device_name") or "").strip()
            if device_name:
                command.extend(["--device-name", device_name])
            chunk_source = iter_pcm_chunks_from_process(command, chunk_bytes, args.debug, stop_requested)

        async for chunk in chunk_source:
            if stop_requested.is_set():
                break
            if chunk and local_fast_recognizer is not None:
                local_fast_recognizer.process_chunk(chunk, subtitle_state)
            try:
                if chunk and original_client is not None:
                    await original_client.send_audio(chunk)
                if chunk and translated_client is not None:
                    await translated_client.send_audio(chunk)
            except Exception as exc:
                print(f"[watchdog] send_audio failed, reconnecting: {exc}", file=sys.stderr)
                await abort_clients(original_client, translated_client, receive_tasks)
                await asyncio.sleep(reconnect_backoff_ms / 1000.0)
                original_client, translated_client, receive_tasks = await start_clients()
                last_watchdog_restart_monotonic = time.monotonic()
                continue

            now = time.monotonic()
            local_recent = (now - subtitle_state.last_local_activity_monotonic) * 1000.0 <= local_activity_window_ms
            senseaudio_idle_ms = (now - subtitle_state.last_senseaudio_activity_monotonic) * 1000.0
            if (
                original_client is not None
                and local_recent
                and senseaudio_idle_ms >= watchdog_no_event_ms
                and (now - last_watchdog_restart_monotonic) * 1000.0 >= watchdog_restart_cooldown_ms
            ):
                print(
                    f"[watchdog] no SenseAudio final for {int(senseaudio_idle_ms)}ms while local subtitles are active; reconnecting",
                    file=sys.stderr,
                )
                await abort_clients(original_client, translated_client, receive_tasks)
                await asyncio.sleep(reconnect_backoff_ms / 1000.0)
                original_client, translated_client, receive_tasks = await start_clients()
                subtitle_state.last_senseaudio_activity_monotonic = time.monotonic()
                last_watchdog_restart_monotonic = time.monotonic()

            original_receive_done = bool(receive_tasks) and receive_tasks[0].done()
            endpoint_streak_triggered = (
                original_client is not None
                and subtitle_state.local_endpoint_count_since_senseaudio >= watchdog_local_endpoint_streak
                and senseaudio_idle_ms >= max(2500, watchdog_no_event_ms * 0.5)
                and (now - last_watchdog_restart_monotonic) * 1000.0 >= watchdog_restart_cooldown_ms
            )
            if original_receive_done or endpoint_streak_triggered:
                reason = "receive_loop_done" if original_receive_done else f"local_endpoint_streak={subtitle_state.local_endpoint_count_since_senseaudio}"
                if original_receive_done:
                    with contextlib.suppress(Exception):
                        exc = receive_tasks[0].exception()
                        if exc:
                            print(f"[watchdog] original receive loop failed: {exc}", file=sys.stderr)
                print(f"[watchdog] reconnecting original SenseAudio stream due to {reason}", file=sys.stderr)
                await abort_clients(original_client, translated_client, receive_tasks)
                await asyncio.sleep(reconnect_backoff_ms / 1000.0)
                original_client, translated_client, receive_tasks = await start_clients()
                subtitle_state.last_senseaudio_activity_monotonic = time.monotonic()
                subtitle_state.local_endpoint_count_since_senseaudio = 0
                last_watchdog_restart_monotonic = time.monotonic()

        if local_fast_recognizer is not None:
            local_fast_recognizer.finish(subtitle_state)
        await finish_clients(original_client, translated_client, receive_tasks)
    finally:
        transcript_archive.finalize()
        if temp_pcm_path and temp_pcm_path.exists():
            temp_pcm_path.unlink()
    return 0


def main() -> int:
    try:
        return asyncio.run(run())
    except KeyboardInterrupt:
        print("\n[runner] interrupted")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
