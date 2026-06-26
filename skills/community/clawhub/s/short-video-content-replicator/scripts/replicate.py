"""
Skill Name: universal-voice-cloner
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: 
"""

import typer
from pathlib import Path
import subprocess
from typing import Optional
from rich.console import Console

console = Console()
app = typer.Typer(help="短视频内容复制工作流 - 一键执行6步处理")


def run_script(cmd: list[str], step_name: str) -> bool:
    """统一执行子脚本，带友好日志、错误捕获和输出显示"""
    try:
        console.print(f"\n[bold cyan]▶ Step {step_name}[/bold cyan]")
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        console.print(f"[bold green]✓ Step {step_name} 完成[/bold green]")
        if result.stdout.strip():
            console.print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✗ Step {step_name} 执行失败[/bold red]")
        if e.stderr:
            console.print(f"[red]错误信息：{e.stderr.strip()}[/red]")
        elif e.stdout:
            console.print(f"[red]{e.stdout.strip()}[/red]")
        raise  # 让 Typer/OpenClaw 能捕获错误，方便调试
    except FileNotFoundError:
        console.print(f"[bold red]✗ Step {step_name} 失败：脚本文件未找到[/bold red]")
        console.print(f"[red]请检查路径：{' '.join(cmd)}[/red]")
        raise


@app.command()
def replicate(
    input_path: str = typer.Argument(..., help="视频URL 或 本地视频/MP3/wav/txt 目录或文件路径"),
    output: Optional[Path] = typer.Option("./output", "--output", "-o", help="总输出根目录"),
    start_from: str = typer.Option("step1", "--start-from", help="从哪一步开始 (step1~step6)"),
    # 各步骤自定义输出目录
    videos_dir: Optional[Path] = typer.Option(None, "--videos-dir"),
    mp3_dir: Optional[Path] = typer.Option(None, "--mp3-dir"),
    vocals_dir: Optional[Path] = typer.Option(None, "--vocals-dir"),
    transcripts_dir: Optional[Path] = typer.Option(None, "--transcripts-dir"),
    corrected_dir: Optional[Path] = typer.Option(None, "--corrected-dir"),
    final_dir: Optional[Path] = typer.Option(None, "--final-dir"),
):
    # ==================== 路径计算（关键优化）====================
    # 假设目录结构：
    # skills/
    #   ├── short-video-content-replicator/
    #   │   ├── scripts/
    #   │   │   └── replicate.py          ← 当前文件
    #   │   └── SKILL.md
    #   ├── link-resolver-engine/
    #   ├── mp4-to-mp3-extractor/
    #   ├── purevocals-uvr-automator/
    #   └── ...（其他原子技能）
    script_dir = Path(__file__).parent.resolve()           # replicate.py 所在 scripts/ 目录
    skill_root = script_dir.parent.resolve()               # short-video-content-replicator 目录
    skills_root = skill_root.parent.resolve()              # 顶层 skills/ 目录（所有技能同级）

    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)

    # 默认各步骤目录
    dirs = {
        "videos": videos_dir or output / "videos",
        "mp3": mp3_dir or output / "mp3",
        "vocals": vocals_dir or output / "vocals",
        "transcripts": transcripts_dir or output / "transcripts",
        "corrected": corrected_dir or output / "corrected",
        "final": final_dir or output / "final",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    console.print("[bold green]🚀 Short Video Content Replicator 开始运行[/bold green]")
    console.print(f"输入路径: {input_path}")
    console.print(f"输出根目录: {output}")

    # 解析 start_from（更安全）
    try:
        start_step = int(start_from.lower().replace("step", "").strip())
        if not 1 <= start_step <= 6:
            raise ValueError
    except ValueError:
        console.print("[bold red]错误：--start-from 必须是 step1~step6[/bold red]")
        raise typer.Exit(1)

    # ====================== 严格顺序执行 ======================
    # Step 1: 视频下载（使用 link-resolver-engine 的脚本）
    if start_step <= 1:
        run_script([
            "python",
            str(script_dir / "video_snapper.py"),      # 你可以把 video_snapper.py 放在本 skill 的 scripts/ 下
            "-u", input_path,
            "-d", str(dirs["videos"])
        ], "1: 下载视频")

    # Step 2: MP4 → MP3
    if start_step <= 2:
        source = dirs["videos"] if start_step <= 1 else Path(input_path)
        run_script([
            "python",
            str(skills_root / "mp4-to-mp3-extractor" / "scripts" / "extract.py"),
            str(source),
            str(dirs["mp3"])
        ], "2: MP4 转 MP3")

    # Step 3: 人声分离（提取干声）
    if start_step <= 3:
        source = dirs["mp3"] if start_step <= 2 else Path(input_path)
        run_script([
            "python",
            str(skills_root / "purevocals-uvr-automator" / "scripts" / "purevocals.py"),
            str(source),
            str(dirs["vocals"]),
            "--model", "VR",
            "--window_size", "512",
            "--aggression", "10"
        ], "3: 提取干声")

    # Step 4: Whisper 本地转录
    if start_step <= 4:
        source = dirs["vocals"] if start_step <= 3 else Path(input_path)
        run_script([
            "python",
            str(script_dir / "audio_to_text.py"),      # 本 skill 自己的 wrapper 脚本
            "--audio_path", str(source),
            "--output_dir", str(dirs["transcripts"]),
            "--language", "zh",
            "--output", "text"
        ], "4: Whisper 本地转录")

    # Step 5: LLM 文本纠错
    if start_step <= 5:
        source = dirs["transcripts"] if start_step <= 4 else Path(input_path)
        run_script([
            "python",
            str(script_dir / "correct_text.py"),
            str(source),
            "--refine"
        ], "5: LLM 文本纠错")

    # Step 6: 标点恢复
    if start_step <= 6:
        source = dirs["corrected"] if start_step <= 5 else Path(input_path)
        run_script([
            "python",
            str(script_dir / "punctuation_restore.py"),
            "--dir", str(source)
        ], "6: 标点恢复")

    console.print("\n[bold green]✅ 全部6步处理完成！[/bold green]")
    console.print(f"最终结果目录: {dirs['final']}")
    console.print("[bold green]🎉 短视频内容复制工作流执行完毕[/bold green]")


if __name__ == "__main__":
    app()