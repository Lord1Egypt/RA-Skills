"""Unified API clients for image, video, and TTS generation."""

import base64
import io
import json
import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import requests
from PIL import Image


class APIError(Exception):
    """Raised when API request fails."""
    pass


class BaseAPIClient(ABC):
    """Base class for all API clients with retry logic."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        logger: Optional[logging.Logger] = None,
        max_retries: int = 3,
        timeout: int = 120,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.model = model
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        stream: bool = False,
    ) -> dict:
        """Make HTTP request with retry logic.

        Args:
            method: HTTP method.
            endpoint: API endpoint (relative to base_url).
            data: Request body.
            stream: Whether to stream response.

        Returns:
            Parsed JSON response.

        Raises:
            APIError: If all retries fail.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    timeout=self.timeout,
                    stream=stream,
                )

                if response.status_code == 429:
                    wait_time = 2 ** attempt
                    self.logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                if response.status_code == 200:
                    if stream:
                        return {"stream": response}
                    return response.json()

                # Handle errors
                error_text = response.text[:500]
                self.logger.error(f"HTTP {response.status_code}: {error_text}")

                if attempt < self.max_retries:
                    time.sleep(self.max_retries)
                    continue

                raise APIError(f"API request failed: HTTP {response.status_code} - {error_text}")

            except requests.exceptions.Timeout:
                self.logger.warning(f"Request timeout (attempt {attempt}/{self.max_retries})")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                raise APIError("Request timeout after all retries")

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request error: {e}")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                raise APIError(f"Request failed: {e}")

        raise APIError("Max retries exceeded")


class ImageAPIClient(BaseAPIClient):
    """Client for image generation APIs."""

    def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        reference_images: Optional[list[str]] = None,
        seed: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ) -> bytes:
        """Generate an image from prompt.

        Args:
            prompt: Image generation prompt.
            size: Image size (e.g., "1024x1024", "4096x2304").
            reference_images: List of base64 data URLs for reference.
            seed: Random seed for reproducibility.
            system_prompt: Optional system prompt.

        Returns:
            Image bytes.

        Raises:
            APIError: If generation fails.
        """
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "size": size,
            "n": 1,
            "response_format": "url",
        }

        if seed is not None:
            payload["seed"] = seed

        if reference_images:
            payload["image"] = reference_images

        result = self._request("POST", "images/generations", data=payload)

        # Unified response parsing: try url, b64_json, b64_image
        image_data = None
        if "data" in result and len(result["data"]) > 0:
            item = result["data"][0]
            image_data = item.get("url") or item.get("b64_json") or item.get("b64_image")

        if not image_data:
            raise APIError(f"No image data in response: {result}")

        if isinstance(image_data, str) and image_data.startswith("http"):
            img_response = self.session.get(image_data, timeout=self.timeout)
            img_response.raise_for_status()
            return img_response.content

        # Base64 encoded
        if isinstance(image_data, str) and image_data.startswith("data:"):
            b64_data = image_data.split(",", 1)[1]
        else:
            b64_data = image_data

        return base64.b64decode(b64_data)

    @staticmethod
    def load_image_as_base64(image_path: Path, max_size: int = 512) -> str:
        """Load image and return as data URL.

        Args:
            image_path: Path to image file.
            max_size: Max dimension for resize.

        Returns:
            Data URL string.
        """
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=85, optimize=True)
            b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{b64}"


