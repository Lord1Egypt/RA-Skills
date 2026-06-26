import asyncio
import re
import subprocess
from pathlib import Path

import edge_tts

from services.tts_base import TTSProvider


class EdgeTTSProvider(TTSProvider):
    def __init__(self, voice: str = "zh-CN-XiaoxiaoNeural", rate: str = "+0%") -> None:
        self.voice = voice
        self.rate = rate

    def synthesize(self, text: str, output_path: Path) -> tuple[str, float]:
        output_path = output_path.with_suffix(".mp3")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        normalized_text = text.strip()
        if not normalized_text:
            self._export_silence(output_path)
        elif not output_path.exists():
            asyncio.run(self._save_tts(normalized_text, output_path))

        duration = self._get_media_duration(output_path)
        return str(output_path), float(duration)

    async def _save_tts(self, text: str, output_path: Path) -> None:
        communicator = edge_tts.Communicate(text=text, voice=self.voice, rate=self.rate)
        await communicator.save(str(output_path))

    @staticmethod
    def _get_media_duration(path: Path) -> float:
        try:
            ffprobe_command = [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ]
            ffprobe_result = subprocess.run(
                ffprobe_command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )
            if ffprobe_result.returncode == 0 and ffprobe_result.stdout.strip():
                return float(ffprobe_result.stdout.strip())
        except FileNotFoundError:
            pass

        ffmpeg_command = ["ffmpeg", "-i", str(path)]
        ffmpeg_result = subprocess.run(
            ffmpeg_command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", ffmpeg_result.stderr or "")
        if duration_match:
            hours = int(duration_match.group(1))
            minutes = int(duration_match.group(2))
            seconds = float(duration_match.group(3))
            return hours * 3600 + minutes * 60 + seconds

        raise RuntimeError(f"Unable to determine media duration for {path}")

    @staticmethod
    def _export_silence(output_path: Path) -> None:
        command = [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=16000:cl=mono",
            "-t",
            "0.2",
            str(output_path),
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "ffmpeg failed to create silent TTS clip")
