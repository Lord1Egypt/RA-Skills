#!/usr/bin/env python3
"""
videogen v2 — Remotion 渲染执行器

用法：
    python run_remotion_render.py render \
        --project /path/to/remotion-project/ \
        --composition Video \
        --output /path/to/output.mp4 \
        --audio /path/to/voiceover.mp3 \
        --subtitles /path/to/subtitles.srt

    python run_remotion_render.py setup --project /path/to/project/
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


# ═══════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════

def run_cmd(cmd: list[str], cwd: Path, timeout: int = 600, **kwargs) -> subprocess.CompletedProcess:
    """执行命令，超时杀死"""
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        timeout=timeout,
        capture_output=True,
        text=True,
    )
    return result


# ═══════════════════════════════════════════════════════
# 设置
# ═══════════════════════════════════════════════════════

def cmd_setup(args):
    """设置 Remotion 项目"""
    project_dir = Path(args.project).resolve()

    # 优先用 videogen 自带的模板
    template_dir = Path(__file__).parent.parent.parent / "remotion-template"

    if not template_dir.exists():
        print(f"❌ 模板不存在: {template_dir}")
        return 1

    # 如果目录存在，先清空（用户确认）
    if project_dir.exists() and any(project_dir.iterdir()):
        if not args.force:
            print(f"⚠️  目录非空: {project_dir}，使用 --force 强制覆盖")
            return 1
        shutil.rmtree(project_dir)

    shutil.copytree(template_dir, project_dir)
    print(f"✅ Remotion 项目模板已复制到: {project_dir}")

    # npm install
    print(f"\n📦 安装依赖...")
    result = run_cmd(["npm", "install"], cwd=project_dir, timeout=300)
    if result.returncode != 0:
        print(f"❌ npm install 失败:\n{result.stderr[-500:]}")
        return 1
    print(f"✅ 依赖安装完成")
    return 0


# ═══════════════════════════════════════════════════════
# 代码生成
# ═══════════════════════════════════════════════════════

def cmd_generate(args):
    """生成 Remotion 代码"""
    from remotion_generator import cmd_gen as _gen

    class Args:
        scene_names = args.scene_names
        timings = args.timings
        narrations = args.narrations
        visuals = args.visuals
        output = args.project

    _gen(Args())
    return 0


# ═══════════════════════════════════════════════════════
# 渲染
# ═══════════════════════════════════════════════════════

def _merge_audio_video(video_path: Path, audio_path: Path, output_path: Path) -> bool:
    """
    合并视频和音频：
    1. 把音频转成 AAC
    2. 用 filter_complex 合并（不用 stream copy，避免 Remotion 嵌入的默认音频问题）
    3. 用 -shortest 取较短者
    """
    tmp_aac = output_path.parent / "tmp_audio.aac"

    # 转码音频为 AAC 48kHz
    cmd_convert = [
        "ffmpeg", "-y",
        "-i", str(audio_path),
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
        str(tmp_aac),
    ]
    r = subprocess.run(cmd_convert, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"  ⚠️  音频转码失败: {r.stderr[-200:]}")
        return False

    # 合并音视频（视频流直接复制，音频重新编码）
    cmd_merge = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(tmp_aac),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(output_path),
    ]
    r = subprocess.run(cmd_merge, capture_output=True, text=True, timeout=120)
    tmp_aac.unlink(missing_ok=True)

    if r.returncode != 0:
        print(f"  ⚠️  音视频合并失败: {r.stderr[-200:]}")
        return False

    return True


def _burn_subtitles(video_path: Path, srt_path: Path, output_path: Path) -> bool:
    """
    烧录字幕到视频（软字幕方式）：
    1. 先检查视频编码是否支持字幕流
    2. 用 ffmpeg subtitles 滤镜烧录
    3. 如果失败，fallback 为软字幕封装
    """
    # 方式1：直接烧录
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"subtitles={srt_path}",
        "-c:v", "copy",
        "-c:a", "copy",
        str(output_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode == 0:
        return True

    # 方式2：软字幕封装（mkv）
    mkv_path = output_path.with_suffix(".mkv")
    cmd_mkv = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(srt_path),
        "-c:v", "copy",
        "-c:a", "copy",
        "-c:s", "mov_text",
        str(mkv_path),
    ]
    r2 = subprocess.run(cmd_mkv, capture_output=True, text=True, timeout=60)
    if r2.returncode == 0:
        # 转换回 mp4
        cmd_final = [
            "ffmpeg", "-y",
            "-i", str(mkv_path),
            "-c:v", "copy",
            "-c:a", "copy",
            "-c:s", "mov_text",
            str(output_path),
        ]
        r3 = subprocess.run(cmd_final, capture_output=True, text=True, timeout=60)
        mkv_path.unlink(missing_ok=True)
        if r3.returncode == 0:
            return True

    print(f"  ⚠️  字幕烧录失败: {r.stderr[-200:]}")
    return False


def cmd_render(args):
    """渲染 Remotion 视频"""
    project_dir = Path(args.project).resolve()
    raw_output = project_dir / "out" / "raw.mp4"
    output_path = Path(args.output) if args.output else project_dir / "out" / "video_final.mp4"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 检查 node_modules
    if not (project_dir / "node_modules").exists():
        print(f"📦 node_modules 不存在，先安装依赖...")
        result = run_cmd(["npm", "install"], cwd=project_dir, timeout=300)
        if result.returncode != 0:
            print(f"❌ npm install 失败:\n{result.stderr[-500:]}")
            return 1

    # 执行渲染
    print(f"\n🎬 开始渲染...")
    print(f"  composition: {args.composition}")
    print(f"  输出: {raw_output}")

    cmd = [
        "npx", "remotion", "render",
        args.composition,
        "--output", str(raw_output),
        "--codec", "h264",
        "--quality", "0",
        "--overwrite",
    ]
    if args.framerate:
        cmd += ["--fps", str(args.framerate)]

    start_time = time.time()
    result = run_cmd(cmd, cwd=project_dir, timeout=args.timeout)

    if result.stdout:
        print(result.stdout[-500:])

    if result.returncode != 0:
        print(f"❌ 渲染失败:\n{result.stderr[-1000:]}")
        return 1

    # 合并音频
    final_output = output_path
    if args.audio and Path(args.audio).exists():
        print(f"\n🔊 合并音轨...")
        audio_ok = _merge_audio_video(raw_output, Path(args.audio), final_output)
        if audio_ok:
            print(f"  ✅ 音频已合并")
        else:
            print(f"  ⚠️  音频合并失败，视频将无声音")
            final_output = raw_output
    else:
        final_output = raw_output

    # 烧录字幕
    if args.subtitles and Path(args.subtitles).exists():
        print(f"\n💬 烧录字幕...")
        srt_ok = _burn_subtitles(final_output, Path(args.subtitles), final_output.with_name(final_output.stem + "_subtitled.mp4"))
        if srt_ok:
            print(f"  ✅ 字幕已烧录")
            final_output = final_output.with_name(final_output.stem + "_subtitled.mp4")
        else:
            print(f"  ⚠️  字幕烧录失败，跳过")

    duration = time.time() - start_time
    size_kb = final_output.stat().st_size / 1024 if final_output.exists() else 0

    print(f"\n{'='*50}")
    print(f"🎉 渲染完成!")
    print(f"  输出: {final_output}")
    print(f"  大小: {size_kb/1024:.1f} MB")
    print(f"  耗时: {duration:.0f} 秒")
    print(f"{'='*50}")

    return 0


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Remotion 渲染执行器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # setup
    p_setup = sub.add_parser("setup", help="设置 Remotion 项目（从模板复制）")
    p_setup.add_argument("--project", required=True, help="项目目录")
    p_setup.add_argument("--force", action="store_true", help="强制覆盖已有目录")

    # generate
    p_gen = sub.add_parser("generate", help="生成 Remotion 代码")
    p_gen.add_argument("--project", required=True, help="项目目录")
    p_gen.add_argument("--scene-names", required=True,
                       help="场景名称，用 | 分隔")
    p_gen.add_argument("--timings", default="",
                       help="各场景时长（秒），用 | 分隔")
    p_gen.add_argument("--narrations", default="",

                       help="各场景旁白，用 || 分隔")
    p_gen.add_argument("--visuals", default="",
                       help="视觉类型，用 | 分隔")

    # render
    p_render = sub.add_parser("render", help="渲染 Remotion 视频")
    p_render.add_argument("--project", required=True, help="Remotion 项目目录")
    p_render.add_argument("--composition", default="Video", help="Composition ID")
    p_render.add_argument("--output", help="输出路径")
    p_render.add_argument("--audio", help="配音文件路径")
    p_render.add_argument("--subtitles", help="字幕文件路径")
    p_render.add_argument("--framerate", type=int, default=30, help="帧率")
    p_render.add_argument("--timeout", type=int, default=1800, help="超时（秒）")

    args = parser.parse_args()

    if args.cmd == "setup":
        return cmd_setup(args)
    elif args.cmd == "generate":
        return cmd_generate(args)
    elif args.cmd == "render":
        return cmd_render(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
