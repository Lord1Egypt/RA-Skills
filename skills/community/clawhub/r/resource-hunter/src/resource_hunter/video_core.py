from __future__ import annotations

import glob
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from .cache import ResourceCache
from .common import default_download_dir, detect_platform, safe_filename, storage_root
from .errors import BinaryMissingError, UpstreamError
from .models import VideoResult


class VideoManager:
    def __init__(self, cache: ResourceCache | None = None) -> None:
        self.cache = cache or ResourceCache()
        self.download_dir = default_download_dir()
        self.subtitle_dir = storage_root() / "subtitles"
        self.subtitle_dir.mkdir(parents=True, exist_ok=True)

    def _binary_status(self) -> dict[str, Any]:
        return {
            "yt_dlp": shutil.which("yt-dlp"),
            "ffmpeg": shutil.which("ffmpeg"),
        }

    def _run_ytdlp(self, args: list[str], capture: bool = True, timeout: int = 300) -> subprocess.CompletedProcess[str]:
        binary = shutil.which("yt-dlp")
        if not binary:
            raise BinaryMissingError("yt-dlp not found")
        return subprocess.run(
            [binary] + args,
            capture_output=capture,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )

    def _load_info_json(self, url: str) -> dict[str, Any]:
        result = self._run_ytdlp(["-J", "--no-playlist", url], capture=True, timeout=120)
        if result.returncode != 0:
            raise UpstreamError((result.stderr or result.stdout or "yt-dlp failed").strip()[:200])
        return json.loads(result.stdout)

    def _format_entries(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        formats: list[dict[str, Any]] = []
        seen: set[tuple[str, int | None]] = set()
        for item in data.get("formats", []):
            height = item.get("height")
            format_id = item.get("format_id")
            if not format_id:
                continue
            key = (format_id, height)
            if key in seen:
                continue
            seen.add(key)
            filesize = item.get("filesize") or item.get("filesize_approx") or 0
            formats.append(
                {
                    "id": format_id,
                    "ext": item.get("ext"),
                    "height": height,
                    "width": item.get("width"),
                    "has_audio": item.get("acodec") not in (None, "none"),
                    "has_video": item.get("vcodec") not in (None, "none"),
                    "filesize_mb": round(filesize / 1024 / 1024, 2) if filesize else None,
                    "note": item.get("format_note") or item.get("format"),
                }
            )
        formats.sort(key=lambda item: ((item.get("height") or 0), item.get("has_audio"), item["id"]), reverse=True)
        return formats

    def _recommended(self, formats: list[dict[str, Any]]) -> list[dict[str, Any]]:
        best = next((item for item in formats if item.get("has_video")), None)
        balanced = next((item for item in formats if (item.get("height") or 0) <= 1080 and item.get("has_video")), best)
        small = next((item for item in formats if (item.get("height") or 0) <= 720 and item.get("has_video")), balanced)
        return [
            {"preset": "best", "format": best["id"] if best else "best"},
            {"preset": "balanced", "format": balanced["id"] if balanced else "best"},
            {"preset": "small", "format": small["id"] if small else "best"},
            {"preset": "audio", "format": "bestaudio/best"},
        ]

    def info(self, url: str) -> VideoResult:
        data = self._load_info_json(url)
        formats = self._format_entries(data)
        return VideoResult(
            url=url,
            platform=detect_platform(url),
            title=data.get("title", ""),
            duration=data.get("duration"),
            formats=formats,
            recommended=self._recommended(formats),
            meta={
                "uploader": data.get("uploader"),
                "yt_dlp": self._binary_status()["yt_dlp"],
                "ffmpeg": self._binary_status()["ffmpeg"],
            },
        )

    def probe(self, url: str) -> VideoResult:
        info = self.info(url)
        info.formats = info.formats[:6]
        info.meta["probe"] = True
        return info

    def _preset_expression(self, preset: str) -> tuple[str, bool]:
        if preset == "best":
            return "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best", False
        if preset == "balanced":
            return "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best", False
        if preset == "small":
            return "best[height<=720]/best", False
        if preset == "audio":
            return "bestaudio/best", True
        return preset, False

    def download(self, url: str, preset: str = "best", output_dir: str | None = None) -> VideoResult:
        target_dir = Path(output_dir) if output_dir else self.download_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        format_expr, audio_only = self._preset_expression(preset)
        args = [
            "--no-playlist",
            "--no-warnings",
            "-o",
            str(target_dir / "%(title)s.%(ext)s"),
            "-f",
            format_expr,
        ]
        if audio_only:
            args.extend(["-x", "--audio-format", "mp3"])
        elif self._binary_status()["ffmpeg"]:
            args.extend(["--merge-output-format", "mp4"])
        args.append(url)
        result = self._run_ytdlp(args, capture=True, timeout=600)
        if result.returncode != 0:
            raise UpstreamError((result.stderr or result.stdout or "download failed").strip()[:200])
        newest = sorted(target_dir.glob("*"), key=lambda path: path.stat().st_mtime, reverse=True)
        artifacts: list[dict[str, Any]] = []
        if newest:
            file_path = newest[0]
            artifacts.append(
                {
                    "path": str(file_path),
                    "size_bytes": file_path.stat().st_size,
                    "preset": preset,
                    "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                }
            )
        payload = {
            "url": url,
            "preset": preset,
            "artifacts": artifacts,
            "meta": self._binary_status(),
        }
        self.cache.record_video_manifest(url, payload)
        return VideoResult(
            url=url,
            platform=detect_platform(url),
            title=Path(artifacts[0]["path"]).name if artifacts else "",
            artifacts=artifacts,
            meta=payload["meta"],
        )

    def subtitle(self, url: str, lang: str = "zh-Hans,zh,en") -> VideoResult:
        prefix = safe_filename(str(int(time.time())))
        template = str(self.subtitle_dir / f"{prefix}_%(title)s")
        before = set(glob.glob(str(self.subtitle_dir / "*.vtt")))
        result = self._run_ytdlp(
            [
                "--skip-download",
                "--write-auto-sub",
                "--write-sub",
                "--sub-lang",
                lang,
                "--sub-format",
                "vtt",
                "-o",
                template,
                url,
            ],
            capture=True,
            timeout=300,
        )
        if result.returncode != 0:
            raise UpstreamError((result.stderr or result.stdout or "subtitle failed").strip()[:200])
        after = set(glob.glob(str(self.subtitle_dir / "*.vtt")))
        subtitle_files = sorted(after - before) or sorted(glob.glob(str(self.subtitle_dir / f"{prefix}_*.vtt")))
        cleaned_text = ""
        artifacts: list[dict[str, Any]] = []
        for subtitle_file in subtitle_files:
            path = Path(subtitle_file)
            text = path.read_text(encoding="utf-8", errors="replace")
            lines = []
            for line in text.splitlines():
                stripped = line.strip()
                if not stripped or stripped == "WEBVTT" or "-->" in stripped or stripped.isdigit():
                    continue
                lines.append(stripped)
            cleaned_text = "\n".join(lines)
            artifacts.append({"path": str(path), "size_bytes": path.stat().st_size})
        return VideoResult(
            url=url,
            platform=detect_platform(url),
            artifacts=artifacts,
            meta={"lang": lang, "text": cleaned_text[:5000], **self._binary_status()},
        )

    def doctor(self) -> dict[str, Any]:
        return {
            "binaries": self._binary_status(),
            "download_dir": str(self.download_dir),
            "subtitle_dir": str(self.subtitle_dir),
            "recent_manifests": self.cache.list_video_manifests(limit=5),
        }


def format_video_text(result: VideoResult, mode: str) -> str:
    lines = [f"Video {mode}", f"URL: {result.url}", f"Platform: {result.platform}"]
    if result.title:
        lines.append(f"Title: {result.title}")
    if result.duration:
        minutes, seconds = divmod(int(result.duration), 60)
        lines.append(f"Duration: {minutes}:{seconds:02d}")
    if result.formats:
        lines.append("")
        lines.append("Formats:")
        for entry in result.formats[:10]:
            bits = [entry["id"]]
            if entry.get("height"):
                bits.append(f"{entry['height']}p")
            if entry.get("ext"):
                bits.append(entry["ext"])
            if entry.get("filesize_mb"):
                bits.append(f"{entry['filesize_mb']}MB")
            lines.append("- " + " | ".join(bits))
    if result.recommended:
        lines.append("")
        lines.append("Recommended:")
        for item in result.recommended:
            lines.append(f"- {item['preset']}: {item['format']}")
    if result.artifacts:
        lines.append("")
        lines.append("Artifacts:")
        for artifact in result.artifacts:
            lines.append(f"- {artifact['path']}")
    if result.meta:
        text = result.meta.get("text")
        if text:
            lines.append("")
            lines.append("Subtitle preview:")
            lines.append(text[:1000])
    return "\n".join(lines)
