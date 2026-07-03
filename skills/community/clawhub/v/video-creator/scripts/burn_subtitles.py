#!/usr/bin/env python3
"""
纯 Python 字幕烧录工具：PIL 生成字幕 PNG → ffmpeg overlay 叠加
不依赖 libass/freetype，高效节省内存，兼容所有 ffmpeg 版本
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path




PREFERRED_BREAK_PUNCT = set("，。！？；：、,.!?;:）)】》」』")
EN_WORD_CHAR_RE = re.compile(r"[A-Za-z0-9']")


def _visual_width(text):
    """计算文本视觉宽度：中文/全角=1，英文/符号=0.5"""
    width = 0.0
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf' or '\u3000' <= ch <= '\u303f' or '\uff00' <= ch <= '\uffef':
            width += 1.0
        else:
            width += 0.5
    return width


def _char_index_at_width(text, max_width):
    """找到视觉宽度刚好不超过 max_width 的字符索引"""
    width = 0.0
    for i, ch in enumerate(text):
        char_w = 1.0 if ('\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf' or '\u3000' <= ch <= '\u303f' or '\uff00' <= ch <= '\uffef') else 0.5
        if width + char_w > max_width:
            return i
        width += char_w
    return len(text)


def parse_srt(srt_path):
    """解析 SRT 文件，返回 [(start_sec, end_sec, text), ...]"""
    with open(srt_path, encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r'\n\s*\n', content.strip())
    result = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        m = re.match(
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})',
            lines[1]
        )
        if not m:
            continue
        g = m.groups()
        start = int(g[0])*3600 + int(g[1])*60 + int(g[2]) + int(g[3])/1000
        end = int(g[4])*3600 + int(g[5])*60 + int(g[6]) + int(g[7])/1000
        text = '\n'.join(lines[2:])
        result.append((start, end, text))
    return result


def _is_en_word_char(ch):
    return bool(EN_WORD_CHAR_RE.fullmatch(ch))


def _choose_cut_index(line, max_chars):
    """选择当前行的断句位置：优先标点，其次视觉宽度上限，且不拆英文单词。"""
    if _visual_width(line) <= max_chars:
        return len(line)

    # 1) 优先在 max_chars 视觉宽度范围内找最后一个标点。
    width_limit_idx = _char_index_at_width(line, max_chars)
    for i in range(width_limit_idx - 1, -1, -1):
        if line[i] in PREFERRED_BREAK_PUNCT:
            return i + 1

    # 2) 否则按视觉宽度上限断，但不能切开英文单词。
    cut = width_limit_idx
    if 0 < cut < len(line) and _is_en_word_char(line[cut - 1]) and _is_en_word_char(line[cut]):
        # 尝试向左回退到该英文词开头。
        left = cut
        while left > 0 and _is_en_word_char(line[left - 1]):
            left -= 1
        if left > 0:
            return left

        # 整行从英文词开始且超长，向右扩展到词尾。
        right = cut
        while right < len(line) and _is_en_word_char(line[right]):
            right += 1
        return right

    return cut


def split_text_chunks(text, max_chars=26):
    """将文本切分为单行片段：优先标点断句，最多 26 字（中文场景），且不拆英文词。"""
    chunks = []
    for raw_line in text.split('\n'):
        line = raw_line.strip()
        if not line:
            continue

        while line:
            cut = _choose_cut_index(line, max_chars)
            piece = line[:cut].strip()
            if piece:
                chunks.append(piece)
            line = line[cut:].strip()

    return chunks


def _visual_wrap(text, max_chars=26):
    """对文本做视觉换行（插入 \n），不拆时间。"""
    chunks = split_text_chunks(text, max_chars=max_chars)
    return '\n'.join(chunks)


def expand_subs_for_single_line(subs, max_chars=26):
    """把一条字幕拆成多个连续时间片，保证单行依次显示。"""
    expanded = []
    for start, end, text in subs:
        chunks = split_text_chunks(text, max_chars=max_chars)
        if not chunks:
            continue
        if len(chunks) == 1:
            expanded.append((start, end, chunks[0]))
            continue

        total_duration = end - start
        if total_duration <= 0:
            expanded.append((start, end, chunks[0]))
            continue

        weights = [max(1, _visual_width(chunk)) for chunk in chunks]
        total_weight = sum(weights)
        current = start
        for idx, (chunk, weight) in enumerate(zip(chunks, weights)):
            if idx == len(chunks) - 1:
                chunk_end = end
            else:
                chunk_end = current + total_duration * (weight / total_weight)
            expanded.append((current, chunk_end, chunk))
            current = chunk_end

    return expanded


def burn_subtitles(video_path, srt_path, output_path):
    """生成字幕 PNG，用 ffmpeg overlay 滤镜叠加到视频上（无需 libass/freetype）"""
    from PIL import Image, ImageDraw, ImageFont

    subs = parse_srt(srt_path)
    if not subs:
        print("⚠️ SRT 字幕为空，直接复制视频")
        import shutil
        shutil.copy2(video_path, output_path)
        return

    # 获取视频尺寸
    probe = subprocess.run(
        ["ffprobe", "-v", "error",
         "-show_entries", "stream=width,height",
         "-of", "json", video_path],
        capture_output=True, text=True
    )
    info = json.loads(probe.stdout)
    video_stream = next((s for s in info.get("streams", []) if "width" in s), None)
    if not video_stream:
        print("❌ 无法获取视频信息")
        return
    w = video_stream["width"]
    h = video_stream["height"]

    # 竖屏每行最多 9 个汉字，横屏最多 26 字
    max_chars_per_line = 9 if h > w else 26
    # 对每条字幕做视觉换行（不拆时间），确保不超出屏幕宽度
    _wrapped_subs = []
    for start, end, text in subs:
        wrapped_text = _visual_wrap(text, max_chars_per_line)
        _wrapped_subs.append((start, end, wrapped_text))
    subs = _wrapped_subs

    # 字体
    font_size = max(28, h // 18)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
    except Exception:
        font = ImageFont.load_default()

    # 生成字幕 PNG + ffmpeg overlay filter
    with tempfile.TemporaryDirectory() as tmp_dir:
        inputs = ["-i", video_path]
        filter_parts = []
        png_paths = []

        for idx, (start, end, text) in enumerate(subs):
            img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            lines = text.split('\n')

            # 计算所有行文字的总尺寸，用于绘制半透明背景条
            line_sizes = []
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                line_sizes.append((tw, th))
            max_tw = max(s[0] for s in line_sizes) if line_sizes else 0
            # 用 font_size 计算行高，与文字定位逻辑 (font_size+6) 保持一致
            total_th = len(line_sizes) * font_size + (len(line_sizes) - 1) * 6 if line_sizes else 0

            # 背景条参数
            bg_pad_x = 16   # 水平内边距
            bg_pad_y = 15   # 垂直内边距（原25→15，减少10px）
            bg_extra_h = 30 # 额外高度补偿（padding减少20，总高需增10，故补偿30）
            bg_x = (w - max_tw) // 2 - bg_pad_x
            bg_y_top = int(h * 0.88) - (total_th + bg_extra_h) // 2 - bg_pad_y
            bg_w = max_tw + 2 * bg_pad_x
            bg_h = total_th + 2 * bg_pad_y + bg_extra_h

            # 绘制深灰色 50% 透明背景条
            draw.rounded_rectangle(
                [bg_x, bg_y_top, bg_x + bg_w, bg_y_top + bg_h],
                radius=6,
                fill=(80, 80, 80, 128),   # 深灰色 RGB(80,80,80)，50% 透明 Alpha=128
            )

            for li, line in enumerate(lines):
                tw, th = line_sizes[li]
                x = (w - tw) // 2
                y_pos = bg_y_top + bg_pad_y + li * (font_size + 6)
                # 描边（黑色，增强对比）
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, y_pos + dy), line, fill="black", font=font)
                draw.text((x, y_pos), line, fill="white", font=font)

            png_path = str(Path(tmp_dir) / f"sub_{idx:04d}.png")
            img.save(png_path)
            inputs.extend(["-i", png_path])
            png_paths.append(png_path)

            enable = f"between(t\\,{start:.3f}\\,{end:.3f})"
            if idx == 0:
                filter_parts.append(f"[0:v][1:v]overlay=0:0:enable='{enable}'[v1]")
            else:
                prev = f"[v{idx}]" if idx > 0 else "[0:v]"
                filter_parts.append(f"{prev}[{idx+1}:v]overlay=0:0:enable='{enable}'[v{idx+1}]")

        if not filter_parts:
            print("⚠️ 无有效字幕，直接复制视频")
            import shutil
            shutil.copy2(video_path, output_path)
            return

        filter_str = ";".join(filter_parts)
        last_v = f"[v{len(subs)}]"

        print(f"🎬 开始 overlay 字幕：{w}x{h}，{len(subs)} 条字幕事件")
        cmd = (
            ["ffmpeg", "-y"]
            + inputs
            + [
                "-filter_complex", filter_str,
                "-map", last_v,
                "-map", "0:a",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-c:a", "copy",
                output_path,
            ]
        )
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            stderr = result.stderr.decode(errors='replace')
            print(f"❌ 编码失败：{stderr[-500:]}")
        else:
            print(f"✅ 字幕烧录完成，{len(subs)} 条字幕")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python burn_subtitles.py <输入视频> <SRT字幕> <输出视频>")
        sys.exit(1)
    burn_subtitles(sys.argv[1], sys.argv[2], sys.argv[3])
