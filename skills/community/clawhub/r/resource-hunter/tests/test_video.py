from __future__ import annotations

import subprocess

from resource_hunter.cache import ResourceCache
from resource_hunter.video_core import VideoManager


def test_video_info_reports_missing_binary(monkeypatch, tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    manager = VideoManager(cache)
    monkeypatch.setattr("resource_hunter.video_core.shutil.which", lambda name: None)
    try:
        manager.info("https://youtu.be/demo")
    except RuntimeError as exc:
        assert "yt-dlp not found" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected RuntimeError")


def test_video_download_records_manifest(monkeypatch, tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    manager = VideoManager(cache)
    target_dir = tmp_path / "downloads"

    def fake_run(args, capture=True, timeout=300):
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "demo.mp4").write_bytes(b"video")
        return subprocess.CompletedProcess(args=["yt-dlp"], returncode=0, stdout="", stderr="")

    monkeypatch.setattr(manager, "_run_ytdlp", fake_run)
    monkeypatch.setattr(manager, "_binary_status", lambda: {"yt_dlp": "/bin/yt-dlp", "ffmpeg": None})
    result = manager.download("https://youtu.be/demo", preset="small", output_dir=str(target_dir))
    assert result.artifacts
    manifests = cache.list_video_manifests(limit=1)
    assert manifests[0]["preset"] == "small"


def test_video_subtitle_cleans_vtt(monkeypatch, tmp_path):
    cache = ResourceCache(tmp_path / "cache.db")
    manager = VideoManager(cache)
    manager.subtitle_dir = tmp_path / "subs"
    manager.subtitle_dir.mkdir()

    def fake_run(args, capture=True, timeout=300):
        subtitle = manager.subtitle_dir / "123_demo.vtt"
        subtitle.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nhello\n\n00:00:02.000 --> 00:00:04.000\nworld\n", encoding="utf-8")
        return subprocess.CompletedProcess(args=["yt-dlp"], returncode=0, stdout="", stderr="")

    monkeypatch.setattr(manager, "_run_ytdlp", fake_run)
    monkeypatch.setattr(manager, "_binary_status", lambda: {"yt_dlp": "/bin/yt-dlp", "ffmpeg": None})
    result = manager.subtitle("https://youtu.be/demo")
    assert "hello" in result.meta["text"]
    assert "00:00:00.000" not in result.meta["text"]
