"""任务运行辅助：录屏信息组装与 CLI 输出（通用模板，无业务逻辑）。"""

from __future__ import annotations

from typing import Any, Dict, Optional


def build_video_info(
    video_summary: dict[str, Any],
    compose_context_before: Optional[dict[str, Any]] = None,
    compose_context_after: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """将 RpaVideoSession.summary() 转为 task log / CLI 可用的 video 块。"""
    return {
        "enabled": video_summary.get("enabled", False),
        "path": video_summary.get("path"),
        "capture_path": video_summary.get("capture_path"),
        "record_log_path": video_summary.get("record_log_path"),
        "warnings": list(video_summary.get("warnings") or []),
        "voiceover_path": video_summary.get("voiceover_path"),
        "music_path": video_summary.get("music_path"),
        "audio_warnings": list(video_summary.get("audio_warnings") or []),
        "compose_context": {
            **(compose_context_before or {}),
            "after_compose": compose_context_after or {},
        },
    }


def merge_video_into_result_summary(
    payload: dict[str, Any],
    video_info: Optional[dict[str, Any]],
) -> dict[str, Any]:
    """把 video artifact 字段写入 result_summary JSON 对象。"""
    if not video_info:
        return payload
    payload = dict(payload)
    payload["video"] = video_info
    payload["video_path"] = video_info.get("path")
    payload["raw_video"] = video_info.get("capture_path")
    payload["video_log"] = video_info.get("record_log_path")
    payload["video_warnings"] = list(video_info.get("warnings") or [])
    payload["voiceover_path"] = video_info.get("voiceover_path")
    payload["music_path"] = video_info.get("music_path")
    payload["audio_warnings"] = list(video_info.get("audio_warnings") or [])
    return payload


def _print_video_summary(video_block: Optional[dict[str, Any]]) -> None:
    """任务完成后在 CLI 打印录屏路径、日志与诊断信息。"""
    if not isinstance(video_block, dict) or not video_block.get("enabled"):
        return
    record_log = video_block.get("record_log_path")
    if record_log:
        print(f"录屏日志：{record_log}")
    path = video_block.get("path")
    if path:
        print(f"录屏路径：{path}")
    else:
        print("录屏路径：未生成")
        warnings = video_block.get("warnings") or []
        if warnings:
            print(f"视频诊断：{'; '.join(str(w) for w in warnings)}")
        capture = video_block.get("capture_path")
        if capture:
            print(f"原始录屏路径：{capture}")
    voiceover = video_block.get("voiceover_path")
    if voiceover:
        print(f"旁白路径：{voiceover}")
    music = video_block.get("music_path")
    if music:
        print(f"背景音乐：{music}")
    audio_warnings = video_block.get("audio_warnings") or []
    if audio_warnings:
        print(f"音频诊断：{'; '.join(str(w) for w in audio_warnings)}")
    compose_ctx = video_block.get("compose_context")
    if isinstance(compose_ctx, dict):
        print(
            "视频合成上下文："
            f"media_assets_root={compose_ctx.get('media_assets_root', '')}; "
            f"ffmpeg_path={compose_ctx.get('ffmpeg_path', '')}; "
            f"background_music_issue={compose_ctx.get('background_music_issue') or ''}; "
            f"background_music_sample_path={compose_ctx.get('background_music_sample_path', '')}"
        )
