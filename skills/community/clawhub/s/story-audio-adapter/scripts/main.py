#!/usr/bin/env python3
"""
Story Audio Adapter CLI.

职责：
- 读取用户可编辑音色库
- 解析带 [角色] 标记的故事文本
- 基于启发式规则产出角色分析和音色匹配
- 调用 SenseAudio TTS 为每段内容生成音频
- 将所有 wav 片段按顺序拼接成完整作品
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import wave
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


def ensure_python_package(import_name: str, pip_name: Optional[str] = None) -> None:
    pip_name = pip_name or import_name
    try:
        importlib.import_module(import_name)
        return
    except ImportError:
        print(f"缺少 {pip_name}，正在自动安装...", file=sys.stderr)

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", pip_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"自动安装 {pip_name} 失败，请手动执行: {sys.executable} -m pip install {pip_name}\n"
            f"{result.stderr.strip()}"
        )

    importlib.import_module(import_name)


ensure_python_package("requests")
import requests


DEFAULT_API_BASE = "https://api.senseaudio.cn"
TTS_API_PATH = "/v1/t2a_v2"
DEFAULT_MODEL = "SenseAudio-TTS-1.0"
DEFAULT_OUTPUT_FORMAT = "wav"
DEFAULT_SAMPLE_RATE = 32000
DEFAULT_BITRATE = 128000
DEFAULT_CHANNEL = 1
DEFAULT_SPEED = 1.0
DEFAULT_VOL = 1.0
DEFAULT_PITCH = 0
MAX_TEXT_LENGTH = 10000

SKILL_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = SKILL_DIR.parent.parent
VOICE_LIBRARY_PATH = SKILL_DIR / "references" / "voice_library.json"
OUTPUT_DIR = WORKSPACE_DIR / "outputs"


class APIError(Exception):
    pass


@dataclass
class VoiceProfile:
    voice_id: str
    description: str
    age_hint: str = ""
    gender_hint: str = ""
    temperament: List[str] = None
    recommended_for: List[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VoiceProfile":
        return cls(
            voice_id=str(data.get("voice_id") or "").strip(),
            description=str(data.get("description") or "").strip(),
            age_hint=str(data.get("age_hint") or "").strip(),
            gender_hint=str(data.get("gender_hint") or "").strip(),
            temperament=[str(item).strip() for item in data.get("temperament") or [] if str(item).strip()],
            recommended_for=[str(item).strip() for item in data.get("recommended_for") or [] if str(item).strip()],
        )


@dataclass
class StorySegment:
    index: int
    role_name: str
    text: str


@dataclass
class RoleAnalysis:
    role_name: str
    line_count: int
    traits: Dict[str, Any]
    voice_match: Dict[str, Any]


@dataclass
class SynthesisArtifact:
    segment_index: int
    role_name: str
    voice_id: str
    text: str
    audio_path: str


class SenseAudioClient:
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        self.api_key = (api_key or os.getenv("SENSEAUDIO_API_KEY", "")).strip()
        self.api_base = (api_base or os.getenv("SENSEAUDIO_API_BASE", DEFAULT_API_BASE)).rstrip("/")

    @property
    def headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise APIError(missing_key_message())
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def auth_check(self) -> Dict[str, Any]:
        if not self.api_key:
            raise APIError(missing_key_message())
        return {
            "configured": True,
            "api_base": self.api_base,
            "message": "已检测到 SENSEAUDIO_API_KEY。"
        }

    def synthesize(self, *, text: str, voice_id: str, output_path: Path) -> Dict[str, Any]:
        validate_text(text)
        payload = {
            "model": DEFAULT_MODEL,
            "text": text,
            "stream": False,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": DEFAULT_SPEED,
                "vol": DEFAULT_VOL,
                "pitch": DEFAULT_PITCH,
            },
            "audio_setting": {
                "format": DEFAULT_OUTPUT_FORMAT,
                "sample_rate": DEFAULT_SAMPLE_RATE,
                "bitrate": DEFAULT_BITRATE,
                "channel": DEFAULT_CHANNEL,
            },
        }
        try:
            response = requests.post(
                f"{self.api_base}{TTS_API_PATH}",
                headers=self.headers,
                json=payload,
                timeout=300,
            )
        except requests.exceptions.RequestException as exc:
            raise APIError(f"TTS 请求失败: {exc}") from exc

        parsed = handle_json_response(response)
        audio_hex = ((parsed.get("data") or {}).get("audio") or "").strip()
        if not audio_hex:
            raise APIError("TTS 返回成功但 `data.audio` 为空。")

        try:
            audio_bytes = bytes.fromhex(audio_hex)
        except ValueError as exc:
            raise APIError("TTS 返回的音频数据不是合法 hex。") from exc

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(audio_bytes)
        return parsed


def missing_key_message() -> str:
    return (
        "未检测到 `SENSEAUDIO_API_KEY`。\n"
        "请先配置：\n"
        'export SENSEAUDIO_API_KEY="YOUR_API_KEY"\n'
        'export SENSEAUDIO_API_BASE="https://api.senseaudio.cn"'
    )


def handle_json_response(response: requests.Response) -> Dict[str, Any]:
    if response.status_code in (401, 403):
        raise APIError("认证失败：`SENSEAUDIO_API_KEY` 无效、过期或无权限。")
    if response.status_code == 429:
        raise APIError("请求频率过高，接口返回 HTTP 429。")
    if response.status_code >= 400:
        raise APIError(f"HTTP {response.status_code}: {response.text[:500]}")
    try:
        parsed = response.json()
    except ValueError as exc:
        raise APIError(f"接口返回了非 JSON 内容: {response.text[:300]}") from exc
    base_resp = parsed.get("base_resp")
    if isinstance(base_resp, dict) and base_resp.get("status_code", 0) not in (0, None):
        raise APIError(f"{base_resp.get('status_code')}: {base_resp.get('status_msg')}")
    if isinstance(parsed, dict) and parsed.get("code") and parsed.get("message"):
        raise APIError(f"{parsed['code']}: {parsed['message']}")
    return parsed


def validate_text(text: str) -> None:
    if not text.strip():
        raise APIError("文本不能为空。")
    if len(text) > MAX_TEXT_LENGTH:
        raise APIError(f"单段文本超过 {MAX_TEXT_LENGTH} 字符，请先拆段。")


def load_voice_library(path: Path = VOICE_LIBRARY_PATH) -> List[VoiceProfile]:
    if not path.exists():
        raise APIError(f"音色库不存在: {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    voices = [VoiceProfile.from_dict(item) for item in raw.get("voices") or []]
    voices = [voice for voice in voices if voice.voice_id and voice.description]
    if not voices:
        raise APIError("音色库为空，请先编辑 references/voice_library.json。")
    return voices


def parse_story_text(text: str) -> List[StorySegment]:
    pattern = re.compile(r"^\s*\[(?P<role>[^\]]+)\]\s*(?P<text>.*)\s*$")
    segments: List[StorySegment] = []
    pending_role = "旁白"
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = pattern.match(line)
        if match:
            role = match.group("role").strip() or "旁白"
            content = match.group("text").strip()
            pending_role = role
        else:
            role = pending_role if segments else "旁白"
            content = line
        if not content:
            continue
        segments.append(StorySegment(index=len(segments), role_name=role, text=content))
    if not segments:
        raise APIError("未解析到有效故事片段，请检查输入格式。")
    return segments


def summarize_role_traits(role_name: str, texts: Sequence[str]) -> Dict[str, Any]:
    joined = " ".join(texts)
    lower = joined.lower()
    personality: List[str] = []
    emotion = "平稳"
    age_hint = "信息不足"
    gender_hint = "信息不足"

    if role_name == "旁白":
        personality.extend(["沉稳", "叙述性"])
        age_hint = "成年"
        gender_hint = "中性"

    keyword_map = [
        ("哈哈", "活泼", "开心"),
        ("笑", "轻快", "开心"),
        ("哭", "脆弱", "悲伤"),
        ("冷", "克制", "冷静"),
        ("杀", "强硬", "紧张"),
        ("师父", "尊敬", "平稳"),
        ("哥哥", "依赖", "柔和"),
        ("我不怕", "倔强", "坚定"),
        ("闭嘴", "攻击性", "激烈"),
    ]
    for marker, trait, inferred_emotion in keyword_map:
        if marker in joined and trait not in personality:
            personality.append(trait)
            emotion = inferred_emotion

    if any(token in role_name for token in ["男", "少年", "青年", "父", "哥"]):
        gender_hint = "男性"
    if any(token in role_name for token in ["女", "少女", "母", "姐"]):
        gender_hint = "女性"
    if any(token in role_name for token in ["孩", "童", "宝宝"]):
        age_hint = "儿童"
    elif any(token in role_name for token in ["青年", "少"]):
        age_hint = "青年"
    elif age_hint == "信息不足":
        age_hint = "成年" if role_name == "旁白" else "信息不足"

    if "!" in joined or "！" in joined:
        emotion = "激动" if emotion == "平稳" else emotion
    if not personality:
        personality = ["信息不足"] if role_name != "旁白" and not lower else ["克制"]

    return {
        "age_hint": age_hint,
        "gender_hint": gender_hint,
        "personality": personality,
        "emotion": emotion,
        "narrative_function": infer_narrative_function(role_name),
    }


def infer_narrative_function(role_name: str) -> str:
    if role_name == "旁白":
        return "承担叙事推进和场景说明"
    if any(token in role_name for token in ["主角", "男主", "女主"]):
        return "主要人物"
    return "次要人物或场景角色"


def score_voice(traits: Dict[str, Any], voice: VoiceProfile, role_name: str) -> Tuple[int, str]:
    score = 0
    reasons: List[str] = []

    age_hint = traits.get("age_hint")
    gender_hint = traits.get("gender_hint")
    personality = traits.get("personality") or []
    emotion = traits.get("emotion") or ""

    if age_hint != "信息不足" and voice.age_hint and age_hint in voice.age_hint:
        score += 3
        reasons.append(f"年龄感接近 {voice.age_hint}")
    if gender_hint != "信息不足" and voice.gender_hint and gender_hint in voice.gender_hint:
        score += 2
        reasons.append(f"性别倾向接近 {voice.gender_hint}")
    if role_name == "旁白" and "旁白" in voice.recommended_for:
        score += 4
        reasons.append("音色描述明确适合旁白")
    for item in personality:
        if item != "信息不足" and any(item in temper for temper in voice.temperament + voice.recommended_for):
            score += 2
            reasons.append(f"气质匹配 {item}")
    if emotion and any(emotion in value for value in [voice.description] + voice.temperament):
        score += 1
        reasons.append(f"情绪基调接近 {emotion}")
    if not reasons:
        reasons.append("在当前音色库中属于相对可用的近似匹配")
    return score, "；".join(dict.fromkeys(reasons))


def build_role_analyses(segments: Sequence[StorySegment], voices: Sequence[VoiceProfile]) -> List[RoleAnalysis]:
    role_to_texts: Dict[str, List[str]] = {}
    for segment in segments:
        role_to_texts.setdefault(segment.role_name, []).append(segment.text)

    analyses: List[RoleAnalysis] = []
    used_voice_ids: Dict[str, int] = {}
    for role_name, texts in role_to_texts.items():
        traits = summarize_role_traits(role_name, texts)
        ranked: List[Tuple[int, VoiceProfile, str]] = []
        for voice in voices:
            score, reason = score_voice(traits, voice, role_name)
            reuse_penalty = used_voice_ids.get(voice.voice_id, 0)
            ranked.append((score - reuse_penalty, voice, reason))
        ranked.sort(key=lambda item: item[0], reverse=True)
        best_score, best_voice, best_reason = ranked[0]
        used_voice_ids[best_voice.voice_id] = used_voice_ids.get(best_voice.voice_id, 0) + 1
        if used_voice_ids[best_voice.voice_id] > 1:
            best_reason = f"{best_reason}；当前音色库有限，因此复用该音色"
        analyses.append(
            RoleAnalysis(
                role_name=role_name,
                line_count=len(texts),
                traits=traits,
                voice_match={
                    "voice_id": best_voice.voice_id,
                    "description": best_voice.description,
                    "reason": best_reason,
                    "score": best_score,
                },
            )
        )
    analyses.sort(key=lambda item: (0 if item.role_name == "旁白" else 1, item.role_name))
    return analyses


def analysis_payload(analyses: Sequence[RoleAnalysis]) -> Dict[str, Any]:
    return {
        "role_count": len(analyses),
        "roles": [asdict(item) for item in analyses],
        "notes": [
            "角色与音色匹配基于当前文本线索和本地音色库启发式判断。",
            "如需更准确的匹配，可扩展 references/voice_library.json 后重新执行。",
        ],
    }


def create_run_dir(output_dir: Optional[Path] = None) -> Path:
    if output_dir is not None:
        target = output_dir
    else:
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        target = OUTPUT_DIR / f"story-{stamp}"
    target.mkdir(parents=True, exist_ok=True)
    return target


def synthesize_story(
    *,
    text: str,
    output_dir: Optional[Path],
    api_key: Optional[str],
    api_base: Optional[str],
) -> Dict[str, Any]:
    voices = load_voice_library()
    segments = parse_story_text(text)
    analyses = build_role_analyses(segments, voices)
    role_to_voice = {item.role_name: item.voice_match["voice_id"] for item in analyses}

    run_dir = create_run_dir(output_dir)
    analysis_path = run_dir / "role_analysis.json"
    mapping_path = run_dir / "voice_mapping.json"
    segment_manifest_path = run_dir / "segment_manifest.json"
    segment_dir = run_dir / "segments"
    meta_dir = run_dir / "meta"
    segment_dir.mkdir(exist_ok=True)
    meta_dir.mkdir(exist_ok=True)

    client = SenseAudioClient(api_key=api_key, api_base=api_base)
    artifacts: List[SynthesisArtifact] = []
    segment_wavs: List[Path] = []
    for segment in segments:
        voice_id = role_to_voice[segment.role_name]
        wav_path = segment_dir / f"{segment.index:04d}-{safe_name(segment.role_name)}.wav"
        meta_path = meta_dir / f"{segment.index:04d}-{safe_name(segment.role_name)}.json"
        response_json = client.synthesize(text=segment.text, voice_id=voice_id, output_path=wav_path)
        meta_path.write_text(json.dumps(response_json, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts.append(
            SynthesisArtifact(
                segment_index=segment.index,
                role_name=segment.role_name,
                voice_id=voice_id,
                text=segment.text,
                audio_path=str(wav_path),
            )
        )
        segment_wavs.append(wav_path)

    final_audio_path = run_dir / "story-full.wav"
    concat_wavs(segment_wavs, final_audio_path)
    media_audio_path = maybe_export_mp3(final_audio_path) or final_audio_path

    analysis_path.write_text(
        json.dumps(analysis_payload(analyses), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    mapping_path.write_text(
        json.dumps(role_to_voice, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    segment_manifest_path.write_text(
        json.dumps([asdict(item) for item in artifacts], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    payload = {
        "output_dir": str(run_dir),
        "role_analysis": str(analysis_path),
        "voice_mapping": str(mapping_path),
        "segment_manifest": str(segment_manifest_path),
        "final_audio": str(final_audio_path),
        "media_audio": str(media_audio_path),
    }
    media_ref = build_media_reference(media_audio_path)
    if media_ref:
        payload["media_ref"] = media_ref
    return payload


def concat_wavs(inputs: Sequence[Path], output: Path) -> None:
    if not inputs:
        raise APIError("没有可拼接的音频片段。")

    normalized_params = None
    normalized_frames = []

    for path in inputs:
        with wave.open(str(path), "rb") as current:
            current_params = current.getparams()
            current_frames = current.readframes(current.getnframes())

            if normalized_params is None:
                normalized_params = current_params
                normalized_frames.append(current_frames)
                continue

            if current_params[:4] == normalized_params[:4]:
                normalized_frames.append(current_frames)
                continue

            import audioop

            converted = current_frames
            if current_params.sampwidth != normalized_params.sampwidth:
                converted = audioop.lin2lin(converted, current_params.sampwidth, normalized_params.sampwidth)

            if current_params.nchannels != normalized_params.nchannels:
                if current_params.nchannels == 1 and normalized_params.nchannels == 2:
                    converted = audioop.tostereo(converted, normalized_params.sampwidth, 1, 1)
                elif current_params.nchannels == 2 and normalized_params.nchannels == 1:
                    converted = audioop.tomono(converted, normalized_params.sampwidth, 0.5, 0.5)
                else:
                    raise APIError(f"不支持的声道转换: {path}")

            if current_params.framerate != normalized_params.framerate:
                converted, _ = audioop.ratecv(
                    converted,
                    normalized_params.sampwidth,
                    normalized_params.nchannels,
                    current_params.framerate,
                    normalized_params.framerate,
                    None,
                )

            normalized_frames.append(converted)

    with wave.open(str(output), "wb") as merged:
        merged.setparams(normalized_params)
        for chunk in normalized_frames:
            merged.writeframes(chunk)


def maybe_export_mp3(wav_path: Path) -> Optional[Path]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return None

    mp3_path = wav_path.with_suffix(".mp3")
    result = subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i",
            str(wav_path),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "128k",
            str(mp3_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0 or not mp3_path.exists():
        return None
    return mp3_path


def build_media_reference(path: Path) -> Optional[str]:
    try:
        relative = path.resolve().relative_to(WORKSPACE_DIR.resolve())
    except ValueError:
        return None
    return f"MEDIA:./{relative.as_posix()}"


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", value).strip("-")
    return cleaned or "segment"


def load_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.text_file:
        return Path(args.text_file).expanduser().read_text(encoding="utf-8")
    raise APIError("必须提供 --text 或 --text-file。")


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_auth_check(args: argparse.Namespace) -> int:
    client = SenseAudioClient(api_key=args.api_key, api_base=args.api_base)
    print_json(client.auth_check())
    return 0


def cmd_list_voices(args: argparse.Namespace) -> int:
    voices = load_voice_library()
    payload = {
        "voice_count": len(voices),
        "voices": [asdict(item) for item in voices],
        "library_path": str(VOICE_LIBRARY_PATH),
    }
    print_json(payload)
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    text = load_text(args)
    voices = load_voice_library()
    segments = parse_story_text(text)
    analyses = build_role_analyses(segments, voices)
    payload = analysis_payload(analyses)
    print_json(payload)
    return 0


def cmd_synthesize_story(args: argparse.Namespace) -> int:
    text = load_text(args)
    payload = synthesize_story(
        text=text,
        output_dir=Path(args.output_dir).expanduser() if args.output_dir else None,
        api_key=args.api_key,
        api_base=args.api_base,
    )
    print_json(payload)
    media_ref = payload.get("media_ref")
    if media_ref:
        print(media_ref)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Story Audio Adapter CLI")
    parser.add_argument("--api-key", help="覆盖环境变量 SENSEAUDIO_API_KEY")
    parser.add_argument("--api-base", help="覆盖环境变量 SENSEAUDIO_API_BASE")
    subparsers = parser.add_subparsers(dest="command", required=True)

    auth_parser = subparsers.add_parser("auth-check", help="检查 API Key 是否配置")
    auth_parser.set_defaults(func=cmd_auth_check)

    voices_parser = subparsers.add_parser("list-voices", help="列出当前音色库")
    voices_parser.set_defaults(func=cmd_list_voices)

    analyze_parser = subparsers.add_parser("analyze", help="分析角色并匹配音色")
    analyze_parser.add_argument("--text", help="直接传入故事文本")
    analyze_parser.add_argument("--text-file", help="故事文本文件路径")
    analyze_parser.set_defaults(func=cmd_analyze)

    synth_parser = subparsers.add_parser("synthesize-story", help="生成完整故事音频")
    synth_parser.add_argument("--text", help="直接传入故事文本")
    synth_parser.add_argument("--text-file", help="故事文本文件路径")
    synth_parser.add_argument("--output-dir", help="自定义输出目录")
    synth_parser.set_defaults(func=cmd_synthesize_story)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except APIError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("ERROR: 用户中断执行。", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
