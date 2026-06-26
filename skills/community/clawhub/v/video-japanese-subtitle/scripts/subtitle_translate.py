#!/usr/bin/env python3
"""
视频字幕翻译烧录脚本 v1
流程：提取音频 → faster-whisper 转录日语 → QClaw LLM 翻译日→中 → SRT转ASS → ffmpeg烧录

环境要求：
- ffmpeg (PATH已配置)
- Python: faster-whisper, deep-translator
- QClaw 网关 (本地)

使用方法：
  python subtitle_translate_v1.py

输出：output/ 目录
"""

import os
import sys
import re
import json
import time
import hashlib
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# ============ 配置 ============
VIDEO_DIR = Path(r"D:\Users\liket\Desktop\000")
OUTPUT_DIR = Path(r"D:\Users\liket\Desktop\000\output")
FFMPEG_DIR = Path(r"E:\ffmpeg\SCP\ffmpeg-master-latest-win64-gpl\bin")
WHISPER_MODEL = "base"  # base / small / medium / large-v3
WHISPER_LANG = "ja"

# QClaw 网关翻译配置
QCLAW_GATEWAY = "http://127.0.0.1:28789/v1/chat/completions"
QCLAW_TOKEN = "78238b99f7ed3fb71de138d875005ac5a80274920af729fe"
TRANSLATE_BATCH_SIZE = 15  # 每批翻译的 SRT 条目数
TRANSLATE_MODEL = "openclaw"

# ffmpeg PATH（Whisper 内部也用 ffmpeg）
os.environ["PATH"] = str(FFMPEG_DIR) + os.pathsep + os.environ.get("PATH", "")
FFMPEG = str(FFMPEG_DIR / "ffmpeg.exe")
FFPROBE = str(FFMPEG_DIR / "ffprobe.exe")

