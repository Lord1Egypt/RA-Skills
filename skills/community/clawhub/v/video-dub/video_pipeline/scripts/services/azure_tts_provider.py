import html
import os
import re
import subprocess
import wave
from pathlib import Path

import requests

from services.tts_base import TTSProvider


class AzureTTSProvider(TTSProvider):
    def __init__(
        self,
        key: str | None = None,
        region: str | None = None,
        voice: str | None = None,
        output_format: str | None = None,
    ) -> None:
        self.key = key or os.getenv("AZURE_TTS_KEY")
        self.region = region or os.getenv("AZURE_TTS_REGION")
        self.voice = voice or os.getenv("AZURE_TTS_VOICE", "zh-CN-YunxiNeural")
        self.output_format = output_format or os.getenv(
            "AZURE_TTS_OUTPUT_FORMAT",
            "audio-24khz-48kbitrate-mono-mp3",
        )

        if not self.key or not self.region:
            raise ValueError("AZURE_TTS_KEY or AZURE_TTS_REGION is not set.")

    def synthesize(self, text: str, output_path: Path, context_text: str = "") -> tuple[str, float]:
        output_path = output_path.with_suffix(".mp3")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        normalized_text = text.strip()
        if not normalized_text:
            raise ValueError("TTS text is empty.")

        if not output_path.exists():
            self._request_tts(normalized_text, output_path)

        duration = self._get_media_duration(output_path)
        return str(output_path), float(duration)

    def _request_tts(self, text: str, output_path: Path) -> None:
        endpoint = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": self.output_format,
            "User-Agent": "video_pipeline",
        }
        ssml = self._build_ssml(text)

        response = requests.post(endpoint, headers=headers, data=ssml.encode("utf-8"), timeout=120)
        response.raise_for_status()
        output_path.write_bytes(response.content)

    def _build_ssml(self, text: str) -> str:
        escaped_text = html.escape(text, quote=False)
        escaped_voice = html.escape(self.voice, quote=True)
        return (
            '<speak version="1.0" xml:lang="zh-CN">'
            f'<voice name="{escaped_voice}">{escaped_text}</voice>'
            "</speak>"
        )

    @staticmethod
    def _get_media_duration(path: Path) -> float:
        if path.suffix.lower() == ".wav":
            with wave.open(str(path), "rb") as wav_file:
                frames = wav_file.getnframes()
                frame_rate = wav_file.getframerate()
                if frame_rate > 0:
                    return frames / float(frame_rate)

        try:
            ffprobe_result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    str(path),
                ],
                capture_output=True,
                text=True,
            )
            if ffprobe_result.returncode == 0 and ffprobe_result.stdout.strip():
                return float(ffprobe_result.stdout.strip())
        except FileNotFoundError:
            pass

        ffmpeg_result = subprocess.run(["ffmpeg", "-i", str(path)], capture_output=True, text=True)
        duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", ffmpeg_result.stderr)
        if duration_match:
            hours = int(duration_match.group(1))
            minutes = int(duration_match.group(2))
            seconds = float(duration_match.group(3))
            return hours * 3600 + minutes * 60 + seconds

        raise RuntimeError(f"Unable to determine media duration for {path}")
