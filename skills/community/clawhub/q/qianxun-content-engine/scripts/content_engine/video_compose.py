"""视频编排（v0.3.0）：seedance-prompt.md → 多 shot 真生视频 → ffmpeg 拼接成片。

流程：
1. parse_shots(): 把 prompt 文件切成 N 个 Shot
2. compose(): 顺序执行 submit + poll + download，失败 shot 不阻断其他 shot
3. concat_with_ffmpeg(): 把成功 shot 拼成 final-video.mp4
4. write_partial_report(): 失败时输出 partial-video.md（含失败 prompt 方便手补）
"""

from __future__ import annotations
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .seedance import (
    DEFAULT_DURATION,
    DEFAULT_RATIO,
    DEFAULT_RESOLUTION,
    SeedanceError,
    TaskFailed,
    TaskTimeout,
    submit_and_wait,
    submit_task,
)


# `## Shot 1 (0-6s)` / `## Shot 2 (7–13s)` 都要识别（半角 - 和全角 –）
_SHOT_HEADER_RE = re.compile(
    r"^##\s*Shot\s*(\d+)\s*\(\s*(\d+)\s*[\-–]\s*(\d+)\s*s\s*\)",
    re.MULTILINE,
)


@dataclass
class Shot:
    index: int               # 1-based
    duration: int            # 秒（end - start）
    body: str                # 该 shot 的全部 prompt 正文（含 header 之后那一段 markdown）

    @property
    def prompt_text(self) -> str:
        """喂给 Seedance 的 prompt：把结构化 markdown 拼成自然语言一段。"""
        # 简化：直接发原 markdown 给模型；Seedance 能理解结构化字段
        return self.body.strip()


@dataclass
class ShotResult:
    shot: Shot
    success: bool
    video_path: Path | None = None  # 成功时本地 .mp4
    task_id: str | None = None
    error: str = ""                 # 失败时人类可读说明


@dataclass
class ComposeReport:
    shots_total: int
    shots_succeeded: int
    final_video: Path | None = None     # ffmpeg 拼接后的成片
    individual: list[ShotResult] = field(default_factory=list)
    skipped_concat_reason: str = ""     # 没拼时的原因

    @property
    def all_succeeded(self) -> bool:
        return self.shots_succeeded == self.shots_total

    @property
    def has_partial_failure(self) -> bool:
        return 0 < self.shots_succeeded < self.shots_total


# ─── 解析 ───

def parse_shots(seedance_md: str) -> list[Shot]:
    """从 seedance-prompt.md 切出 N 个 shot。

    格式约定（prompt_seedance_video 出的）：
        ## Shot 1 (0-3s)
        - Shot type: ...
        ## Shot 2 (3-8s)
        ...
    """
    matches = list(_SHOT_HEADER_RE.finditer(seedance_md))
    if not matches:
        return []

    shots: list[Shot] = []
    for i, m in enumerate(matches):
        idx = int(m.group(1))
        start_s = int(m.group(2))
        end_s = int(m.group(3))
        duration = max(1, end_s - start_s)

        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(seedance_md)
        body = seedance_md[body_start:body_end]

        shots.append(Shot(index=idx, duration=duration, body=body))
    return shots


# ─── 单 shot 执行 ───

