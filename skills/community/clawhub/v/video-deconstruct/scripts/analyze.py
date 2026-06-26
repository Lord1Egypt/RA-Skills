"""video-deconstruct 主入口（v2.0 叙事式拆解）。

用法:
    python scripts/analyze.py /path/to/video.mp4
    python scripts/analyze.py video.mp4 --with-asr             # 同时跑 stepaudio-2.5-asr
    python scripts/analyze.py video.mp4 --output-dir ./reports
    python scripts/analyze.py video.mp4 --comments-file comments.txt   # v2 占位
    python scripts/analyze.py video.mp4 --keep-upload                  # 保留云端文件
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import compress  # noqa: E402
import render_report  # noqa: E402
import stepfun_client  # noqa: E402

DIRECT_UPLOAD_MAX_BYTES = 128 * 1024 * 1024  # StepFun files API hard limit used by this skill
COMPRESS_TARGET_MB = 10  # Optional quality-preserving fallback when source exceeds direct upload limit
MAX_RETRIES = 2  # 一致性自检失败后最多重试次数（0 = 关闭重试）


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_failures(analysis: dict) -> list[tuple[str, dict]]:
    qc = analysis.get("一致性自检") or {}
    return [
        (name, data)
        for name, data in qc.items()
        if isinstance(data, dict) and data.get("通过") is False
    ]


def _build_correction_prompt(failures: list[tuple[str, dict]], prior: dict) -> str:
    """
    把上一次失败的一致性自检喂回 rubric，让模型二次生成。

    v2.0 的自检规则比 v1 多：除了"总时长一致"，还有"事件推进齐全"
    "内容描述充分""落幕文案与启示对齐"。
    """
    duration = prior.get("节奏", {}).get("总时长秒", 0) or 0
    mm, ss = int(duration // 60), int(duration % 60)
    lines = [
        "",
        "==================================================",
        "⚠️ 重试：上一次输出的一致性自检未通过，请修正后重新生成完整 JSON。",
        "==================================================",
        f"视频实际总时长 = {duration:.1f}s（即 {mm:02d}:{ss:02d}）。",
        f"所有段落 start/end 必须落在 [00:00, {mm:02d}:{ss:02d}] 内。",
        "",
        "上次失败的规则：",
    ]
    for name, data in failures:
        lines.append(f"  - {name}：{data.get('规则', '')}")
        for k, v in data.items():
            if k in ("规则", "通过"):
                continue
            lines.append(f"      · {k} = {v}")
    lines.append("")
    lines.append("请重新生成整个 JSON（不是只改 一致性自检），确保所有 通过=true。")
    lines.append("特别提醒：内容描述至少 200 字、事件推进至少 3 条、落幕文案与受众启示要对齐。")
    return "\n".join(lines)


def _validate(video_path: Path) -> None:
    if not video_path.exists():
        raise SystemExit(f"❌ 文件不存在: {video_path}")
    if video_path.suffix.lower() != ".mp4":
        raise SystemExit(
            f"❌ 只支持 mp4，当前是 {video_path.suffix}。\n"
            f"   先转一下: ffmpeg -i {video_path.name} {video_path.stem}.mp4"
        )


def run(
    video_path: Path,
    output_dir: Path,
    comments_file: Path | None,
    keep_upload: bool,
    with_asr: bool,
) -> Path:
    _validate(video_path)

    if comments_file is not None:
        print(f"⚠️  --comments-file 在 v1 暂未启用（已忽略 {comments_file}），v2 会接入评论分析。")

    # —— ASR 阶段（可选）——
    asr_transcript: str | None = None
    if with_asr:
        try:
            import asr_client  # noqa: WPS433
            print(f"🎤 抽音轨 + 跑 stepaudio-2.5-asr ...")
            asr_transcript = asr_client.transcribe_video(video_path)
            preview = (asr_transcript[:120] + "…") if len(asr_transcript) > 120 else asr_transcript
            print(f"   ✅ ASR 转录 {len(asr_transcript)} 字：{preview!r}")
        except Exception as e:
            print(f"   ⚠️ ASR 失败（继续走 vision-only 模式）：{e}")
            asr_transcript = None

    # —— 直传优先：只有超过 StepFun 文件 API 上限时才压缩 ——
    upload_path = video_path
    compressed_tmp: Path | None = None
    size_mb = video_path.stat().st_size / 1024 / 1024
    if video_path.stat().st_size > DIRECT_UPLOAD_MAX_BYTES:
        print(f"🗜  输入 {size_mb:.1f}MB > 128MB（StepFun 文件 API 上限），自动压缩中...")
        compressed_tmp = compress.compress_to_target(video_path, target_mb=COMPRESS_TARGET_MB)
        upload_path = compressed_tmp
        size_mb = compressed_tmp.stat().st_size / 1024 / 1024
        print(f"   ✅ 压缩后 {size_mb:.2f}MB")
    else:
        print(f"📦 输入 {size_mb:.1f}MB <= 128MB，跳过压缩，直接上传")

    print(f"📤 上传视频到 StepFun: {upload_path.name} ({size_mb:.1f}MB)")
    file_id = stepfun_client.upload_video(upload_path)
    print(f"   file_id = {file_id}")

    try:
        print(f"🤖 调 step-1o-turbo-vision 拆解中{' (附 ASR 对白)' if asr_transcript else ''}...")
        system_prompt = _load_text(SKILL_ROOT / "prompts" / "system.txt")
        base_rubric = _load_text(SKILL_ROOT / "prompts" / "analysis_rubric.txt")

        rubric_prompt = base_rubric
        analysis: dict = {}
        for attempt in range(MAX_RETRIES + 1):
            analysis = stepfun_client.analyze_video(
                file_id=file_id,
                system_prompt=system_prompt,
                rubric_prompt=rubric_prompt,
                asr_transcript=asr_transcript,
            )
            failures = _extract_failures(analysis)
            if not failures:
                if attempt > 0:
                    print(f"   ✅ 第 {attempt + 1} 次尝试通过一致性自检")
                break
            if attempt < MAX_RETRIES:
                names = ", ".join(n for n, _ in failures)
                print(f"   ⚠️ 第 {attempt + 1} 次尝试 {len(failures)} 条自检失败（{names}），重试中...")
                rubric_prompt = base_rubric + _build_correction_prompt(failures, analysis)
            else:
                print(f"   ⚠️ 重试 {MAX_RETRIES} 次后仍有 {len(failures)} 条失败；报告会带告警发出")

        print("📝 渲染报告...")
        report_md = render_report.render(
            analysis=analysis,
            video_name=video_path.name,
        )

        output_dir.mkdir(parents=True, exist_ok=True)
        report_path = output_dir / f"{video_path.stem}-report.md"
        report_path.write_text(report_md, encoding="utf-8")
        json_path = output_dir / f"{video_path.stem}-analysis.json"
        json_path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
        if asr_transcript:
            asr_path = output_dir / f"{video_path.stem}-transcript.txt"
            asr_path.write_text(asr_transcript, encoding="utf-8")
            print(f"📜 ASR 转录: {asr_path}")
        print(f"✅ 报告: {report_path}")
        print(f"🔍 原始 JSON: {json_path}")
        return report_path

    finally:
        if keep_upload:
            print(f"📎 保留云端文件: {file_id}（--keep-upload）")
        else:
            stepfun_client.delete_file(file_id)
            print(f"🧹 已清理云端文件: {file_id}")
        if compressed_tmp is not None:
            compressed_tmp.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="短视频爆款拆解 v2.0 (step-1o-turbo-vision + stepaudio-2.5-asr · StepClaw)"
    )
    ap.add_argument("video", type=Path, help="本地 mp4 文件路径")
    ap.add_argument("--output-dir", type=Path, default=SKILL_ROOT / "output", help="报告输出目录")
    ap.add_argument("--with-asr", action="store_true", help="启用 stepaudio-2.5-asr 抽对白文本作为辅助上下文（强烈推荐）")
    ap.add_argument("--comments-file", type=Path, default=None, help="(v2 占位) 评论 txt 文件")
    ap.add_argument("--keep-upload", action="store_true", help="分析完后保留云端文件，默认自动删除")
    args = ap.parse_args()
    run(
        video_path=args.video.resolve(),
        output_dir=args.output_dir.resolve(),
        comments_file=args.comments_file,
        keep_upload=args.keep_upload,
        with_asr=args.with_asr,
    )


if __name__ == "__main__":
    main()
