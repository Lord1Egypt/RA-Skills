import argparse
import json
import os
import sys
from typing import Any
from types import SimpleNamespace
import tempfile
import shutil
import urllib.error
import urllib.request
import uuid
import soundfile as sf
import numpy as np
import logging
logging.basicConfig(level=logging.ERROR)

IS_DARWIN = sys.platform == "darwin"

_MLX_AUDIO_READY = False
_QWEN_ASR_BACKEND_READY = False
_QWEN_TTS_BACKEND_READY = False

_QWEN_ASR_TORCH = None
_QWEN_TTS_TORCH = None
_QWEN_ASR_MODEL_CLS = None
_QWEN_TTS_MODEL_CLS = None

_QWEN_ASR_MODEL = None
_QWEN_ASR_MODEL_KEY = None
_QWEN_TTS_MODEL = None
_QWEN_TTS_MODEL_KEY = None



def _ensure_mlx_audio() -> None:
    global _MLX_AUDIO_READY
    if _MLX_AUDIO_READY:
        return
    try:
        import mlx_audio  # noqa: F401
    except ImportError:
        print("mlx-audio 未安装，正在安装...", file=sys.stderr)
        os.system("uv add mlx-audio --prerelease=allow")
        import mlx_audio  # noqa: F401
        print("mlx-audio installed", file=sys.stderr)
    _MLX_AUDIO_READY = True


def _resolve_default_device() -> str:
    configured = os.environ.get("QWEN_AUDIO_DEVICE")
    if configured and configured.strip():
        return configured.strip()
    try:
        import torch  # type: ignore
        if torch.cuda.is_available():
            return "cuda:0"
    except Exception:
        pass
    return "cpu"


DEFAULT_DEVICE = _resolve_default_device()
DEFAULT_DTYPE = os.environ.get("QWEN_AUDIO_DTYPE", "bf16")


def _resolve_torch_dtype(dtype: str, torch: Any) -> Any:
    norm = (dtype or DEFAULT_DTYPE).lower().strip()
    table = {
        "float16": torch.float16,
        "fp16": torch.float16,
        "half": torch.float16,
        "bfloat16": torch.bfloat16,
        "bf16": torch.bfloat16,
        "float32": torch.float32,
        "fp32": torch.float32,
    }
    if norm not in table:
        raise ValueError(f"unsupported dtype: {dtype}")
    return table[norm]


def _normalize_device(device: str) -> str:
    resolved = (device or DEFAULT_DEVICE).strip().lower()
    if resolved in {"cuda", "gpu"}:
        return "cuda:0"
    return resolved


def _ensure_qwen_asr_backend() -> tuple[Any, Any]:
    global _QWEN_ASR_BACKEND_READY, _QWEN_ASR_TORCH, _QWEN_ASR_MODEL_CLS
    if _QWEN_ASR_BACKEND_READY and _QWEN_ASR_TORCH is not None and _QWEN_ASR_MODEL_CLS is not None:
        return _QWEN_ASR_TORCH, _QWEN_ASR_MODEL_CLS
    try:
        import torch  # type: ignore
        from qwen_asr import Qwen3ASRModel  # type: ignore
    except Exception as exc:
        raise RuntimeError("qwen-asr 不可用，请先安装 qwen-asr 和 torch") from exc
    _QWEN_ASR_TORCH = torch
    _QWEN_ASR_MODEL_CLS = Qwen3ASRModel
    _QWEN_ASR_BACKEND_READY = True
    return _QWEN_ASR_TORCH, _QWEN_ASR_MODEL_CLS


def _ensure_qwen_tts_backend() -> tuple[Any, Any]:
    global _QWEN_TTS_BACKEND_READY, _QWEN_TTS_TORCH, _QWEN_TTS_MODEL_CLS
    if _QWEN_TTS_BACKEND_READY and _QWEN_TTS_TORCH is not None and _QWEN_TTS_MODEL_CLS is not None:
        return _QWEN_TTS_TORCH, _QWEN_TTS_MODEL_CLS
    try:
        import torch  # type: ignore
        from qwen_tts import Qwen3TTSModel  # type: ignore
    except Exception as exc:
        raise RuntimeError("qwen-tts 不可用，请先安装 qwen-tts 和 torch") from exc
    _QWEN_TTS_TORCH = torch
    _QWEN_TTS_MODEL_CLS = Qwen3TTSModel
    _QWEN_TTS_BACKEND_READY = True
    return _QWEN_TTS_TORCH, _QWEN_TTS_MODEL_CLS