def _generate_one_shot(
    shot: Shot,
    out_dir: Path,
    *,
    model: str | None,
    ratio: str,
    resolution: str,
    api_key: str | None,
    poll_timeout: int,
    poll_interval: int,
    on_progress=None,
) -> ShotResult:
    """单个 shot 的 submit + poll + download。失败不抛，包成 ShotResult。"""
    out_path = out_dir / f"shot_{shot.index:02d}.mp4"
    try:
        result_path, task_id = submit_and_wait(
            shot.prompt_text,
            out_path,
            model=model,
            duration=shot.duration,
            ratio=ratio,
            resolution=resolution,
            api_key=api_key,
            poll_timeout=poll_timeout,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ShotResult(shot=shot, success=True, video_path=result_path, task_id=task_id)
    except (SeedanceError, TaskFailed, TaskTimeout) as e:
        return ShotResult(shot=shot, success=False, error=str(e))


# ─── 主入口 ───

def compose(
    seedance_md: str,
    out_dir: Path,
    *,
    model: str | None = None,
    ratio: str = DEFAULT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    api_key: str | None = None,
    poll_timeout: int = 600,
    poll_interval: int = 8,
    on_shot_progress=None,  # callable(shot_idx, status, elapsed)
    skip_concat: bool = False,
) -> ComposeReport:
    """顺序生成所有 shot 的视频，再 ffmpeg 拼接。

    顺序而非并发：火山 Ark 单账号有 QPS 限制，且视频任务本身就慢，
    并发收益小但限流风险大。

    Args:
        seedance_md: seedance-prompt.md 全文
        out_dir: 输出目录（GEN-xxx-video/shots/）
        skip_concat: 测试用，跳过 ffmpeg

    Returns:
        ComposeReport
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    shots = parse_shots(seedance_md)
    if not shots:
        return ComposeReport(
            shots_total=0, shots_succeeded=0,
            skipped_concat_reason="seedance-prompt.md 解析不出 shot（## Shot N 格式不对）",
        )

    results: list[ShotResult] = []
    for shot in shots:
        progress_cb = None
        if on_shot_progress:
            def _cb(status, elapsed, _idx=shot.index):
                on_shot_progress(_idx, status, elapsed)
            progress_cb = _cb

        result = _generate_one_shot(
            shot, out_dir,
            model=model, ratio=ratio, resolution=resolution,
            api_key=api_key,
            poll_timeout=poll_timeout, poll_interval=poll_interval,
            on_progress=progress_cb,
        )
        results.append(result)

    successes = [r for r in results if r.success]
    report = ComposeReport(
        shots_total=len(shots),
        shots_succeeded=len(successes),
        individual=results,
    )

    # 拼接（all-fail 优先于 skip_concat，因为它反映真实状态）
    if not successes:
        report.skipped_concat_reason = "全部 shot 都失败，无法拼接"
        return report

    if skip_concat:
        report.skipped_concat_reason = "skip_concat=True (test)"
        return report

    final_path = out_dir.parent / "final-video.mp4"
    try:
        concat_with_ffmpeg([r.video_path for r in successes], final_path)
        report.final_video = final_path
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        report.skipped_concat_reason = f"ffmpeg 拼接失败：{e}"

    return report


# ─── ffmpeg 拼接 ───

def concat_with_ffmpeg(video_paths: list[Path], out_path: Path) -> Path:
    """用 ffmpeg concat demuxer 把多个 mp4 无损拼成 1 个。

    要求所有输入是相同编码 / 分辨率（Seedance 同次任务输出参数一致）。

    Raises:
        FileNotFoundError: ffmpeg 不在 PATH
        subprocess.CalledProcessError: ffmpeg 拼接失败
    """
    if not shutil.which("ffmpeg"):
        raise FileNotFoundError("ffmpeg 不在 PATH，无法拼接视频。安装：brew install ffmpeg")
    if not video_paths:
        raise ValueError("video_paths 为空")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # ffmpeg concat 协议要求一个文本清单文件
    with tempfile.NamedTemporaryFile(
        "w", suffix=".txt", delete=False, encoding="utf-8",
    ) as f:
        for p in video_paths:
            # ffmpeg 单引号包路径，自身的 ' 转成 '\''
            safe = str(p.absolute()).replace("'", "'\\''")
            f.write(f"file '{safe}'\n")
        list_file = f.name

    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
             "-i", list_file, "-c", "copy", str(out_path)],
            check=True, capture_output=True,
        )
    finally:
        Path(list_file).unlink(missing_ok=True)

    return out_path


# ─── partial-video 报告 ───

def write_partial_report(report: ComposeReport, out_path: Path) -> Path:
    """失败时写一个 markdown 报告，包含每个失败 shot 的 prompt 让用户能手动重跑。"""
    lines = [
        "# Partial Video Report",
        "",
        f"**Shots total**: {report.shots_total}",
        f"**Succeeded**: {report.shots_succeeded}",
        f"**Failed**: {report.shots_total - report.shots_succeeded}",
        "",
    ]
    if report.final_video:
        lines.append(f"✅ 已拼接成片：`{report.final_video}`（用了 {report.shots_succeeded} 个成功的 shot）")
    elif report.skipped_concat_reason:
        lines.append(f"⚠️ 未拼接：{report.skipped_concat_reason}")
    lines.append("")
    lines.append("## 各 shot 状态")
    lines.append("")

    for r in report.individual:
        if r.success:
            lines.append(f"### Shot {r.shot.index} ✅")
            lines.append(f"- 时长：{r.shot.duration}s")
            lines.append(f"- 文件：`{r.video_path}`")
            lines.append(f"- task_id：`{r.task_id}`")
        else:
            lines.append(f"### Shot {r.shot.index} ❌")
            lines.append(f"- 时长：{r.shot.duration}s")
            lines.append(f"- 错误：{r.error}")
            lines.append("- 重跑此 shot 的 prompt：")
            lines.append("  ```")
            for line in r.shot.prompt_text.splitlines():
                lines.append(f"  {line}")
            lines.append("  ```")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ─── async 模式（仅 submit，不 poll） ───

def submit_all(
    seedance_md: str,
    *,
    model: str | None = None,
    ratio: str = DEFAULT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    api_key: str | None = None,
) -> list[tuple[Shot, str | None, str]]:
    """异步模式：仅提交全部 shot 任务，立刻返回 task_id 列表。

    Returns:
        list of (shot, task_id_or_None, error_msg)
    """
    shots = parse_shots(seedance_md)
    out: list[tuple[Shot, str | None, str]] = []
    for shot in shots:
        try:
            tid = submit_task(
                shot.prompt_text,
                model=model, duration=shot.duration,
                ratio=ratio, resolution=resolution, api_key=api_key,
            )
            out.append((shot, tid, ""))
        except SeedanceError as e:
            out.append((shot, None, str(e)))
    return out
