import base64
import os
import re
import subprocess
import time
import uuid
import wave
from pathlib import Path

import requests

from services.tts_base import TTSProvider


class VolcengineTTSProvider(TTSProvider):
    V1_URL = "https://openspeech.bytedance.com/api/v1/tts"
    SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/tts/submit"
    QUERY_URL = "https://openspeech.bytedance.com/api/v3/tts/query"

    def __init__(
        self,
        app_id: str | None = None,
        access_token: str | None = None,
        cluster: str | None = None,
        voice_type: str | None = None,
    ) -> None:
        self.app_id = app_id or os.getenv("VOLCENGINE_APP_ID")
        self.access_token = access_token or os.getenv("VOLCENGINE_ACCESS_TOKEN")
        self.cluster = cluster or os.getenv("VOLCENGINE_TTS_CLUSTER", "seed-tts-2.0")
        self.voice_type = voice_type or os.getenv("VOLCENGINE_TTS_VOICE", "zh_male_m191_uranus_bigtts")

        if not self.app_id or not self.access_token:
            raise ValueError("VOLCENGINE_APP_ID or VOLCENGINE_ACCESS_TOKEN is not set.")

    def synthesize(self, text: str, output_path: Path, context_text: str = "") -> tuple[str, float]:
        output_path = output_path.with_suffix(".mp3")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        normalized_text = text.strip()
        if not normalized_text:
            raise ValueError("TTS text is empty.")

        if not output_path.exists():
            last_error: Exception | None = None
            for attempt in range(3):
                try:
                    if self._should_use_v1():
                        self._request_tts_v1(normalized_text, output_path)
                    else:
                        self._request_tts_v3(normalized_text, output_path)
                    last_error = None
                    break
                except Exception as exc:
                    last_error = exc
                    output_path.unlink(missing_ok=True)
                    time.sleep(2 * (attempt + 1))
            if last_error is not None:
                raise RuntimeError(f"Volcengine TTS failed after retries: {last_error}")

        duration = self._get_media_duration(output_path)
        return str(output_path), float(duration)

    def _should_use_v1(self) -> bool:
        return self.voice_type.endswith("_moon_bigtts")


    def _request_tts_v1(self, text: str, output_path: Path) -> None:
        headers = {
            "Authorization": f"Bearer;{self.access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "app": {
                "appid": self.app_id,
                "token": "access_token",
                "cluster": "volcano_tts",
            },
            "user": {
                "uid": "video_pipeline",
            },
            "audio": {
                "voice_type": self.voice_type,
                "encoding": "mp3",
                "speed_ratio": 1.0,
                "rate": 24000,
                "bitrate": 64,
            },
            "request": {
                "reqid": str(uuid.uuid4()),
                "text": text,
                "operation": "query",
            },
        }

        response = requests.post(self.V1_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("code") != 3000:
            raise ValueError(f"Volcengine TTS v1 failed: {response_data}")

        audio_base64 = response_data.get("data")
        if not isinstance(audio_base64, str) or not audio_base64.strip():
            raise ValueError(f"Volcengine TTS v1 missing audio data: {response_data}")

        output_path.write_bytes(base64.b64decode(audio_base64))


    def _request_tts_v3(self, text: str, output_path: Path) -> None:
        headers = {
            "X-Api-App-Id": self.app_id,
            "X-Api-Access-Key": self.access_token,
            "X-Api-Resource-Id": self.cluster,
            "X-Api-Request-Id": str(uuid.uuid4()),
            "Content-Type": "application/json",
        }
        payload = {
            "user": {
                "uid": "video_pipeline",
            },
            "req_params": {
                "text": text,
                "speaker": self.voice_type,
                "audio_params": {
                    "format": "mp3",
                    "sample_rate": 24000,
                    "bit_rate": 64000,
                },
            },
        }

        submit_data = None
        last_error: Exception | None = None
        for _ in range(3):
            try:
                response = requests.post(self.SUBMIT_URL, headers=headers, json=payload, timeout=120)
                response.raise_for_status()
                submit_data = response.json()
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                time.sleep(2)
        if submit_data is None:
            raise RuntimeError(f"Volcengine TTS submit failed after retries: {last_error}")

        if submit_data.get("code") != 20000000:
            raise ValueError(f"Volcengine TTS submit failed: {submit_data}")

        task_id = submit_data.get("data", {}).get("task_id")
        if not task_id:
            raise ValueError(f"Volcengine TTS missing task_id: {submit_data}")

        query_payload = {"task_id": task_id}
        for _ in range(300):
            try:
                query_response = requests.post(self.QUERY_URL, headers=headers, json=query_payload, timeout=120)
                query_response.raise_for_status()
                query_data = query_response.json()
            except Exception:
                time.sleep(2)
                continue
            if query_data.get("code") != 20000000:
                raise ValueError(f"Volcengine TTS query failed: {query_data}")

            task_status = query_data.get("data", {}).get("task_status")
            if task_status == 2:
                audio_url = query_data.get("data", {}).get("audio_url")
                if not audio_url:
                    raise ValueError(f"Volcengine TTS query missing audio_url: {query_data}")
                audio_response = requests.get(audio_url, timeout=120)
                audio_response.raise_for_status()
                output_path.write_bytes(audio_response.content)
                return
            if task_status == 3:
                raise ValueError(f"Volcengine TTS task failed: {query_data}")
            time.sleep(2)

        raise TimeoutError("Volcengine TTS query timed out.")


    @staticmethod
    def _get_media_duration(path: Path) -> float:
        if path.suffix.lower() == ".wav":
            with wave.open(str(path), "rb") as wav_file:
                frames = wav_file.getnframes()
                frame_rate = wav_file.getframerate()
                if frame_rate > 0:
                    return frames / float(frame_rate)

        result = subprocess.run(["ffmpeg", "-i", str(path)], capture_output=True, text=True)
        duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", result.stderr)
        if duration_match:
            hours = int(duration_match.group(1))
            minutes = int(duration_match.group(2))
            seconds = float(duration_match.group(3))
            return hours * 3600 + minutes * 60 + seconds

        raise RuntimeError(f"Unable to determine media duration for {path}")