class VideoAPIClient(BaseAPIClient):
    """Client for video generation APIs supporting Kling and Volcengine Ark."""

    def __init__(self, *args, provider: str = "kling", **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = provider.lower()
        self._is_volcengine = self.provider == "volcengine" or "volces" in self.base_url

    def submit(
        self,
        prompt: str,
        mode: str = "singleImage",
        image_url: Optional[str] = None,
        start_image_url: Optional[str] = None,
        end_image_url: Optional[str] = None,
        duration: int = 5,
        resolution: str = "720p",
        aspect_ratio: str = "16:9",
        camera_fixed: bool = False,
    ) -> str:
        """Submit a video generation task."""
        if self._is_volcengine:
            return self._submit_volcengine(
                prompt=prompt,
                image_url=image_url,
                start_image_url=start_image_url,
                end_image_url=end_image_url,
                duration=duration,
                aspect_ratio=aspect_ratio,
            )
        return self._submit_kling(
            prompt=prompt,
            mode=mode,
            image_url=image_url,
            start_image_url=start_image_url,
            end_image_url=end_image_url,
            duration=duration,
            resolution=resolution,
            aspect_ratio=aspect_ratio,
            camera_fixed=camera_fixed,
        )

    def _submit_volcengine(
        self,
        prompt: str,
        image_url: Optional[str] = None,
        start_image_url: Optional[str] = None,
        end_image_url: Optional[str] = None,
        duration: int = 5,
        aspect_ratio: str = "16:9",
    ) -> str:
        """Submit video task to Volcengine Ark API."""
        content = [{"type": "text", "text": prompt}]

        for url in (image_url, start_image_url, end_image_url):
            if url:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": url},
                    "role": "reference_image",
                })

        payload = {
            "model": self.model,
            "content": content,
            "ratio": aspect_ratio,
            "duration": duration,
            "watermark": False,
        }

        result = self._request("POST", "contents/generations/tasks", data=payload)
        return result.get("id") or result.get("task_id", "")

    def _submit_kling(
        self,
        prompt: str,
        mode: str = "singleImage",
        image_url: Optional[str] = None,
        start_image_url: Optional[str] = None,
        end_image_url: Optional[str] = None,
        duration: int = 5,
        resolution: str = "720p",
        aspect_ratio: str = "16:9",
        camera_fixed: bool = False,
    ) -> str:
        """Submit video task to Kling API."""
        content = [{"type": "text", "text": prompt}]

        if mode in ("singleImage", "text") and image_url:
            content.append({"type": "image_url", "image_url": {"url": image_url}})

        if mode == "startEnd" and start_image_url:
            content.append({"type": "image_url", "image_url": {"url": start_image_url}})
            if end_image_url:
                content.append({"type": "image_url", "image_url": {"url": end_image_url}})

        payload = {
            "model": self.model,
            "content": content,
            "duration": duration,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "camera_fixed": camera_fixed,
        }

        result = self._request("POST", "videos/generations", data=payload)
        return result.get("id") or result.get("task_id", "")

    def query_status(self, task_id: str) -> dict:
        """Query video generation task status."""
        if self._is_volcengine:
            return self._query_status_volcengine(task_id)
        return self._query_status_kling(task_id)

    def _query_status_volcengine(self, task_id: str) -> dict:
        """Query task status from Volcengine Ark API."""
        result = self._request("GET", f"contents/generations/tasks/{task_id}")

        api_status = result.get("status", "").lower()
        status_map = {
            "queued": "pending",
            "running": "processing",
            "succeeded": "succeeded",
            "failed": "failed",
            "error": "failed",
        }

        status = status_map.get(api_status, "pending")
        video_url = None

        if status == "succeeded":
            video_url = (
                result.get("content", {}).get("video_url")
                or result.get("video_url")
                or result.get("url")
            )
            if not video_url and "content" in result:
                content_list = result.get("content", [])
                if isinstance(content_list, list):
                    for item in content_list:
                        if isinstance(item, dict) and item.get("type") == "video_url":
                            video_url = item.get("video_url", {}).get("url")
                            break

        return {
            "status": status,
            "video_url": video_url,
            "error": result.get("error") or result.get("message") if status == "failed" else None,
        }

    def _query_status_kling(self, task_id: str) -> dict:
        """Query task status from Kling API."""
        result = self._request("GET", f"videos/generations/{task_id}")

        api_status = result.get("status", "").lower()
        status_map = {
            "pending": "pending",
            "queued": "pending",
            "processing": "processing",
            "running": "processing",
            "succeeded": "succeeded",
            "failed": "failed",
            "error": "failed",
        }

        status = status_map.get(api_status, "pending")
        video_url = None

        if status == "succeeded":
            video_url = (
                result.get("content", {}).get("video_url")
                or result.get("video_url")
                or result.get("url")
            )

        return {
            "status": status,
            "video_url": video_url,
            "error": result.get("error") or result.get("message") if status == "failed" else None,
        }

    def wait_for_completion(
        self,
        task_id: str,
        timeout: int = 600,
        poll_interval: int = 5,
    ) -> dict:
        """Wait for video generation to complete.

        Args:
            task_id: Task ID.
            timeout: Max wait time in seconds.
            poll_interval: Polling interval.

        Returns:
            Final status dict.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.query_status(task_id)
            if result["status"] in ("succeeded", "failed"):
                return result
            self.logger.info(f"Task {task_id} status: {result['status']}, waiting...")
            time.sleep(poll_interval)

        return {"status": "failed", "error": f"Timeout after {timeout}s"}


class TTSAPIClient(BaseAPIClient):
    """Client for TTS APIs (Volcano Engine SSE format)."""

    def synthesize(
        self,
        text: str,
        voice_type: str,
        emotion: Optional[str] = None,
        resource_id: str = "volc.seedtts.default",
    ) -> tuple[Optional[bytes], Optional[list[tuple]]]:
        """Synthesize speech from text.

        Args:
            text: Text to synthesize.
            voice_type: Voice type ID.
            emotion: Optional emotion tag.
            resource_id: TTS resource ID.

        Returns:
            Tuple of (audio_bytes, timestamps).
            timestamps is list of (start_ms, end_ms, text).
        """
        import uuid

        req_id = str(uuid.uuid4())

        payload = {
            "user": {"uid": f"uid_{req_id[:8]}"},
            "event": 200,
            "req_params": {
                "text": text,
                "speaker": voice_type,
                "audio_params": {
                    "format": "mp3",
                    "sample_rate": 24000,
                    "enable_subtitle": True,
                },
            },
        }

        if emotion:
            payload["req_params"]["emotion"] = emotion

        url = f"{self.base_url}/unidirectional/sse?api_resource_id={resource_id}&api_key={self.api_key}"

        try:
            response = self.session.post(url, json=payload, timeout=60, stream=True)
            response.raise_for_status()

            audio_chunks = []
            timestamps = []
            current_event = None

            for line in response.iter_lines():
                if not line:
                    continue

                line_text = line.decode("utf-8")

                if line_text.startswith("event:"):
                    current_event = line_text.split(":", 1)[1].strip()
                    continue

                if line_text.startswith("data:") and current_event:
                    data_text = line_text[5:].strip()
                    try:
                        data = json.loads(data_text)
                    except json.JSONDecodeError:
                        continue

                    code = data.get("code")
                    if code and code not in (0, 20000000):
                        error_msg = data.get("message", "Unknown error")
                        self.logger.error(f"TTS API error: {error_msg}")
                        return None, None

                    if current_event == "352" and data.get("data"):
                        audio_b64 = data["data"]
                        if audio_b64:
                            audio_chunks.append(base64.b64decode(audio_b64))

                    elif current_event == "351" and data.get("sentence"):
                        sentence = data["sentence"]
                        words = sentence.get("words", [])
                        for word_info in words:
                            if isinstance(word_info, dict):
                                start_ms = int(word_info.get("startTime", 0) * 1000)
                                end_ms = int(word_info.get("endTime", 0) * 1000)
                                word_text = word_info.get("word", "")
                                if word_text:
                                    timestamps.append((start_ms, end_ms, word_text))

                    elif current_event == "152":
                        break

            if audio_chunks:
                return b"".join(audio_chunks), timestamps if timestamps else None
            else:
                self.logger.error("No audio data received")
                return None, None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"TTS request failed: {e}")
            return None, None
