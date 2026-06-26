#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频字幕生成 Skill 脚本
输入视频/音频 → SenseAudio ASR 识别 → 生成 SRT 字幕 → 可选翻译 → 可选烧入视频

内容总结由 Claude 直接完成，本脚本不调用外部 LLM。
"""

import os
import re
import json
import argparse
import subprocess
import requests
import time
import math
import tempfile
import sys

# ============== 配置 ==============
SENSEAUDIO_API_KEY = os.environ.get("SENSEAUDIO_API_KEY", "")
ASR_API_URL = "https://api.senseaudio.cn/v1/audio/transcriptions"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# ASR 模型选择
ASR_MODELS = {
    "lite": "sense-asr-lite",
    "standard": "sense-asr",
    "pro": "sense-asr-pro",
    "deepthink": "sense-asr-deepthink",
}

# 支持的语言
SUPPORTED_LANGUAGES = [
    "zh", "en", "ja", "ko", "fr", "de", "es", "pt", "ru", "it",
    "ar", "yue", "nl", "id", "ms", "th", "tr", "ur", "vi",
]


def extract_audio(video_path: str, output_audio: str, sample_rate: int = 16000) -> str:
    """使用 ffmpeg 从视频中提取音频，转为单声道 wav"""
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-ac", "1", "-ar", str(sample_rate),
        "-acodec", "pcm_s16le", output_audio,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg 提取音频失败:\n{result.stderr}")
    return output_audio


def get_audio_duration(file_path: str) -> float:
    """获取音频/视频时长（秒）"""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", file_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe 获取时长失败:\n{result.stderr}")
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def split_audio(audio_path: str, chunk_duration: int = 55, output_dir: str = None) -> list:
    """将音频按指定时长切片（应对 10MB 限制）"""
    total_duration = get_audio_duration(audio_path)
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="subtitle_chunks_")

    file_size = os.path.getsize(audio_path)
    if file_size < MAX_FILE_SIZE:
        return [(audio_path, 0.0)]

    chunks = []
    num_chunks = math.ceil(total_duration / chunk_duration)

    for i in range(num_chunks):
        start_time = i * chunk_duration
        chunk_path = os.path.join(output_dir, f"chunk_{i:04d}.wav")
        cmd = [
            "ffmpeg", "-y", "-i", audio_path,
            "-ss", str(start_time), "-t", str(chunk_duration),
            "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000",
            chunk_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  警告: 切片 {i} 失败: {result.stderr[:100]}")
            continue
        if os.path.getsize(chunk_path) > 0:
            chunks.append((chunk_path, start_time))

    return chunks


def asr_recognize(audio_path: str, api_key: str, model: str = "sense-asr",
                  language: str = None, target_language: str = None,
                  enable_speaker: bool = False, enable_sentiment: bool = False) -> dict:
    """调用 SenseAudio ASR API 识别音频"""
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"file": (os.path.basename(audio_path), open(audio_path, "rb"))}
    data = {"model": model, "response_format": "verbose_json"}

    timestamp_granularities = []
    if model in ("sense-asr", "sense-asr-pro"):
        timestamp_granularities = [("timestamp_granularities[]", "segment")]
        data["enable_punctuation"] = "true"

    if language and model != "sense-asr-deepthink":
        data["language"] = language
    if target_language and model != "sense-asr-lite":
        data["target_language"] = target_language
    if enable_speaker and model in ("sense-asr", "sense-asr-pro"):
        data["enable_speaker_diarization"] = "true"
    if enable_sentiment and model in ("sense-asr", "sense-asr-pro"):
        data["enable_sentiment"] = "true"

    data_tuples = [(k, v) for k, v in data.items()]
    data_tuples.extend(timestamp_granularities)

    for retry in range(3):
        try:
            resp = requests.post(ASR_API_URL, headers=headers, files=files,
                                 data=data_tuples, timeout=120)
            if resp.status_code == 429:
                wait = 10 * (retry + 1)
                print(f"  速率限制，等待 {wait}s...")
                time.sleep(wait)
                files["file"] = (os.path.basename(audio_path), open(audio_path, "rb"))
                continue
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"  ASR 重试 {retry+1}/3: {e}")
            time.sleep(5 * (retry + 1))
            files["file"] = (os.path.basename(audio_path), open(audio_path, "rb"))
    raise RuntimeError(f"ASR 识别失败: {audio_path}")


def format_srt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def split_segment_by_punctuation(seg_text: str, seg_start: float, seg_end: float,
                                  max_chars: int = 18) -> list:
    """将一个长 segment 按标点拆成短句，时间按字数比例分配"""
    if not seg_text.strip():
        return []

    total_duration = seg_end - seg_start
    total_chars = len(seg_text.replace(" ", ""))
    if total_chars == 0:
        return []

    parts = re.split(r'([。！？!?；;])', seg_text)
    chunks = []
    for i, part in enumerate(parts):
        if not part:
            continue
        if part in "。！？!?；;" and chunks:
            chunks[-1] += part
        else:
            chunks.append(part)

    fine_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_chars:
            fine_chunks.append(chunk)
        else:
            sub_parts = re.split(r'([，,、：:])', chunk)
            sub_chunks = []
            for sp in sub_parts:
                if not sp:
                    continue
                if sp in "，,、：:" and sub_chunks:
                    sub_chunks[-1] += sp
                else:
                    sub_chunks.append(sp)
            merged = []
            buf = ""
            for sc in sub_chunks:
                buf += sc
                if len(buf) >= 5:
                    merged.append(buf)
                    buf = ""
            if buf:
                if merged:
                    merged[-1] += buf
                else:
                    merged.append(buf)
            fine_chunks.extend(merged)

    entries = []
    char_offset = 0
    for chunk in fine_chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        chunk_chars = len(chunk)
        chunk_start = seg_start + (char_offset / total_chars) * total_duration
        chunk_end = seg_start + ((char_offset + chunk_chars) / total_chars) * total_duration
        entries.append({
            "start": round(chunk_start, 3),
            "end": round(chunk_end, 3),
            "text": chunk,
        })
        char_offset += chunk_chars

    return entries


def segments_to_srt(segments: list, offset: float = 0.0, max_chars: int = 18) -> list:
    """将 ASR segments 转为 SRT 条目列表，长段落自动拆分"""
    srt_entries = []
    for seg in segments:
        start = seg.get("start", 0) + offset
        end = seg.get("end", 0) + offset
        text = seg.get("text", "").strip()
        speaker = seg.get("speaker", "")
        translation = seg.get("translation", "")

        if not text:
            continue

        if len(text) <= max_chars:
            subtitle_text = ""
            if speaker:
                subtitle_text += f"[{speaker}] "
            subtitle_text += text
            if translation:
                subtitle_text += f"\n{translation}"
            srt_entries.append({"start": start, "end": end, "text": subtitle_text})
        else:
            sub_entries = split_segment_by_punctuation(text, start, end, max_chars=max_chars)
            if speaker:
                for e in sub_entries:
                    e["text"] = f"[{speaker}] {e['text']}"
            srt_entries.extend(sub_entries)

    return srt_entries


def text_to_srt_entries(text: str, total_duration: float) -> list:
    """当 ASR 不返回 segments 时，将纯文本按句号分割，均匀分配时间"""
    sentences = re.split(r'[。！？!?\.]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return []

    avg_duration = total_duration / len(sentences)
    entries = []
    for i, sent in enumerate(sentences):
        entries.append({
            "start": i * avg_duration,
            "end": (i + 1) * avg_duration,
            "text": sent,
        })
    return entries


def strip_punctuation(text: str) -> str:
    """去除中英文标点符号，仅保留文字内容"""
    return re.sub(r'[，。！？、；：""''（）《》【】\[\]{}(),.!?;:\'"…—·\-\s]+', '', text)


def write_srt(entries: list, output_path: str, remove_punct: bool = True):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, entry in enumerate(entries, 1):
            text = entry['text']
            if remove_punct:
                text = strip_punctuation(text)
            if not text:
                continue
            f.write(f"{i}\n")
            f.write(f"{format_srt_time(entry['start'])} --> {format_srt_time(entry['end'])}\n")
            f.write(f"{text}\n\n")


def write_vtt(entries: list, output_path: str, remove_punct: bool = True):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, entry in enumerate(entries, 1):
            text = entry['text']
            if remove_punct:
                text = strip_punctuation(text)
            if not text:
                continue
            start = format_srt_time(entry["start"]).replace(",", ".")
            end = format_srt_time(entry["end"]).replace(",", ".")
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")


def find_cjk_font() -> str:
    """查找系统中可用的中文字体"""
    import shutil
    if shutil.which("fc-list"):
        result = subprocess.run(
            ["fc-list", ":lang=zh", "-f", "%{family}\n"],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            font = result.stdout.strip().split("\n")[0].split(",")[0].strip()
            if font:
                return font
    fallbacks = [
        "Noto Sans CJK SC", "Noto Serif CJK SC",
        "WenQuanYi Micro Hei", "WenQuanYi Zen Hei",
        "SimHei", "Microsoft YaHei", "PingFang SC",
        "Source Han Sans SC", "Source Han Serif SC",
    ]
    for fb in fallbacks:
        result = subprocess.run(["fc-match", fb], capture_output=True, text=True)
        if result.returncode == 0 and "NotoSans" in result.stdout or "Wen" in result.stdout:
            return fb
    return "Noto Sans CJK SC"


def burn_subtitles(video_path: str, srt_path: str, output_path: str,
                   font_size: int = 24, font_color: str = "white",
                   outline_color: str = "black", outline_width: int = 2,
                   position: str = "bottom"):
    """使用 ffmpeg 将 SRT 字幕烧入视频（支持中文字体）"""
    font_name = find_cjk_font()
    print(f"  使用字体: {font_name}")

    escaped_srt = srt_path.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    margin_v = 30 if position == "bottom" else 10
    alignment = 2 if position == "bottom" else 6

    subtitle_filter = (
        f"subtitles='{escaped_srt}'"
        f":force_style='FontName={font_name},"
        f"FontSize={font_size},"
        f"PrimaryColour=&H00FFFFFF,"
        f"OutlineColour=&H00000000,"
        f"Outline={outline_width},"
        f"Alignment={alignment},"
        f"MarginV={margin_v}'"
    )

    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", subtitle_filter, "-c:a", "copy", output_path,
    ]

    print(f"  烧入字幕: {os.path.basename(video_path)} -> {os.path.basename(output_path)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg 字幕烧入失败:\n{result.stderr}")
    return output_path


def generate_subtitles(input_path: str, output_dir: str = None,
                       senseaudio_api_key: str = None,
                       model: str = "standard",
                       language: str = None,
                       target_language: str = None,
                       enable_speaker: bool = False,
                       enable_sentiment: bool = False,
                       burn: bool = False,
                       font_size: int = 24,
                       subtitle_format: str = "srt"):
    """主流程：生成字幕"""
    api_key = senseaudio_api_key or SENSEAUDIO_API_KEY
    if not api_key:
        api_key = input("未检测到 SENSEAUDIO_API_KEY，请输入 SenseAudio API 密钥（https://senseaudio.cn 注册获取）: ").strip()
        if not api_key:
            print("错误: 未提供 API 密钥，无法继续。")
            return

    asr_model = ASR_MODELS.get(model, model)
    if asr_model not in ASR_MODELS.values():
        print(f"错误: 不支持的模型 '{model}'，可选: {', '.join(ASR_MODELS.keys())}")
        return

    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(input_path)), "subtitle_output")
    os.makedirs(output_dir, exist_ok=True)

    basename = os.path.splitext(os.path.basename(input_path))[0]

    # Step 1: 判断输入类型，提取音频
    print(f"[1/4] 处理输入文件: {input_path}")
    audio_extensions = {".wav", ".mp3", ".ogg", ".flac", ".aac", ".m4a"}
    video_extensions = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".ts"}
    ext = os.path.splitext(input_path)[1].lower()

    is_video = ext in video_extensions
    audio_path = input_path

    if is_video:
        print(f"  检测到视频文件，提取音频...")
        audio_path = os.path.join(output_dir, f"{basename}_audio.wav")
        extract_audio(input_path, audio_path)
        print(f"  音频已提取: {audio_path}")
    elif ext not in audio_extensions:
        print(f"  警告: 未知文件类型 '{ext}'，尝试当作音频处理")

    # Step 2: 切片
    print(f"\n[2/4] 准备音频切片...")
    chunks = split_audio(audio_path, chunk_duration=55, output_dir=output_dir)
    print(f"  共 {len(chunks)} 个切片")

    # Step 3: ASR 识别
    print(f"\n[3/4] ASR 语音识别 (模型: {asr_model})...")
    all_entries = []
    full_text_parts = []

    for i, (chunk_path, offset) in enumerate(chunks):
        print(f"  ({i+1}/{len(chunks)}) 识别中... [偏移: {offset:.1f}s]")
        result = asr_recognize(
            chunk_path, api_key, model=asr_model,
            language=language, target_language=target_language,
            enable_speaker=enable_speaker, enable_sentiment=enable_sentiment,
        )

        text = result.get("text", "")
        segments = result.get("segments")
        duration_ms = 0
        if result.get("audio_info"):
            duration_ms = result["audio_info"].get("duration", 0)
        chunk_duration_sec = duration_ms / 1000.0 if duration_ms else 55.0

        if segments:
            entries = segments_to_srt(segments, offset=offset)
            all_entries.extend(entries)
            print(f"    生成 {len(entries)} 条字幕")
        elif text:
            entries = text_to_srt_entries(text, chunk_duration_sec)
            for e in entries:
                e["start"] += offset
                e["end"] += offset
            all_entries.extend(entries)

        if text:
            full_text_parts.append(text)
            print(f"    识别文本: {text[:60]}...")

    if not all_entries and not full_text_parts:
        print("错误: ASR 未识别到任何内容")
        return

    # Step 4: 生成字幕文件
    print(f"\n[4/4] 生成字幕文件...")

    srt_path = os.path.join(output_dir, f"{basename}.srt")
    vtt_path = os.path.join(output_dir, f"{basename}.vtt")
    txt_path = os.path.join(output_dir, f"{basename}.txt")

    write_srt(all_entries, srt_path)
    print(f"  SRT: {srt_path}")

    if subtitle_format in ("vtt", "both"):
        write_vtt(all_entries, vtt_path)
        print(f"  VTT: {vtt_path}")

    full_text = "\n".join(full_text_parts)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"  TXT: {txt_path}")

    json_path = os.path.join(output_dir, f"{basename}_detail.json")
    detail = {
        "source": input_path,
        "model": asr_model,
        "language": language,
        "target_language": target_language,
        "total_segments": len(all_entries),
        "full_text": full_text,
        "segments": all_entries,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(detail, f, ensure_ascii=False, indent=2)
    print(f"  JSON: {json_path}")

    # 可选: 烧入字幕
    if burn and is_video:
        print(f"\n[Extra] 烧入字幕到视频...")
        output_video = os.path.join(output_dir, f"{basename}_subtitled{ext}")
        burn_subtitles(input_path, srt_path, output_video, font_size=font_size)
        print(f"  输出视频: {output_video}")

    # 清理临时切片
    if len(chunks) > 1:
        for chunk_path, _ in chunks:
            if chunk_path != audio_path and os.path.exists(chunk_path):
                os.remove(chunk_path)

    print(f"\n完成!")
    print(f"  字幕条目数: {len(all_entries)}")
    print(f"  输出目录: {output_dir}")

    return srt_path


def interactive_select_output_dir(input_path: str, default_subdir: str = "subtitle_output") -> str:
    """交互式选择输出目录"""
    input_dir = os.path.dirname(os.path.abspath(input_path))

    candidates = []
    # 1. 输入文件所在目录下的默认子目录
    candidates.append(os.path.join(input_dir, default_subdir))
    # 2. 当前工作目录下的默认子目录
    cwd_output = os.path.join(os.getcwd(), default_subdir)
    if os.path.abspath(cwd_output) != os.path.abspath(candidates[0]):
        candidates.append(cwd_output)
    # 3. 桌面
    desktop = os.path.join(os.path.expanduser("~"), "Desktop", default_subdir)
    candidates.append(desktop)
    # 4. 输入文件所在目录（直接输出，不创建子目录）
    candidates.append(input_dir)

    # 去重并保持顺序
    seen = set()
    unique = []
    for c in candidates:
        norm = os.path.normpath(c)
        if norm not in seen:
            seen.add(norm)
            unique.append(c)

    print("\n请选择输出目录:")
    for i, path in enumerate(unique, 1):
        exists_tag = " (已存在)" if os.path.isdir(path) else ""
        print(f"  [{i}] {path}{exists_tag}")
    print(f"  [{len(unique) + 1}] 手动输入路径")

    while True:
        try:
            choice = input(f"\n请输入编号 [1-{len(unique) + 1}]，直接回车选 [1]: ").strip()
            if not choice:
                return unique[0]
            idx = int(choice)
            if 1 <= idx <= len(unique):
                return unique[idx - 1]
            elif idx == len(unique) + 1:
                custom = input("请输入自定义输出路径: ").strip()
                if custom:
                    return os.path.abspath(custom)
                print("路径不能为空，请重新选择。")
            else:
                print(f"请输入 1-{len(unique) + 1} 之间的数字。")
        except ValueError:
            print("请输入有效数字。")
        except (EOFError, KeyboardInterrupt):
            print("\n使用默认路径。")
            return unique[0]


def main():
    parser = argparse.ArgumentParser(
        description="视频/音频字幕生成工具 — 基于 SenseAudio ASR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python video_subtitle.py video.mp4
  python video_subtitle.py video.mp4 --language zh --translate en
  python video_subtitle.py meeting.mp4 --model pro --speaker
  python video_subtitle.py video.mp4 --burn --font-size 28
        """,
    )
    parser.add_argument("input", type=str, help="输入视频或音频文件路径")
    parser.add_argument("--output", type=str, default=None, help="输出目录")
    parser.add_argument("--model", type=str, default="standard",
                        choices=["lite", "standard", "pro", "deepthink"],
                        help="ASR 模型 (默认: standard)")
    parser.add_argument("--language", type=str, default=None,
                        help="音频语言代码 (如 zh/en/ja，不设则自动检测)")
    parser.add_argument("--translate", type=str, default=None, dest="target_language",
                        help="翻译目标语言代码 (如 en/zh/ja)")
    parser.add_argument("--speaker", action="store_true", default=False,
                        help="启用说话人分离 (仅 standard/pro)")
    parser.add_argument("--sentiment", action="store_true", default=False,
                        help="启用情感分析 (仅 standard/pro)")
    parser.add_argument("--burn", action="store_true", default=False,
                        help="将字幕烧入视频")
    parser.add_argument("--font-size", type=int, default=24,
                        help="烧入字幕字体大小 (默认: 24)")
    parser.add_argument("--format", type=str, default="srt",
                        choices=["srt", "vtt", "both"],
                        dest="subtitle_format",
                        help="字幕格式 (默认: srt)")
    parser.add_argument("--senseaudio-api-key", type=str, default=None,
                        help="SenseAudio API 密钥")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"错误: 文件不存在: {args.input}")
        return

    output_dir = args.output
    if output_dir is None:
        output_dir = interactive_select_output_dir(
            args.input, default_subdir="subtitle_output"
        )

    generate_subtitles(
        input_path=args.input,
        output_dir=output_dir,
        senseaudio_api_key=args.senseaudio_api_key,
        model=args.model,
        language=args.language,
        target_language=args.target_language,
        enable_speaker=args.speaker,
        enable_sentiment=args.sentiment,
        burn=args.burn,
        font_size=args.font_size,
        subtitle_format=args.subtitle_format,
    )


if __name__ == "__main__":
    main()