# ASS 字幕样式
ASS_HEADER = """[Script Info]
Title: Translated Subtitles
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft YaHei UI,36,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,2,10,10,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def file_hash(path):
    """取文件名 hash 作为短名"""
    return hashlib.md5(path.encode('utf-8')).hexdigest()[:8]


def get_video_list():
    """扫描视频目录"""
    videos = []
    for f in sorted(Path(VIDEO_DIR).iterdir()):
        if f.suffix.lower() == '.mp4' and f.is_file():
            videos.append(f)
    return videos


def extract_audio(video_path, audio_path):
    """提取音频为 WAV"""
    print(f"  [1/5] 提取音频: {video_path.name}")
    cmd = [
        FFMPEG, "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        str(audio_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        print(f"    ⚠ 音频提取失败: {result.stderr[-200:]}")
        return False
    print(f"    ✓ 音频已提取")
    return True


def transcribe_audio(audio_path, srt_path):
    """用 openai-whisper 转录日语"""
    print(f"  [2/5] Whisper 转录日语...")
    import whisper
    
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(
        str(audio_path),
        language=WHISPER_LANG,
        task="transcribe",
        verbose=False
    )
    
    srt_entries = []
    for i, seg in enumerate(result['segments'], 1):
        start = format_srt_time(seg['start'])
        end = format_srt_time(seg['end'])
        text = seg['text'].strip()
        if text:
            srt_entries.append(f"{i}\n{start} --> {end}\n{text}\n")
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(srt_entries))
    
    print(f"    ✓ 转录完成: {len(srt_entries)} 条")
    return len(srt_entries) > 0


def format_srt_time(seconds):
    """秒数转 SRT 时间格式"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_srt(srt_path):
    """解析 SRT 文件"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = []
    blocks = re.split(r'\n\s*\n', content.strip())
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            idx = int(lines[0].strip())
            time_match = re.match(
                r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})',
                lines[1].strip()
            )
            if time_match:
                start = time_match.group(1)
                end = time_match.group(2)
                text = '\n'.join(lines[2:]).strip()
                entries.append({
                    'index': idx,
                    'start': start,
                    'end': end,
                    'text': text
                })
    return entries


def translate_with_qclaw(texts, retry=3):
    """用 QClaw 网关 LLM 批量翻译日语→中文"""
    if not texts:
        return texts
    
    # 构建翻译 prompt
    numbered = '\n'.join(f'{i+1}. {t}' for i, t in enumerate(texts))
    user_msg = f"请将以下日语逐行翻译为简体中文，保留编号格式（1. 2. 3. ...），只输出翻译结果：\n\n{numbered}"
    
    payload = json.dumps({
        'model': TRANSLATE_MODEL,
        'messages': [
            {
                'role': 'system',
                'content': '你是一个日语到简体中文的专业翻译器。只输出翻译结果，不加任何解释、注释或额外文字。保留原文的编号格式。'
            },
            {
                'role': 'user',
                'content': user_msg
            }
        ],
        'max_tokens': 2000,
        'temperature': 0.1
    }).encode('utf-8')
    
    req = urllib.request.Request(
        QCLAW_GATEWAY,
        data=payload,
        headers={
            'Authorization': f'Bearer {QCLAW_TOKEN}',
            'Content-Type': 'application/json'
        }
    )
    
    for attempt in range(retry):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                content = result['choices'][0]['message']['content'].strip()
                return parse_translated_lines(content, len(texts))
        except Exception as e:
            print(f"    翻译请求失败 (尝试 {attempt+1}/{retry}): {e}")
            time.sleep(2 * (attempt + 1))
    
    # 全部失败，回退到 MyMemory
    print(f"    ⚠ LLM 翻译全部失败，回退 MyMemory...")
    return translate_with_mymemory(texts)


def parse_translated_lines(content, expected_count):
    """解析 LLM 翻译结果，提取编号行"""
    lines = content.split('\n')
    translated = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 去掉编号前缀 (1. 2. 等)
        match = re.match(r'^\d+[\.\)、]\s*(.*)', line)
        if match:
            translated.append(match.group(1).strip())
        else:
            translated.append(line)
    
    # 如果数量不匹配，尝试其他解析方式
    if len(translated) != expected_count:
        # 可能没有编号，直接按行分割
        alt = [l.strip() for l in lines if l.strip()]
        if len(alt) == expected_count:
            return alt
        print(f"    ⚠ 翻译条目数不匹配: 期望{expected_count}, 实际{len(translated)}")
        # 尽量对齐
        while len(translated) < expected_count:
            translated.append("")
    
    return translated[:expected_count]


def translate_with_mymemory(texts):
    """回退：用 MyMemory 翻译"""
    from deep_translator import MyMemoryTranslator
    translator = MyMemoryTranslator(source='ja-JP', target='zh-CN')
    results = []
    for text in texts:
        try:
            t = translator.translate(text)
            results.append(t if t else text)
            time.sleep(0.3)  # 避免限流
        except:
            results.append(text)  # 翻译失败保留原文
    return results


def translate_srt(srt_path, translated_srt_path):
    """翻译 SRT 文件：日语→中文"""
    print(f"  [3/5] 翻译字幕 日→中...")
    entries = parse_srt(srt_path)
    if not entries:
        print("    ⚠ 无有效字幕条目")
        return False
    
    # 批量翻译
    all_texts = [e['text'] for e in entries]
    all_translated = []
    
    total_batches = (len(all_texts) + TRANSLATE_BATCH_SIZE - 1) // TRANSLATE_BATCH_SIZE
    for i in range(0, len(all_texts), TRANSLATE_BATCH_SIZE):
        batch = all_texts[i:i+TRANSLATE_BATCH_SIZE]
        batch_num = i // TRANSLATE_BATCH_SIZE + 1
        print(f"    翻译批次 {batch_num}/{total_batches} ({len(batch)} 条)...")
        
        translated = translate_with_qclaw(batch)
        all_translated.extend(translated)
        time.sleep(1)  # 避免请求过快
    
    # 写入翻译后的 SRT
    with open(translated_srt_path, 'w', encoding='utf-8') as f:
        for i, entry in enumerate(entries):
            translated_text = all_translated[i] if i < len(all_translated) else entry['text']
            f.write(f"{entry['index']}\n")
            f.write(f"{entry['start']} --> {entry['end']}\n")
            f.write(f"{translated_text}\n\n")
    
    print(f"    ✓ 翻译完成: {len(entries)} 条")
    return True


def srt_to_ass(srt_path, ass_path):
    """SRT 转 ASS 格式"""
    print(f"  [3.5] SRT → ASS 格式转换...")
    entries = parse_srt(srt_path)
    
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ASS_HEADER)
        for entry in entries:
            start = srt_time_to_ass(entry['start'])
            end = srt_time_to_ass(entry['end'])
            text = entry['text'].replace('\n', '\\N')
            f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")
    
    print(f"    ✓ ASS 生成完成")
    return True


def srt_time_to_ass(srt_time):
    """SRT 时间格式转 ASS 时间格式"""
    # 00:00:05,000 → 0:00:05.00
    h, m, s = srt_time.replace(',', '.').split(':')
    s_int, s_dec = s.split('.')
    s_dec = s_dec[:2]  # 取前两位
    return f"{int(h)}:{m}:{s_int}.{s_dec}"


def burn_subtitles(video_path, ass_path, output_path):
    """烧录字幕到视频（NVENC 优先，CPU 回退）"""
    print(f"  [4/5] 烧录字幕...")
    
    # 使用相对路径 + cwd 避免 Windows 盘符冒号问题
    ass_dir = os.path.dirname(os.path.abspath(ass_path))
    ass_filename = os.path.basename(ass_path)
    
    # 尝试 NVENC
    cmd_nvenc = [
        FFMPEG, "-y",
        "-i", str(video_path),
        "-vf", f"ass={ass_filename}",
        "-c:v", "h264_nvenc",
        "-preset", "p4",
        "-cq", "23",
        "-c:a", "copy",
        str(output_path)
    ]
    
    # CPU 回退
    cmd_cpu = [
        FFMPEG, "-y",
        "-i", str(video_path),
        "-vf", f"ass={ass_filename}",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "copy",
        str(output_path)
    ]
    
    for label, cmd in [("NVENC GPU", cmd_nvenc), ("CPU libx264", cmd_cpu)]:
        print(f"    尝试 {label}...")
        try:
            result = subprocess.run(
                cmd,
                cwd=ass_dir,  # 关键：设置工作目录为字幕文件所在目录
                capture_output=True,
                text=True,
                timeout=3600  # 1小时超时
            )
            if result.returncode == 0:
                size_mb = os.path.getsize(output_path) / (1024*1024)
                print(f"    ✓ {label} 烧录完成 ({size_mb:.1f} MB)")
                return True
            else:
                err = result.stderr[-300:] if result.stderr else "unknown"
                print(f"    ✗ {label} 失败: {err}")
        except subprocess.TimeoutExpired:
            print(f"    ✗ {label} 超时")
        except Exception as e:
            print(f"    ✗ {label} 异常: {e}")
    
    return False


def verify_video(video_path):
    """用 ffprobe 验证视频完整性"""
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            duration = float(result.stdout.strip())
            return duration > 0
    except:
        pass
    return False


def process_video(video_path):
    """处理单个视频的完整流程"""
    h = file_hash(str(video_path))
    print(f"\n{'='*60}")
    print(f"处理: {video_path.name} (hash: {h})")
    print(f"{'='*60}")
    
    # 工作目录
    work_dir = Path(OUTPUT_DIR)
    work_dir.mkdir(parents=True, exist_ok=True)
    
    # 文件路径
    audio_path = work_dir / f"{h}_audio.wav"
    srt_path = work_dir / f"{h}_subs.srt"
    translated_srt_path = work_dir / f"{h}_subs_zh.srt"
    ass_path = work_dir / f"{h}_subs_zh.ass"
    output_path = work_dir / f"video_{h}_subtitled.mp4"
    
    # 检查是否已完成
    if output_path.exists() and verify_video(output_path):
        print(f"  ✓ 已存在，跳过")
        return True
    
    start_time = time.time()
    
    # Step 1: 提取音频
    if not audio_path.exists():
        if not extract_audio(video_path, audio_path):
            return False
    else:
        print(f"  [1/5] 音频已存在，跳过提取")
    
    # Step 2: Whisper 转录
    if not srt_path.exists():
        if not transcribe_audio(audio_path, srt_path):
            return False
    else:
        print(f"  [2/5] SRT 已存在，跳过转录")
    
    # Step 3: 翻译字幕
    if not translated_srt_path.exists():
        if not translate_srt(srt_path, translated_srt_path):
            return False
    else:
        print(f"  [3/5] 翻译字幕已存在，跳过")
    
    # Step 3.5: SRT 转 ASS
    if not ass_path.exists():
        if not srt_to_ass(translated_srt_path, ass_path):
            return False
    else:
        print(f"  [3.5] ASS 已存在，跳过转换")
    
    # Step 4: 烧录字幕
    if not burn_subtitles(video_path, ass_path, output_path):
        return False
    
    # Step 5: 验证
    print(f"  [5/5] 验证视频...")
    if verify_video(output_path):
        elapsed = time.time() - start_time
        print(f"  ✓ 全部完成！耗时 {elapsed:.0f} 秒")
        return True
    else:
        print(f"  ✗ 视频验证失败")
        return False


def main():
    print("字幕翻译烧录 v1")
    print(f"视频目录: {VIDEO_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"翻译方式: QClaw LLM (回退 MyMemory)")
    print()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    videos = get_video_list()
    print(f"找到 {len(videos)} 个视频文件\n")
    
    success = 0
    failed = 0
    
    for i, video in enumerate(videos, 1):
        print(f"\n>>> 进度: {i}/{len(videos)}")
        if process_video(video):
            success += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"全部完成！成功: {success}, 失败: {failed}")
    print(f"输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
