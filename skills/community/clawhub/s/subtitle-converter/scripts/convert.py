#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字幕格式转换工具

支持格式：VTT, SRT, ASS, LRC
功能：
  1. 格式互转
  2. 时间轴偏移
  3. 字幕合并（双语）
  4. 批量处理

用法：
  python convert.py <input> [--output <path>] [--format <fmt>]
  python convert.py <input> --shift <seconds>
  python convert.py <file1> <file2> --merge [--output <path>]
  python convert.py <directory> --batch [--format <fmt>]
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class Subtitle:
    """字幕条目数据结构"""

    index: int = 0
    start: float = 0.0  # 秒
    end: float = 0.0  # 秒
    text: str = ""


# ==================== 时间格式工具 ====================


def time_to_seconds(h: int, m: int, s: int, ms: int) -> float:
    """将时分秒毫秒转换为总秒数"""
    return h * 3600 + m * 60 + s + ms / 1000.0


def seconds_to_srt_time(seconds: float) -> str:
    """将秒数转换为 SRT 时间格式 (HH:MM:SS,mmm)"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def seconds_to_vtt_time(seconds: float) -> str:
    """将秒数转换为 VTT 时间格式 (HH:MM:SS.mmm)"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def seconds_to_ass_time(seconds: float) -> str:
    """将秒数转换为 ASS 时间格式 (H:MM:SS.cc)"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))  # 厘秒
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def seconds_to_lrc_time(seconds: float) -> str:
    """将秒数转换为 LRC 时间格式 [mm:ss.xx]"""
    m = int(seconds // 60)
    s = seconds % 60
    return f"[{m:02d}:{s:05.2f}]"


def parse_srt_time(time_str: str) -> Tuple[float, float]:
    """解析 SRT 时间格式"""
    # 格式: HH:MM:SS,mmm --> HH:MM:SS,mmm
    pattern = r"(\d{2}):(\d{2}):(\d{2}),(\d{3})"
    match = re.findall(pattern, time_str)
    if len(match) == 2:
        start = time_to_seconds(*map(int, match[0]))
        end = time_to_seconds(*map(int, match[1]))
        return start, end
    return 0.0, 0.0


def parse_vtt_time(time_str: str) -> Tuple[float, float]:
    """解析 VTT 时间格式"""
    # 格式: HH:MM:SS.mmm --> HH:MM:SS.mmm 或 MM:SS.mmm --> MM:SS.mmm
    pattern = r"(\d{1,2}):(\d{2}):(\d{2})\.(\d{3})"
    pattern_short = r"(\d{1,2}):(\d{2})\.(\d{3})"

    match = re.findall(pattern, time_str)
    if len(match) == 2:
        start = time_to_seconds(
            int(match[0][0]), int(match[0][1]), int(match[0][2]), int(match[0][3])
        )
        end = time_to_seconds(
            int(match[1][0]), int(match[1][1]), int(match[1][2]), int(match[1][3])
        )
        return start, end

    match = re.findall(pattern_short, time_str)
    if len(match) == 2:
        start = time_to_seconds(0, int(match[0][0]), int(match[0][1]), int(match[0][2]))
        end = time_to_seconds(0, int(match[1][0]), int(match[1][1]), int(match[1][2]))
        return start, end
    return 0.0, 0.0


def parse_ass_time(time_str: str) -> float:
    """解析 ASS 时间格式 (H:MM:SS.cc)"""
    pattern = r"(\d{1,2}):(\d{2}):(\d{2})\.(\d{2})"
    match = re.match(pattern, time_str.strip())
    if match:
        h, m, s, cs = map(int, match.groups())
        return h * 3600 + m * 60 + s + cs / 100.0
    return 0.0


def parse_lrc_time(time_str: str) -> float:
    """解析 LRC 时间格式 [mm:ss.xx]"""
    pattern = r"\[(\d{1,2}):(\d{2})\.(\d{2,3})\]"
    match = re.match(pattern, time_str.strip())
    if match:
        m, s, ms = match.groups()
        ms_val = int(ms) / (100 if len(ms) == 2 else 1000)
        return int(m) * 60 + int(s) + ms_val
    return 0.0


# ==================== 格式检测 ====================


def detect_format(file_path: str) -> str:
    """自动检测字幕文件格式"""
    path = Path(file_path)
    ext = path.suffix.lower()

    # 优先根据扩展名判断
    if ext == ".vtt":
        return "vtt"
    elif ext == ".srt":
        return "srt"
    elif ext in (".ass", ".ssa"):
        return "ass"
    elif ext == ".lrc":
        return "lrc"

    # 根据内容判断
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(500)
        if content.startswith("WEBVTT"):
            return "vtt"
        elif "[Script Info]" in content:
            return "ass"
        elif re.search(r"\[\d{2}:\d{2}\.\d{2}", content):
            return "lrc"
        elif re.search(r"\d{2}:\d{2}:\d{2},\d{3}.*-->", content):
            return "srt"

    return "unknown"


# ==================== 解析器 ====================


def parse_vtt(file_path: str) -> List[Subtitle]:
    """解析 VTT 文件"""
    subtitles = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 移除头部和注释
    lines = content.split("\n")
    cue_blocks = []
    current_block = []

    for line in lines:
        if "-->" in line:
            if current_block:
                cue_blocks.append(current_block)
            current_block = [line]
        elif current_block:
            if line.strip():
                current_block.append(line)
            else:
                if current_block:
                    cue_blocks.append(current_block)
                    current_block = []

    if current_block:
        cue_blocks.append(current_block)

    idx = 1
    for block in cue_blocks:
        if not block:
            continue

        time_line = block[0]
        # 清理时间戳中的定位参数
        time_line = re.sub(
            r"\s*(align|position|line|size|vertical):[^\s]*", "", time_line
        )
        start, end = parse_vtt_time(time_line)

        # 合并文本行并清理标签
        text_lines = block[1:] if len(block) > 1 else []
        text = "\n".join(text_lines)

        # 清理 VTT 标签
        text = re.sub(r"<[^>]+>", "", text)
        text = text.strip()

        if text and end > start:
            subtitles.append(Subtitle(index=idx, start=start, end=end, text=text))
            idx += 1

    return subtitles


def parse_srt(file_path: str) -> List[Subtitle]:
    """解析 SRT 文件"""
    subtitles = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 按空行分割块
    blocks = re.split(r"\n\s*\n", content.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue

        # 第一行是序号
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue

        # 第二行是时间戳
        time_line = lines[1]
        start, end = parse_srt_time(time_line)

        # 剩余行是文本
        text = "\n".join(lines[2:]).strip()

        # 清理 HTML 标签
        text = re.sub(r"</?[a-zA-Z]+>", "", text)

        if text and end > start:
            subtitles.append(Subtitle(index=index, start=start, end=end, text=text))

    return subtitles


def parse_ass(file_path: str) -> List[Subtitle]:
    """解析 ASS/SSA 文件"""
    subtitles = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 查找 Events 部分
    events_match = re.search(r"\[Events\](.*?)(\[|$)", content, re.DOTALL)
    if not events_match:
        return subtitles

    events_content = events_match.group(1)

    # 查找 Format 行
    format_match = re.search(r"Format:\s*(.+)", events_content)
    if not format_match:
        return subtitles

    format_fields = [f.strip().lower() for f in format_match.group(1).split(",")]

    try:
        start_idx = format_fields.index("start")
        end_idx = format_fields.index("end")
        text_idx = format_fields.index("text")
    except ValueError:
        return subtitles

    # 解析 Dialogue 行
    dialogue_pattern = r"Dialogue:\s*(.+)"
    idx = 1

    for match in re.finditer(dialogue_pattern, events_content):
        parts = match.group(1).split(",")

        # 文本部分可能包含逗号，需要特殊处理
        if len(parts) > text_idx:
            text = ",".join(parts[text_idx:]).strip()
            start = parse_ass_time(parts[start_idx].strip())
            end = parse_ass_time(parts[end_idx].strip())

            # 清理 ASS 标签
            text = re.sub(r"\{[^}]+\}", "", text)
            text = text.replace("\\N", "\n").replace("\\n", "\n").strip()

            if text and end > start:
                subtitles.append(Subtitle(index=idx, start=start, end=end, text=text))
                idx += 1

    return subtitles


def parse_lrc(file_path: str) -> List[Subtitle]:
    """解析 LRC 文件"""
    subtitles = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    idx = 1
    for line in lines:
        line = line.strip()
        if (
            not line
            or line.startswith("[")
            and ":" in line
            and not re.match(r"\[\d", line)
        ):
            # 跳过元数据行 [ti:], [ar:] 等
            continue

        # 解析时间标签
        time_pattern = r"\[(\d{1,2}:\d{2}\.\d{2,3})\](.*)"
        match = re.match(time_pattern, line)
        if match:
            start = parse_lrc_time(f"[{match.group(1)}]")
            text = match.group(2).strip()

            # 清理增强 LRC 标签
            text = re.sub(r"<\d{1,2}:\d{2}\.\d{2,3}>", "", text)

            if text:
                # LRC 没有结束时间，设置为下一行开始时间或 +5秒
                subtitles.append(
                    Subtitle(index=idx, start=start, end=start + 5, text=text)
                )
                idx += 1

    # 根据下一行开始时间修正结束时间
    for i in range(len(subtitles) - 1):
        subtitles[i].end = subtitles[i + 1].start

    return subtitles


# ==================== 生成器 ====================


def generate_srt(subtitles: List[Subtitle]) -> str:
    """生成 SRT 格式内容"""
    lines = []
    for sub in subtitles:
        lines.append(str(sub.index))
        lines.append(
            f"{seconds_to_srt_time(sub.start)} --> {seconds_to_srt_time(sub.end)}"
        )
        lines.append(sub.text)
        lines.append("")
    return "\n".join(lines)


def generate_vtt(subtitles: List[Subtitle]) -> str:
    """生成 VTT 格式内容"""
    lines = ["WEBVTT", ""]
    for sub in subtitles:
        lines.append(
            f"{seconds_to_vtt_time(sub.start)} --> {seconds_to_vtt_time(sub.end)}"
        )
        lines.append(sub.text)
        lines.append("")
    return "\n".join(lines)


def generate_ass(subtitles: List[Subtitle]) -> str:
    """生成 ASS 格式内容"""
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for sub in subtitles:
        text = sub.text.replace("\n", "\\N")
        lines.append(
            f"Dialogue: 0,{seconds_to_ass_time(sub.start)},{seconds_to_ass_time(sub.end)},Default,,0,0,0,,{text}"
        )
    return "\n".join(lines)


def generate_lrc(subtitles: List[Subtitle]) -> str:
    """生成 LRC 格式内容"""
    lines = ["[ti:Converted]", "[ar:Unknown]", ""]
    for sub in subtitles:
        lines.append(
            f"{seconds_to_lrc_time(sub.start)}{sub.text.replace(chr(10), ' ')}"
        )
    return "\n".join(lines)


# ==================== 主功能 ====================

# 解析器映射
PARSERS = {
    "vtt": parse_vtt,
    "srt": parse_srt,
    "ass": parse_ass,
    "lrc": parse_lrc,
}

# 生成器映射
GENERATORS = {
    "srt": generate_srt,
    "vtt": generate_vtt,
    "ass": generate_ass,
    "lrc": generate_lrc,
}


def convert(
    input_path: str,
    output_path: Optional[str] = None,
    target_format: Optional[str] = None,
) -> str:
    """
    转换字幕格式

    参数:
        input_path: 输入文件路径
        output_path: 输出文件路径（可选）
        target_format: 目标格式（可选，自动推断）

    返回:
        输出文件路径
    """
    # 检测源格式
    source_format = detect_format(input_path)
    if source_format == "unknown":
        raise ValueError(f"无法识别文件格式: {input_path}")

    # 确定目标格式
    if target_format is None:
        if output_path:
            target_format = Path(output_path).suffix.lower().lstrip(".")
        else:
            raise ValueError("必须指定目标格式或输出路径")

    if target_format not in GENERATORS:
        raise ValueError(f"不支持的目标格式: {target_format}")

    # 解析源文件
    parser = PARSERS.get(source_format)
    if not parser:
        raise ValueError(f"不支持的源格式: {source_format}")

    subtitles = parser(input_path)

    # 生成目标格式
    generator = GENERATORS[target_format]
    content = generator(subtitles)

    # 确定输出路径
    if output_path is None:
        input_file = Path(input_path)
        output_path = str(input_file.with_suffix(f".{target_format}"))

    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


def shift_timeline(
    input_path: str, offset_seconds: float, output_path: Optional[str] = None
) -> str:
    """
    时间轴偏移

    参数:
        input_path: 输入文件路径
        offset_seconds: 偏移秒数（正数延后，负数提前）
        output_path: 输出文件路径（可选）

    返回:
        输出文件路径
    """
    source_format = detect_format(input_path)
    parser = PARSERS.get(source_format)
    if not parser:
        raise ValueError(f"不支持的格式: {source_format}")

    subtitles = parser(input_path)

    # 应用偏移
    for sub in subtitles:
        sub.start = max(0, sub.start + offset_seconds)
        sub.end = max(0, sub.end + offset_seconds)

    # 生成输出
    generator = GENERATORS[source_format]
    content = generator(subtitles)

    if output_path is None:
        input_file = Path(input_path)
        suffix = "_shifted" if offset_seconds >= 0 else "_shifted_back"
        output_path = str(input_file.with_stem(input_file.stem + suffix))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


def merge_subtitles(
    file1: str, file2: str, output_path: Optional[str] = None, separator: str = "\n"
) -> str:
    """
    合并两个字幕文件（双语字幕）

    参数:
        file1: 第一个字幕文件（主语言）
        file2: 第二个字幕文件（副语言）
        output_path: 输出文件路径（可选）
        separator: 两行字幕之间的分隔符

    返回:
        输出文件路径
    """
    format1 = detect_format(file1)
    format2 = detect_format(file2)

    # 使用第一个文件的格式作为输出格式
    target_format = format1

    parser1 = PARSERS.get(format1)
    parser2 = PARSERS.get(format2)

    if not parser1 or not parser2:
        raise ValueError(f"不支持的格式: {format1} 或 {format2}")

    subs1 = parser1(file1)
    subs2 = parser2(file2)

    # 基于时间匹配合并
    merged = []
    used_indices = set()

    for sub1 in subs1:
        merged_text = sub1.text

        # 找到时间重叠的字幕
        best_match = None
        best_overlap = 0

        for i, sub2 in enumerate(subs2):
            if i in used_indices:
                continue

            # 计算时间重叠
            overlap_start = max(sub1.start, sub2.start)
            overlap_end = min(sub1.end, sub2.end)
            overlap = max(0, overlap_end - overlap_start)

            if overlap > best_overlap:
                best_overlap = overlap
                best_match = (i, sub2)

        if best_match and best_overlap > 0.5:  # 至少0.5秒重叠
            i, sub2 = best_match
            used_indices.add(i)
            merged_text = sub1.text + separator + sub2.text

        merged.append(
            Subtitle(
                index=len(merged) + 1, start=sub1.start, end=sub1.end, text=merged_text
            )
        )

    # 添加未匹配的第二个文件的字幕
    for i, sub2 in enumerate(subs2):
        if i not in used_indices:
            merged.append(
                Subtitle(
                    index=len(merged) + 1,
                    start=sub2.start,
                    end=sub2.end,
                    text=sub2.text,
                )
            )

    # 按时间排序
    merged.sort(key=lambda x: x.start)

    # 重新编号
    for i, sub in enumerate(merged):
        sub.index = i + 1

    # 生成输出
    generator = GENERATORS[target_format]
    content = generator(merged)

    if output_path is None:
        input_file = Path(file1)
        output_path = str(input_file.with_stem(input_file.stem + "_merged"))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


def batch_convert(
    directory: str,
    target_format: str,
    pattern: str = "*.*",
    output_dir: Optional[str] = None,
) -> List[str]:
    """
    批量转换目录下的字幕文件

    参数:
        directory: 目录路径
        target_format: 目标格式
        pattern: 文件匹配模式
        output_dir: 输出目录（可选，默认同目录）

    返回:
        转换后的文件路径列表
    """
    dir_path = Path(directory)
    results = []

    for file_path in dir_path.glob(pattern):
        if file_path.is_file():
            detected = detect_format(str(file_path))
            if detected in PARSERS and detected != target_format:
                try:
                    if output_dir:
                        out_dir = Path(output_dir)
                        out_dir.mkdir(parents=True, exist_ok=True)
                        output_path = str(
                            out_dir / file_path.with_suffix(f".{target_format}").name
                        )
                    else:
                        output_path = None

                    result = convert(str(file_path), output_path, target_format)
                    results.append(result)
                    print(f"✅ 转换完成: {file_path.name} -> {Path(result).name}")
                except Exception as e:
                    print(f"❌ 转换失败: {file_path.name} - {e}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="字幕格式转换工具 - 支持 VTT/SRT/ASS/LRC 互转",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s input.vtt --format srt              # VTT 转 SRT
  %(prog)s input.vtt --output out.srt          # 指定输出路径
  %(prog)s input.srt --shift 2.5               # 时间轴延后 2.5 秒
  %(prog)s input.srt --shift -1.0              # 时间轴提前 1 秒
  %(prog)s zh.srt en.srt --merge               # 合并双语字幕
  %(prog)s ./subs --batch --format srt         # 批量转换目录
        """,
    )

    parser.add_argument("inputs", nargs="+", help="输入文件或目录")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument(
        "--format", "-f", choices=["vtt", "srt", "ass", "lrc"], help="目标格式"
    )
    parser.add_argument("--shift", type=float, help="时间轴偏移秒数")
    parser.add_argument("--merge", action="store_true", help="合并两个字幕文件")
    parser.add_argument("--batch", action="store_true", help="批量处理目录")

    args = parser.parse_args()

    try:
        if args.batch:
            # 批量转换
            results = batch_convert(args.inputs[0], args.format, output_dir=args.output)
            print(f"\n📊 共转换 {len(results)} 个文件")

        elif args.merge:
            # 合并字幕
            if len(args.inputs) < 2:
                print("❌ 合并模式需要两个输入文件")
                sys.exit(1)
            result = merge_subtitles(args.inputs[0], args.inputs[1], args.output)
            print(f"✅ 合并完成: {result}")

        elif args.shift is not None:
            # 时间轴偏移
            result = shift_timeline(args.inputs[0], args.shift, args.output)
            print(f"✅ 偏移完成: {result}")

        else:
            # 格式转换
            result = convert(args.inputs[0], args.output, args.format)
            print(f"✅ 转换完成: {result}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