def _get_qwen_asr_model(
    model_name: str,
    aligner_model: str,
    device: str = DEFAULT_DEVICE,
    dtype: str = DEFAULT_DTYPE,
) -> Any:
    global _QWEN_ASR_MODEL, _QWEN_ASR_MODEL_KEY
    torch, Qwen3ASRModel = _ensure_qwen_asr_backend()
    resolved_device = _normalize_device(device)
    resolved_dtype = (dtype or DEFAULT_DTYPE).strip()
    key = json.dumps(
        {
            "model": model_name,
            "aligner_model": aligner_model,
            "device": resolved_device,
            "dtype": resolved_dtype,
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    if _QWEN_ASR_MODEL is not None and _QWEN_ASR_MODEL_KEY == key:
        return _QWEN_ASR_MODEL

    torch_dtype = _resolve_torch_dtype(resolved_dtype, torch)
    _QWEN_ASR_MODEL = Qwen3ASRModel.from_pretrained(
        model_name,
        dtype=torch_dtype,
        device_map=resolved_device,
        max_inference_batch_size=2,
        max_new_tokens=8192,
        forced_aligner=aligner_model,
        forced_aligner_kwargs={
            "dtype": torch_dtype,
            "device_map": resolved_device,
        },
    )
    _QWEN_ASR_MODEL_KEY = key
    return _QWEN_ASR_MODEL


def _get_qwen_tts_model(
    model_name: str,
    device: str = DEFAULT_DEVICE,
    dtype: str = DEFAULT_DTYPE,
) -> Any:
    global _QWEN_TTS_MODEL, _QWEN_TTS_MODEL_KEY
    torch, Qwen3TTSModel = _ensure_qwen_tts_backend()
    resolved_device = _normalize_device(device)
    resolved_dtype = (dtype or DEFAULT_DTYPE).strip()
    key = json.dumps(
        {
            "model": model_name,
            "device": resolved_device,
            "dtype": resolved_dtype,
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    if _QWEN_TTS_MODEL is not None and _QWEN_TTS_MODEL_KEY == key:
        return _QWEN_TTS_MODEL

    load_kwargs = {
        "device_map": resolved_device,
        "dtype": _resolve_torch_dtype(resolved_dtype, torch),
    }
    if resolved_device.startswith("cuda"):
        load_kwargs["attn_implementation"] = "flash_attention_2"
    try:
        _QWEN_TTS_MODEL = Qwen3TTSModel.from_pretrained(model_name, **load_kwargs)
    except Exception:
        if "attn_implementation" not in load_kwargs:
            raise
        load_kwargs.pop("attn_implementation", None)
        _QWEN_TTS_MODEL = Qwen3TTSModel.from_pretrained(model_name, **load_kwargs)

    _QWEN_TTS_MODEL_KEY = key
    return _QWEN_TTS_MODEL

def _can_reach_hf(endpoint: str, timeout_sec: float = 2.0) -> bool:
    url = endpoint.rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout_sec):
            return True
    except urllib.error.HTTPError:
        return True
    except Exception:
        return False

def _configure_hf(args: argparse.Namespace) -> None:
    if args.hf_mirror:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        endpoint = os.environ["HF_ENDPOINT"]
    else:
        endpoint = os.environ.get("HF_ENDPOINT", "https://huggingface.co")
    if not _can_reach_hf(endpoint):
        os.environ["HF_HUB_OFFLINE"] = "1"
        print("! 无法连接 Hugging Face，已启用离线模式（仅使用本地模型）", file=sys.stderr)

DEFAULT_TTS_MODEL = (
    "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16"
    if IS_DARWIN
    else "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
)
DEFAULT_STT_MODEL = (
    "mlx-community/Qwen3-ASR-1.7B-bf16"
    if IS_DARWIN
    else "Qwen/Qwen3-ASR-1.7B"
)
DEFAULT_ASR_MODEL = DEFAULT_STT_MODEL
DEFAULT_ALIGNER_MODEL = (
    "mlx-community/Qwen3-ForcedAligner-0.6B-8bit"
    if IS_DARWIN
    else "Qwen/Qwen3-ForcedAligner-0.6B"
)
DEFAULT_CUSTOME_MODEL = (
    "mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice"
    if IS_DARWIN
    else "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
)
DEFAULT_VOICEDESIGN_MODEL = (
    "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16"
    if IS_DARWIN
    else "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign"
)


def _default_qwen_speaker(language: str | None) -> str:
    lang = (language or "").strip().lower()
    if "en" in lang:
        return "Ryan"
    if "japanese" in lang or "jp" in lang:
        return "Ono_Anna"
    if "korean" in lang or "ko" in lang:
        return "Sohee"
    return "Vivian"

def _get_sample_rate(result: Any, model: Any) -> int:
    # Best-effort sampling rate inference.
    for attr in ("sample_rate", "sr", "sampling_rate"):
        if hasattr(result, attr):
            return int(getattr(result, attr))
    for attr in ("sample_rate", "sr", "sampling_rate"):
        if hasattr(model, attr):
            return int(getattr(model, attr))
    return 24000

def _normalize_text(text: str) -> str:
    """Normalize text by replacing newlines with spaces and collapsing multiple spaces."""
    if not text:
        return text
    # Replace newlines with spaces
    text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    # Collapse multiple spaces into one
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text.strip()

# Text-to-Speech
def run_tts(args: argparse.Namespace) -> None:
    # Normalize text: replace newlines with spaces
    text = _normalize_text(args.text)
    ref_text = _normalize_text(args.ref_text) if args.ref_text else None

    # Handle --ref_voice parameter (shortcut for voice_id)
    if args.ref_voice and not args.ref_audio:
        voice_path = get_voice_path(args.ref_voice)
        if voice_path is None:
            raise ValueError(f"Voice not found: {args.ref_voice}")
        args.ref_audio = voice_path["ref_audio"]
        if not args.ref_text:
            ref_text = voice_path["ref_text"]

    if IS_DARWIN:
        _ensure_mlx_audio()
        from mlx_audio.tts.utils import load_model as load_tts_model

        model = load_tts_model(DEFAULT_VOICEDESIGN_MODEL if args.instruct else args.model)

        kwargs = {
            "text": text,
            "language": args.language,
        }
        if args.voice:
            kwargs["voice"] = args.voice
        if args.instruct:
            kwargs["instruct"] = args.instruct
        if args.ref_audio:
            kwargs["ref_audio"] = args.ref_audio
        if ref_text:
            kwargs["ref_text"] = ref_text

        results = list(model.generate(**kwargs))
        if not results:
            raise RuntimeError("TTS 生成失败：未返回音频结果")
        result = results[0]
        sample_rate = _get_sample_rate(result, model)
        audio_np = np.array(result.audio, dtype=np.float32)
    else:
        language = args.language if args.language else "English"
        qwen_voice = args.voice if args.voice and args.voice != "Chelsie" else None
        speaker = qwen_voice or args.speaker or _default_qwen_speaker(language)

        if args.instruct:
            model = _get_qwen_tts_model(DEFAULT_VOICEDESIGN_MODEL)
            wavs, sample_rate = model.generate_voice_design(
                text=text,
                language=language,
                instruct=args.instruct,
            )
        elif args.ref_audio or ref_text:
            if not args.ref_audio or not ref_text:
                raise ValueError("使用参考音频克隆时必须同时提供 ref_audio 和 ref_text")
            model = _get_qwen_tts_model(args.model)
            wavs, sample_rate = model.generate_voice_clone(
                text=text,
                language=language,
                ref_audio=args.ref_audio,
                ref_text=ref_text,
            )
        else:
            custom_model = (
                DEFAULT_CUSTOME_MODEL
                if args.model == DEFAULT_TTS_MODEL
                else args.model
            )
            model = _get_qwen_tts_model(custom_model)
            kwargs = {
                "text": text,
                "language": language,
                "speaker": speaker,
            }
            wavs, sample_rate = model.generate_custom_voice(**kwargs)

        if wavs is None:
            raise RuntimeError("TTS 生成失败：未返回音频结果")
        audio = wavs[0] if isinstance(wavs, (list, tuple)) else wavs
        audio_np = np.array(audio, dtype=np.float32)
        if audio_np.ndim > 1:
            audio_np = audio_np.reshape(-1)
        sample_rate = int(sample_rate) if sample_rate else 24000

    # audio_fast = librosa.effects.time_stretch(audio_np, rate=1.2)
    # fast_output = args.output.replace(".wav", "_fast.wav")
    # sf.write(fast_output, audio_fast, sample_rate)
    sf.write(args.output, audio_np, sample_rate)

    # Calculate duration
    duration = len(audio_np) / sample_rate

    # Output result as JSON
    result_data = {
        "audio_path": os.path.abspath(args.output),
        "duration": round(duration, 3),
        "sample_rate": sample_rate,
        "success": True
    }
    print(json.dumps(result_data, ensure_ascii=False))

# Speech-to-Text
def run_stt(args: argparse.Namespace) -> None:
    if not os.path.exists(args.audio):
        raise FileNotFoundError(f"音频文件不存在: {args.audio}")

    audio_data, sr = sf.read(args.audio, always_2d=True)
    total_sec = audio_data.shape[0] / sr
    asr_text = ""
    alignment_result: list[SimpleNamespace] = []

    if IS_DARWIN:
        _ensure_mlx_audio()
        from mlx_audio.stt.utils import load_model as load_stt_model

        asr_model = load_stt_model(args.model)
        aligner_model = load_stt_model(args.aligner_model)
        max_chunk_sec = 120.0
        min_silence_sec = 0.2
        tail_silence_window_sec = 3.0
        merge_tail_sec = 60.0

        if total_sec <= max_chunk_sec:
            asr_result = asr_model.generate(
                args.audio,
                language=args.language,
                verbose=True,
            )
            asr_text = str(asr_result.text or "").strip()
            raw_alignment = aligner_model.generate(
                args.audio,
                text=asr_text,
                language=args.language,
            )
            alignment_result = [
                SimpleNamespace(
                    start_time=float(item.start_time),
                    end_time=float(item.end_time),
                    text=str(item.text),
                )
                for item in (raw_alignment or [])
            ]
        else:
            def _find_tail_silence_start(alignment, chunk_len_sec: float) -> float | None:
                if not alignment:
                    return None
                window_start = max(0.0, chunk_len_sec - tail_silence_window_sec)
                gaps = []

                first = alignment[0]
                if first.start_time >= min_silence_sec:
                    gaps.append((0.0, first.start_time))

                for i in range(len(alignment) - 1):
                    gap_start = alignment[i].end_time
                    gap_end = alignment[i + 1].start_time
                    if gap_end - gap_start >= min_silence_sec:
                        gaps.append((gap_start, gap_end))

                last = alignment[-1]
                if chunk_len_sec - last.end_time >= min_silence_sec:
                    gaps.append((last.end_time, chunk_len_sec))

                if not gaps:
                    return None

                tail_gaps = [
                    gap for gap in gaps if gap[1] < window_start and gap[0] < chunk_len_sec
                ]
                if not tail_gaps:
                    return None
                return max(tail_gaps, key=lambda g: g[0])[0]

            max_chunk_samples = int(max_chunk_sec * sr)
            temp_dir = tempfile.mkdtemp(prefix="mlx_audio_stream_")
            try:
                start = 0
                idx = 0
                total_samples = audio_data.shape[0]
                while start < total_samples:
                    end = min(start + max_chunk_samples, total_samples)
                    if total_samples - end < int(merge_tail_sec * sr):
                        end = total_samples
                    chunk_path = os.path.join(temp_dir, f"chunk_{idx:03d}.wav")
                    sf.write(chunk_path, audio_data[start:end], sr)

                    chunk_asr = asr_model.generate(
                        chunk_path,
                        language=args.language,
                        verbose=True,
                    )
                    if chunk_asr.text:
                        asr_text = f"{asr_text} {chunk_asr.text}".strip()

                    raw_chunk_alignment = aligner_model.generate(
                        chunk_path,
                        text=chunk_asr.text,
                        language=args.language,
                    )
                    chunk_alignment = [
                        SimpleNamespace(
                            start_time=float(item.start_time),
                            end_time=float(item.end_time),
                            text=str(item.text),
                        )
                        for item in (raw_chunk_alignment or [])
                    ]

                    chunk_len = (end - start) / sr
                    cut_start = None
                    if chunk_alignment:
                        cut_start = _find_tail_silence_start(chunk_alignment, chunk_len)

                    offset = start / sr

                    # Advance by nearest tail silence (<=3s from end) to avoid re-running models.
                    if end >= total_samples:
                        next_start = total_samples
                    elif chunk_alignment:
                        if cut_start is None:
                            last_end = chunk_alignment[-1].end_time
                            next_start = int(round((offset + last_end) * sr))
                        else:
                            next_start = int(round((offset + cut_start) * sr))
                        if next_start <= start:
                            next_start = end
                    else:
                        next_start = end

                    trim_at = None
                    if cut_start is not None and next_start < end:
                        trim_at = cut_start

                    if trim_at is None:
                        trimmed_alignment = chunk_alignment
                    else:
                        trimmed_alignment = [
                            item for item in chunk_alignment if item.end_time <= trim_at
                        ]

                    for item in trimmed_alignment:
                        alignment_result.append(
                            SimpleNamespace(
                                start_time=item.start_time + offset,
                                end_time=item.end_time + offset,
                                text=item.text,
                            )
                        )
                    if next_start > total_samples:
                        next_start = total_samples
                    start = next_start
                    idx += 1
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
    else:
        asr_model = _get_qwen_asr_model(args.model, args.aligner_model)
        results = asr_model.transcribe(
            audio=args.audio,
            language=args.language,
            return_time_stamps=True,
        )
        if not isinstance(results, list):
            results = [results]
        first = results[0] if results else None
        asr_text = str(getattr(first, "text", "") or "").strip()

        time_stamps = getattr(first, "time_stamps", None) if first is not None else None
        ts_items = getattr(time_stamps, "items", []) if time_stamps is not None else []
        alignment_result = [
            SimpleNamespace(
                start_time=float(getattr(item, "start_time", 0.0)),
                end_time=float(getattr(item, "end_time", 0.0)),
                text=str(getattr(item, "text", "")),
            )
            for item in ts_items
        ]
    # result = generate_transcription(
    #     model=model,
    #     audio_path=args.audio,
    #     format="txt",
    #     verbose=True,
    # )

    def _build_sentence_segments():
        punct = set("，。！？；：、,.!?;:…")
        if not alignment_result:
            return []

        def _norm_char(ch: str) -> str:
            if "A" <= ch <= "Z":
                return ch.lower()
            return ch

        asr_clean = []
        punct_positions = set()
        for ch in asr_text:
            if ch.isspace():
                continue
            if ch in punct:
                if asr_clean:
                    punct_positions.add(len(asr_clean) - 1)
                continue
            asr_clean.append(_norm_char(ch))

        align_clean = []
        align_char_token = []
        for token_idx, item in enumerate(alignment_result):
            token_text = str(item.text)
            for ch in token_text:
                if ch.isspace() or ch in punct:
                    continue
                align_clean.append(_norm_char(ch))
                align_char_token.append(token_idx)

        token_boundaries = set()
        asr_idx = 0
        for align_idx, ch in enumerate(align_clean):
            while asr_idx < len(asr_clean) and asr_clean[asr_idx] != ch:
                asr_idx += 1
            if asr_idx >= len(asr_clean):
                break
            if asr_idx in punct_positions:
                token_boundaries.add(align_char_token[align_idx])
            asr_idx += 1

        segments = []
        cur_text = []
        cur_start = None
        cur_end = None
        for token_idx, item in enumerate(alignment_result):
            if cur_start is None:
                cur_start = item.start_time
            cur_end = item.end_time
            cur_text.append(str(item.text))
            if token_idx in token_boundaries:
                text = "".join(cur_text).strip()
                if text:
                    segments.append(
                        {
                            "start": cur_start,
                            "end": cur_end,
                            "text": text,
                        }
                    )
                cur_text = []
                cur_start = None
                cur_end = None

        if cur_text and cur_start is not None and cur_end is not None:
            text = "".join(cur_text).strip()
            if text:
                segments.append(
                    {
                        "start": cur_start,
                        "end": cur_end,
                        "text": text,
                    }
                )

        return segments

    sentence_segments = _build_sentence_segments()

    # for item in alignment_result:
    #     print(f"  [{item.start_time}s - {item.end_time}s] {item.text}")

    def _format_ass_time(seconds: float) -> str:
        total_cs = int(round(seconds * 100))
        cs = total_cs % 100
        total_s = total_cs // 100
        s = total_s % 60
        total_m = total_s // 60
        m = total_m % 60
        h = total_m // 60
        return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

    def _format_srt_time(seconds: float) -> str:
        total_ms = int(round(seconds * 1000))
        ms = total_ms % 1000
        total_s = total_ms // 1000
        s = total_s % 60
        total_m = total_s // 60
        m = total_m % 60
        h = total_m // 60
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def _write_ass(path: str) -> None:
        header = (
            "[Script Info]\n"
            "ScriptType: v4.00+\n"
            "\n"
            "[V4+ Styles]\n"
            "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,"
            "Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,"
            "Alignment,MarginL,MarginR,MarginV,Encoding\n"
            f"Style: {args.ass_style}\n"
            "\n"
            "[Events]\n"
            "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(header)
            for item in sentence_segments:
                start = _format_ass_time(item["start"])
                end = _format_ass_time(item["end"])
                text = str(item["text"]).replace("\n", " ").replace("\r", " ")
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")

    def _write_srt(path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            for idx, item in enumerate(sentence_segments, start=1):
                start = _format_srt_time(item["start"])
                end = _format_srt_time(item["end"])
                text = str(item["text"]).replace("\n", " ").replace("\r", " ")
                f.write(f"{idx}\n{start} --> {end}\n{text}\n\n")

    def _replace_ext(path: str, ext: str) -> str:
        base, _ = os.path.splitext(path)
        return f"{base}.{ext}"

    fmt = args.output_format
    if fmt in ("ass", "srt", "both", "all") and not args.output:
        raise ValueError("输出格式包含字幕文件时必须提供 --output")

    if fmt in ("txt", "both", "all"):
        if args.output:
            txt_path = _replace_ext(args.output, "txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(asr_text)
            print(f"STT Saved: {txt_path}")
        else:
            print(asr_text)

    if fmt in ("ass", "both", "all"):
        ass_path = _replace_ext(args.output, "ass")
        _write_ass(ass_path)
        print(f"STT Saved: {ass_path}")

    if fmt in ("srt", "all"):
        srt_path = _replace_ext(args.output, "srt")
        _write_srt(srt_path)

    # Output result as JSON
    result_data = {
        "text": asr_text,
        "duration": round(total_sec, 3),
        "sample_rate": sr,
        "files": [],
        "success": True
    }
    if args.output:
        if fmt in ("txt", "both", "all"):
            result_data["files"].append(os.path.abspath(_replace_ext(args.output, "txt")))
        if fmt in ("ass", "both", "all"):
            result_data["files"].append(os.path.abspath(_replace_ext(args.output, "ass")))
        if fmt in ("srt", "all"):
            result_data["files"].append(os.path.abspath(_replace_ext(args.output, "srt")))
    print(json.dumps(result_data, ensure_ascii=False))

# Voices directory management
def get_voices_dir() -> str:
    """Get the voices directory path at skill root level, create if not exists."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)  # Go up from scripts/ to skill root
    voices_dir = os.path.join(skill_dir, "voices")
    os.makedirs(voices_dir, exist_ok=True)
    return voices_dir

def get_voice_path(voice_id: str) -> dict | None:
    """Get voice file paths by voice_id. Returns dict with ref_audio, ref_text and instruct, or None if not found."""
    voices_dir = get_voices_dir()
    voice_dir = os.path.join(voices_dir, voice_id)
    if not os.path.isdir(voice_dir):
        return None

    ref_audio = os.path.join(voice_dir, "ref_audio.wav")
    ref_text_path = os.path.join(voice_dir, "ref_text.txt")
    instruct_path = os.path.join(voice_dir, "ref_instruct.txt")

    if not os.path.exists(ref_audio):
        return None

    ref_text = ""
    if os.path.exists(ref_text_path):
        with open(ref_text_path, "r", encoding="utf-8") as f:
            ref_text = f.read().strip()

    instruct = ""
    if os.path.exists(instruct_path):
        with open(instruct_path, "r", encoding="utf-8") as f:
            instruct = f.read().strip()

    return {
        "ref_audio": ref_audio,
        "ref_text": ref_text,
        "instruct": instruct
    }

def run_voice_create(args: argparse.Namespace) -> None:
    """Create a new voice by generating audio and saving reference info."""
    voices_dir = get_voices_dir()
    voice_id = args.id or str(uuid.uuid4())[:8]
    voice_dir = os.path.join(voices_dir, voice_id)
    os.makedirs(voice_dir, exist_ok=True)

    # Normalize text: replace newlines with spaces
    text = _normalize_text(args.text)
    instruct = _normalize_text(args.instruct) if args.instruct else None

    if not instruct:
        raise ValueError("--instruct 参数是必需的，请提供语音风格描述")

    # Generate audio using TTS
    output_audio = os.path.join(voice_dir, "ref_audio.wav")

    # Run TTS to generate the audio (always use VoiceDesign model for voice creation)
    if IS_DARWIN:
        _ensure_mlx_audio()
        from mlx_audio.tts.utils import load_model as load_tts_model

        model = load_tts_model(DEFAULT_VOICEDESIGN_MODEL)
        kwargs = {
            "text": text,
            "language": args.language,
            "instruct": instruct,
        }
        results = list(model.generate(**kwargs))
        if not results:
            raise RuntimeError("TTS Failed：未返回音频结果")
        result = results[0]
        sample_rate = _get_sample_rate(result, model)
        audio_np = np.array(result.audio, dtype=np.float32)
    else:
        model = _get_qwen_tts_model(DEFAULT_VOICEDESIGN_MODEL)
        wavs, sample_rate = model.generate_voice_design(
            text=text,
            language=args.language,
            instruct=instruct,
        )
        if wavs is None:
            raise RuntimeError("TTS Failed：未返回音频结果")
        audio = wavs[0] if isinstance(wavs, (list, tuple)) else wavs
        audio_np = np.array(audio, dtype=np.float32)
        if audio_np.ndim > 1:
            audio_np = audio_np.reshape(-1)
        sample_rate = int(sample_rate) if sample_rate else 24000

    sf.write(output_audio, audio_np, sample_rate)

    # Save reference text
    ref_text_path = os.path.join(voice_dir, "ref_text.txt")
    with open(ref_text_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Save instruct
    instruct_path = os.path.join(voice_dir, "ref_instruct.txt")
    with open(instruct_path, "w", encoding="utf-8") as f:
        f.write(instruct)

    # Calculate duration
    duration = len(audio_np) / sample_rate

    # Output result as JSON
    result_data = {
        "id": voice_id,
        "ref_audio": output_audio,
        "ref_text": text,
        "instruct": instruct,
        "duration": round(duration, 3),
        "sample_rate": sample_rate,
        "success": True
    }
    print(json.dumps(result_data, ensure_ascii=False))

def run_voice_list(args: argparse.Namespace) -> None:
    """List all created voices."""
    voices_dir = get_voices_dir()
    voices = []

    if os.path.exists(voices_dir):
        for voice_id in sorted(os.listdir(voices_dir)):
            voice_dir = os.path.join(voices_dir, voice_id)
            if os.path.isdir(voice_dir):
                ref_audio = os.path.join(voice_dir, "ref_audio.wav")
                ref_text_path = os.path.join(voice_dir, "ref_text.txt")
                instruct_path = os.path.join(voice_dir, "ref_instruct.txt")

                ref_text = ""
                if os.path.exists(ref_text_path):
                    with open(ref_text_path, "r", encoding="utf-8") as f:
                        ref_text = f.read().strip()

                instruct = ""
                if os.path.exists(instruct_path):
                    with open(instruct_path, "r", encoding="utf-8") as f:
                        instruct = f.read().strip()

                if os.path.exists(ref_audio):
                    # Get audio info
                    audio_data, sr = sf.read(ref_audio)
                    duration = len(audio_data) / sr

                    voices.append({
                        "id": voice_id,
                        "ref_audio": ref_audio,
                        "ref_text": ref_text,
                        "instruct": instruct,
                        "duration": round(duration, 3),
                        "sample_rate": sr
                    })
    if len(voices) == 0:
        print("(not found any voices, use 'voice create' command to create one)")
        return
    # Output result as JSON
    print(json.dumps(voices, ensure_ascii=False, indent=2))

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="MLX-Audio CLI (TTS + STT)",
    )
    # parser.add_argument("--test", action="store_true", help="使用默认测试参数")
    parser.add_argument(
        "--hf-mirror",
        dest="hf_mirror",
        action="store_true",
        help="使用 hf-mirror 镜像站（默认）",
    )
    parser.add_argument(
        "--no-hf-mirror",
        dest="hf_mirror",
        action="store_false",
        help="不使用 hf-mirror 镜像站",
    )
    parser.set_defaults(hf_mirror=True)
    subparsers = parser.add_subparsers(dest="command", required=True)

    tts = subparsers.add_parser("tts", help="Text-to-Speech")
    tts.add_argument("--text", help="要合成的文本")
    tts.add_argument("--output", help="输出音频路径 (WAV)")
    tts.add_argument("--model", default=DEFAULT_TTS_MODEL, help="TTS 模型")
    tts.add_argument("--voice", default="Chelsie", help="TTS 语音角色")
    tts.add_argument("--language", default="English", help="TTS 语言")
    tts.add_argument("--speaker", default="Vivian", help="音色")
    tts.add_argument("--ref_voice", help="音色ID（使用 voice create 创建的音色）")
    tts.add_argument("--ref_audio", help="参考音频路径，用于克隆")
    tts.add_argument("--ref_text", help="参考文本，用于克隆")
    tts.add_argument("--instruct", default=None, help="语音风格指令（用于VoiceDesign模型）")
    tts.set_defaults(func=run_tts)

    stt = subparsers.add_parser("stt", help="Speech-to-Text")
    stt.add_argument("--audio", help="输入音频路径")
    stt.add_argument("--model", default=DEFAULT_STT_MODEL, help="STT 模型")
    stt.add_argument("--aligner-model", default=DEFAULT_ALIGNER_MODEL, help="STT 对齐模型")
    stt.add_argument("--language", default="English", help="STT 语言")
    stt.add_argument("--output", help="输出文本路径 (可选)")
    # stt.add_argument("--chunks-dir", help="裁剪后的音频片段输出目录")
    stt.add_argument(
        "--output-format",
        default="txt",
        choices=["txt", "ass", "srt", "all"],
        help="输出格式: txt / ass / srt / all",
    )
    stt.add_argument(
        "--ass-style",
        default="Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,"
        "-1,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1",
        help="ASS 样式行（Style: 后的内容）",
    )
    stt.set_defaults(func=run_stt)

    # Voice management commands
    voice = subparsers.add_parser("voice", help="Voice management")
    voice_subparsers = voice.add_subparsers(dest="voice_command", required=True)

    # voice create
    voice_create = voice_subparsers.add_parser("create", help="Create a new voice")
    voice_create.add_argument("--text", required=True, help="参考文本")
    voice_create.add_argument("--instruct", required=True, help="语音风格描述（必需，用于VoiceDesign模型）")
    voice_create.add_argument("--id", help="音色ID (可选，默认自动生成)")
    voice_create.add_argument("--language", default="English", help="TTS 语言")
    voice_create.set_defaults(func=run_voice_create)

    # voice list
    voice_list = voice_subparsers.add_parser("list", help="List all created voices")
    voice_list.set_defaults(func=run_voice_list)

    return parser


def main() -> None:
    # os.environ["HTTP_PROXY"] = "http://127.0.0.1:10809"
    # os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10809"

    # os.environ["HF_HUB_OFFLINE"] = "1"
    parser = build_parser()
    args = parser.parse_args()
    _configure_hf(args)
    args.func(args)


if __name__ == "__main__":
    main()
