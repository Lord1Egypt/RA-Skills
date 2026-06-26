#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时序对齐模块 (Timing Alignment Module)

防止配音/画面/字幕错位。在渲染前执行，验证并修正时序。

核心功能:
  1. 音频-画面同步验证 (audio-video sync)
  2. 帧级对齐 (frame-level alignment)
  3. 字幕时间戳验证 (subtitle timestamp validation)
  4. 自动修正 (auto-fix drift)

用法:
  # 独立验证
  python timing_align.py --lesson lesson_01 --project ~/course-video-remotion

  # 作为 pipeline 步骤调用
  python timing_align.py --lesson lesson_01 --project ~/course-video-remotion --fix

  # 生成字幕SRT
  python timing_align.py --lesson lesson_01 --project ~/course-video-remotion --gen-srt
"""

import argparse
import json
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Windows GBK workaround
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
try:
    if sys.stdout and hasattr(sys.stdout, 'buffer'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr and hasattr(sys.stderr, 'buffer'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ─── 常量 ────────────────────────────────────────────────────────────────────
DEFAULT_FPS = 24
COVER_DURATION_SEC = 3
ENDING_DURATION_SEC = 3
MAX_DRIFT_FRAMES = 2        # 最大允许漂移帧数
MAX_DRIFT_SEC = 0.1         # 最大允许漂移秒数
MIN_AUDIO_SEC = 2.0         # 最短音频时长
MAX_AUDIO_SEC = 120.0       # 最长音频时长
AUDIO_PADDING_SEC = 0.3     # 音频尾部安全余量（秒）


# ─── 数据结构 ────────────────────────────────────────────────────────────────
@dataclass
class SlideTiming:
    """单个slide的时序信息"""
    slide_id: str
    is_cover: bool = False
    audio_file: Optional[str] = None
    audio_duration_sec: float = 0.0      # 实际音频时长
    video_duration_frames: int = 0       # 视频帧数
    video_duration_sec: float = 0.0      # 视频时长（由帧数换算）
    start_frame: int = 0                 # 起始帧
    end_frame: int = 0                   # 结束帧
    drift_frames: float = 0.0            # 漂移帧数（正=视频长，负=音频长）
    drift_sec: float = 0.0               # 漂移秒数
    status: str = 'pending'              # pending | ok | drift | missing | too_short | too_long

    @property
    def duration_frames(self) -> int:
        """该slide占用的帧数"""
        return self.end_frame - self.start_frame


@dataclass
class TimingReport:
    """时序对齐报告"""
    lesson_name: str
    fps: int
    total_frames: int = 0
    total_duration_sec: float = 0.0
    slide_timings: list = field(default_factory=list)
    issues: list = field(default_factory=list)
    overall_status: str = 'pending'  # pending | pass | fail

    @property
    def issue_count(self) -> int:
        return len(self.issues)

    @property
    def critical_issues(self) -> list:
        return [i for i in self.issues if i.get('severity') == 'critical']


# ─── 核心功能 ────────────────────────────────────────────────────────────────

def get_audio_duration(audio_path: Path) -> float:
    """用ffprobe获取音频精确时长（秒）"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'csv=p=0', str(audio_path)],
            capture_output=True, text=True, timeout=30
        )
        dur = float(result.stdout.strip())
        if dur > 0:
            return round(dur, 3)
    except (ValueError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return 0.0


def get_video_duration(video_path: Path) -> float:
    """用ffprobe获取视频精确时长（秒）"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'csv=p=0', str(video_path)],
            capture_output=True, text=True, timeout=30
        )
        dur = float(result.stdout.strip())
        if dur > 0:
            return round(dur, 3)
    except (ValueError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return 0.0


def frames_to_sec(frames: int, fps: int) -> float:
    """帧数转秒数"""
    return round(frames / fps, 3)


def sec_to_frames(seconds: float, fps: int) -> int:
    """秒数转帧数（向上取整，确保音频不超出画面）"""
    return math.ceil(seconds * fps)


def sec_to_frames_safe(seconds: float, fps: int, padding_sec: float = AUDIO_PADDING_SEC) -> int:
    """秒数转帧数（含安全余量，画面比音频多padding_sec秒）"""
    return math.ceil((seconds + padding_sec) * fps)


# ─── 时序分析 ────────────────────────────────────────────────────────────────

def load_pipeline_data(project_dir: Path, lesson_name: str, fps: int = DEFAULT_FPS) -> dict:
    """加载pipeline所需的全部时序数据"""
    lesson_dir = project_dir / 'src' / 'slides' / lesson_name
    audio_dir = project_dir / 'public' / 'audio' / lesson_name

    # 读取slide_map.json
    slide_map_path = lesson_dir / 'slide_map.json'
    if not slide_map_path.exists():
        raise FileNotFoundError(f'slide_map.json not found: {slide_map_path}')
    slide_map = json.loads(slide_map_path.read_text(encoding='utf-8'))

    # 读取narration.json
    narration_path = lesson_dir / 'narration.json'
    narration = []
    if narration_path.exists():
        narration = json.loads(narration_path.read_text(encoding='utf-8'))

    # 读取durations.json（TTS生成的音频时长）
    durations_path = audio_dir / 'durations.json'
    durations = {}
    if durations_path.exists():
        durations = json.loads(durations_path.read_text(encoding='utf-8'))

    # 读取现有Composition中的durations（如果存在）
    comp_name = ''.join(w.capitalize() for w in lesson_name.split('_')) + 'Composition'
    comp_path = project_dir / 'src' / 'compositions' / f'{comp_name}.tsx'
    comp_durations = {}
    if comp_path.exists():
        comp_text = comp_path.read_text(encoding='utf-8')
        # 从slide_map中提取durations引用
        for entry in slide_map:
            audio_file = entry.get('audioFile')
            if audio_file and audio_file != 'null':
                key = audio_file.strip("'")
                if key in durations:
                    comp_durations[key] = durations[key]

    return {
        'slide_map': slide_map,
        'narration': narration,
        'durations': durations,
        'comp_durations': comp_durations,
        'comp_path': comp_path,
        'audio_dir': audio_dir,
        'lesson_dir': lesson_dir,
    }


def analyze_timing(data: dict, fps: int = DEFAULT_FPS) -> TimingReport:
    """分析时序对齐，生成报告"""
    lesson_name = data['lesson_dir'].name
    report = TimingReport(lesson_name=lesson_name, fps=fps)

    slide_map = data['slide_map']
    durations = data['durations']
    audio_dir = data['audio_dir']

    current_frame = 0

    for entry in slide_map:
        slide_id = entry['id']
        is_cover = entry.get('isCover', False)
        audio_file = entry.get('audioFile')

        timing = SlideTiming(slide_id=slide_id, is_cover=is_cover)
        timing.start_frame = current_frame

        if is_cover:
            # 封面：固定时长
            timing.video_duration_frames = sec_to_frames(COVER_DURATION_SEC, fps)
            timing.video_duration_sec = COVER_DURATION_SEC
            timing.audio_duration_sec = 0.0
            timing.status = 'ok'
        else:
            # 内容slide
            if audio_file and audio_file != 'null':
                audio_file_clean = audio_file.strip("'")
                timing.audio_file = audio_file_clean

                # 获取音频实际时长
                audio_path = audio_dir / audio_file_clean
                if audio_path.exists():
                    timing.audio_duration_sec = get_audio_duration(audio_path)
                elif audio_file_clean in durations:
                    timing.audio_duration_sec = durations[audio_file_clean]

                # 验证音频时长范围
                if timing.audio_duration_sec < MIN_AUDIO_SEC:
                    timing.status = 'too_short'
                    report.issues.append({
                        'slide_id': slide_id,
                        'severity': 'critical',
                        'type': 'audio_too_short',
                        'message': f'音频太短: {timing.audio_duration_sec:.1f}s < {MIN_AUDIO_SEC}s',
                    })
                elif timing.audio_duration_sec > MAX_AUDIO_SEC:
                    timing.status = 'too_long'
                    report.issues.append({
                        'slide_id': slide_id,
                        'severity': 'warning',
                        'type': 'audio_too_long',
                        'message': f'音频过长: {timing.audio_duration_sec:.1f}s > {MAX_AUDIO_SEC}s',
                    })

                # 计算视频帧数（含安全余量）
                timing.video_duration_frames = sec_to_frames_safe(
                    timing.audio_duration_sec, fps, AUDIO_PADDING_SEC
                )
                timing.video_duration_sec = frames_to_sec(timing.video_duration_frames, fps)

                # 计算漂移
                timing.drift_frames = timing.video_duration_frames - sec_to_frames(timing.audio_duration_sec, fps)
                timing.drift_sec = timing.video_duration_sec - timing.audio_duration_sec

                # 判断状态
                # 正漂移 = 视频比音频长（安全余量，正常）
                # 负漂移 = 视频比音频短（音频被截断，严重）
                if timing.drift_frames >= 0:
                    # 正漂移：视频长于音频，安全余量，正常
                    timing.status = 'ok'
                elif abs(timing.drift_frames) <= MAX_DRIFT_FRAMES:
                    # 微小负漂移：可接受
                    timing.status = 'ok'
                else:
                    # 严重负漂移：视频短于音频，音频会被截断
                    timing.status = 'drift'
                    report.issues.append({
                        'slide_id': slide_id,
                        'severity': 'critical',
                        'type': 'audio_video_drift',
                        'message': f'视频短于音频: {timing.drift_frames:.1f}帧 ({timing.drift_sec:.3f}s)，音频将被截断',
                    })
            else:
                # 无音频的slide，使用默认时长
                timing.video_duration_frames = sec_to_frames(5, fps)
                timing.video_duration_sec = 5.0
                timing.status = 'ok'

        timing.end_frame = current_frame + timing.video_duration_frames
        current_frame = timing.end_frame
        report.slide_timings.append(timing)

    # 结尾
    end_start_frame = current_frame
    end_frames = sec_to_frames(ENDING_DURATION_SEC, fps)
    total_frames = end_start_frame + end_frames
    total_duration = frames_to_sec(total_frames, fps)

    report.total_frames = total_frames
    report.total_duration_sec = total_duration

    # 检查音频文件完整性
    for entry in slide_map:
        if entry.get('isCover'):
            continue
        audio_file = entry.get('audioFile')
        if audio_file and audio_file != 'null':
            audio_file_clean = audio_file.strip("'")
            audio_path = audio_dir / audio_file_clean
            if not audio_path.exists():
                report.issues.append({
                    'slide_id': entry['id'],
                    'severity': 'critical',
                    'type': 'audio_missing',
                    'message': f'音频文件不存在: {audio_path}',
                })

    # 检查slide_map和narration的ID一致性
    narration_ids = set()
    for n in data.get('narration', []):
        narration_ids.add(n.get('id', ''))
    for entry in slide_map:
        sid = entry['id']
        nid = entry.get('narrationId', sid)
        if narration_ids and nid not in narration_ids:
            report.issues.append({
                'slide_id': sid,
                'severity': 'warning',
                'type': 'narration_id_mismatch',
                'message': f'slide_map ID "{sid}" 在narration中找不到对应项',
            })

    # 总体状态
    critical = report.critical_issues
    if critical:
        report.overall_status = 'fail'
    elif report.issues:
        report.overall_status = 'pass'  # 有warning但可渲染
    else:
        report.overall_status = 'pass'

    return report


# ─── 自动修正 ────────────────────────────────────────────────────────────────

def fix_composition_durations(data: dict, report: TimingReport, fps: int = DEFAULT_FPS) -> bool:
    """修正Composition中的durations，使音画同步"""
    comp_path = data['comp_path']
    if not comp_path.exists():
        print(f"  [FIX] Composition不存在，跳过修正: {comp_path}")
        return False

    comp_text = comp_path.read_text(encoding='utf-8')

    # 构建修正后的durations映射
    fixed_durations = {}
    for timing in report.slide_timings:
        if timing.audio_file and timing.audio_duration_sec > 0:
            # 使用修正后的视频时长（含安全余量）
            fixed_durations[timing.audio_file] = round(timing.video_duration_sec, 2)

    if not fixed_durations:
        print("  [FIX] 无可修正的durations")
        return False

    # 更新durations.json
    durations_path = data['audio_dir'] / 'durations.json'
    if durations_path.exists():
        existing = json.loads(durations_path.read_text(encoding='utf-8'))
        existing.update(fixed_durations)
        durations_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"  [FIX] 已更新 durations.json ({len(fixed_durations)} 项)")

    return True


def regenerate_composition_with_timing(data: dict, report: TimingReport, fps: int = DEFAULT_FPS) -> bool:
    """重新生成Composition TSX，使用修正后的时序"""
    lesson_name = data['lesson_dir'].name
    slide_map = data['slide_map']

    # 生成 import 和 SLIDES 数组
    imports = []
    slides_entries = []
    for entry in slide_map:
        tsx = entry['component']
        imports.append(f"import {{ {tsx} }} from '../slides/{lesson_name}/{tsx}';")

        audio = entry.get('audioFile')
        audio_str = f"'{audio}'" if audio else 'null'
        is_cover = str(entry.get('isCover', False)).lower()
        slides_entries.append(
            f"  {{ id: '{entry['id']}', component: {tsx}, "
            f"audioFile: {audio_str}, isCover: {is_cover} }},"
        )

    comp_name = ''.join(w.capitalize() for w in lesson_name.split('_')) + 'Composition'

    # 构建修正后的durations映射（用于Composition）
    timing_map = {}
    for timing in report.slide_timings:
        if timing.audio_file:
            timing_map[timing.audio_file] = round(timing.video_duration_sec, 2)

    content_lines = [
        "import React from 'react';",
        "import { Audio, Sequence, staticFile, useVideoConfig } from 'remotion';",
        "import { VIDEO_CONFIG, COVER_DURATION, ENDING_DURATION } from '../utils/constants';",
        "import { BackCover } from '../components/BackCover';",
        "",
    ]
    content_lines.extend(imports)
    content_lines.extend([
        "",
        "interface Props {",
        "  lessonId: string;",
        "  durations?: Record<string, number>;",
        "}",
        "",
        "const SLIDES = [",
    ])
    content_lines.extend(slides_entries)
    content_lines.extend([
        "];",
        "",
        f"export const {comp_name}: React.FC<Props> = ({{ lessonId, durations }}) => {{",
        "  const { fps } = useVideoConfig();",
        "  const dirName = lessonId.replace(/-/g, '_');",
        "",
        "  // ─── 时序对齐：使用修正后的durations ───",
        "  const TIMING_ALIGN_DURATIONS: Record<string, number> = {",
    ])
    for audio_file, dur in timing_map.items():
        content_lines.append(f"    '{audio_file}': {dur},")
    content_lines.extend([
        "  };",
        "",
        "  let currentFrame = 0;",
        "  const timeline = SLIDES.map((slide) => {",
        "    let frames: number;",
        "    if (slide.isCover) {",
        "      frames = Math.ceil(COVER_DURATION * fps);",
        "    } else {",
        "      // 优先使用修正后的durations，其次使用传入的durations，最后fallback",
        "      const dur = TIMING_ALIGN_DURATIONS[slide.audioFile!]",
        "        ?? durations?.[slide.audioFile!]",
        "        ?? 5;",
        "      frames = Math.ceil(dur * fps);",
        "    }",
        "    const start = currentFrame;",
        "    currentFrame += frames;",
        "    return { ...slide, start, frames };",
        "  });",
        "",
        "  const backCoverStart = currentFrame;",
        "  const backCoverFrames = Math.ceil(ENDING_DURATION * fps);",
        "",
        "  return (",
        "    <div style={{ position: 'relative', width: VIDEO_CONFIG.width, height: VIDEO_CONFIG.height }}>",
        "      {timeline.map((slide) => {",
        "        const SlideComponent = slide.component;",
        "        return (",
        "          <Sequence key={slide.id} from={slide.start} durationInFrames={slide.frames} name={String(slide.id)}>",
        "            <SlideComponent />",
        "            {!slide.isCover && slide.audioFile && (",
        "              <Audio src={staticFile(`audio/${dirName}/${slide.audioFile}`)} />",
        "            )}",
        "          </Sequence>",
        "        );",
        "      })}",
        '      <Sequence from={backCoverStart} durationInFrames={backCoverFrames} name="back-cover">',
        "        <BackCover />",
        "      </Sequence>",
        "    </div>",
        "  );",
        "};",
        "",
    ])
    content = '\n'.join(content_lines)

    comp_path = data['comp_path']
    comp_path.write_text(content, encoding='utf-8')
    print(f"  [FIX] 已重新生成 Composition: {comp_path} ({len(slide_map)} slides)")
    return True


# ─── 字幕生成 ────────────────────────────────────────────────────────────────

def generate_subtitle_srt(data: dict, report: TimingReport, fps: int = DEFAULT_FPS) -> Optional[Path]:
    """根据时序数据生成SRT字幕文件"""
    lesson_name = data['lesson_dir'].name
    narration = data.get('narration', [])
    if not narration:
        print("  [SRT] 无narration数据，跳过字幕生成")
        return None

    # 构建narration映射
    narration_map = {}
    for n in narration:
        narration_map[n['id']] = n.get('narration', '')

    srt_lines = []
    idx = 1

    for timing in report.slide_timings:
        if timing.is_cover or not timing.audio_file:
            continue

        text = narration_map.get(timing.slide_id, '')
        if not text:
            continue

        start_sec = frames_to_sec(timing.start_frame, fps)
        end_sec = frames_to_sec(timing.end_frame, fps)

        srt_lines.append(str(idx))
        srt_lines.append(f"{_format_srt_time(start_sec)} --> {_format_srt_time(end_sec)}")
        srt_lines.append(text)
        srt_lines.append("")
        idx += 1

    if not srt_lines:
        print("  [SRT] 无有效字幕内容")
        return None

    srt_path = data['lesson_dir'] / f'{lesson_name}.srt'
    srt_path.write_text('\n'.join(srt_lines), encoding='utf-8')
    print(f"  [SRT] 已生成字幕文件: {srt_path} ({idx - 1} 条)")
    return srt_path


def _format_srt_time(seconds: float) -> str:
    """秒数转SRT时间格式 HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# ─── 报告输出 ────────────────────────────────────────────────────────────────

def print_report(report: TimingReport):
    """打印时序对齐报告"""
    print("\n" + "=" * 60)
    print("时序对齐报告")
    print("=" * 60)
    print(f"  课程:        {report.lesson_name}")
    print(f"  FPS:         {report.fps}")
    print(f"  总帧数:      {report.total_frames}")
    print(f"  总时长:      {report.total_duration_sec:.1f}s ({report.total_duration_sec/60:.1f}min)")
    print(f"  Slide数:     {len(report.slide_timings)}")
    print(f"  问题数:      {report.issue_count}")
    print(f"  总体状态:    {report.overall_status.upper()}")
    print("-" * 60)

    for t in report.slide_timings:
        status_icon = {'ok': '✅', 'drift': '⚠️', 'missing': '❌', 'too_short': '❌', 'too_long': '⚠️'}.get(t.status, '❓')
        audio_info = f"{t.audio_duration_sec:.1f}s" if t.audio_duration_sec > 0 else "N/A"
        print(f"  {status_icon} {t.slide_id:<20s} | 音频:{audio_info:>8s} | "
              f"视频:{t.video_duration_frames:>4d}帧({t.video_duration_sec:.1f}s) | "
              f"漂移:{t.drift_frames:+.1f}帧")

    if report.issues:
        print("\n  问题列表:")
        for issue in report.issues:
            sev = issue.get('severity', 'info').upper()
            print(f"    [{sev}] {issue['slide_id']}: {issue['message']}")

    print("=" * 60)


# ─── CLI入口 ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='时序对齐模块 - 防止配音/画面/字幕错位',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='示例:\n'
               '  python timing_align.py --lesson lesson_01 --project ~/course-video-remotion\n'
               '  python timing_align.py --lesson lesson_01 --project ~/course-video-remotion --fix\n'
               '  python timing_align.py --lesson lesson_01 --project ~/course-video-remotion --gen-srt\n',
    )
    parser.add_argument('--lesson', required=True, help='课程名称 (如 lesson_01)')
    parser.add_argument('--project', required=True, help='项目路径')
    parser.add_argument('--fps', type=int, default=DEFAULT_FPS, help=f'帧率 (默认 {DEFAULT_FPS})')
    parser.add_argument('--fix', action='store_true', help='自动修正时序问题')
    parser.add_argument('--gen-srt', action='store_true', help='生成SRT字幕文件')
    parser.add_argument('--json', dest='json_output', action='store_true', help='输出JSON格式报告')
    args = parser.parse_args()

    project_dir = Path(args.project)
    lesson_name = args.lesson
    fps = args.fps

    print(f"时序对齐检查: {lesson_name} @ {fps}fps")
    print(f"项目路径: {project_dir}")

    # 加载数据
    data = load_pipeline_data(project_dir, lesson_name, fps)

    # 分析时序
    report = analyze_timing(data, fps)

    # 输出报告
    if args.json_output:
        report_json = {
            'lesson': report.lesson_name,
            'fps': report.fps,
            'total_frames': report.total_frames,
            'total_duration_sec': report.total_duration_sec,
            'slide_count': len(report.slide_timings),
            'issue_count': report.issue_count,
            'overall_status': report.overall_status,
            'slides': [
                {
                    'slide_id': t.slide_id,
                    'is_cover': t.is_cover,
                    'audio_file': t.audio_file,
                    'audio_duration_sec': t.audio_duration_sec,
                    'video_duration_frames': t.video_duration_frames,
                    'video_duration_sec': t.video_duration_sec,
                    'drift_frames': t.drift_frames,
                    'drift_sec': t.drift_sec,
                    'status': t.status,
                }
                for t in report.slide_timings
            ],
            'issues': report.issues,
        }
        print(json.dumps(report_json, indent=2, ensure_ascii=False))
    else:
        print_report(report)

    # 自动修正
    if args.fix and report.issues:
        print("\n执行自动修正...")
        fix_composition_durations(data, report, fps)
        regenerate_composition_with_timing(data, report, fps)
        print("修正完成")

    # 生成字幕
    if args.gen_srt:
        print("\n生成SRT字幕...")
        srt_path = generate_subtitle_srt(data, report, fps)
        if srt_path:
            print(f"字幕已生成: {srt_path}")

    # 退出码
    if report.overall_status == 'fail':
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
