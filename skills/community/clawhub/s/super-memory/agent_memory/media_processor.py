"""
media_processor.py - 多模态媒体处理器
用视觉/语音模型理解图片、音频、视频，提取文本后写入记忆

支持：
1. 图片理解 — 场景描述、OCR、图表分析、代码截图识别
2. 音频理解 — 语音转文字、说话人区分
3. 视频理解 — 关键帧提取 + 音频转写

接入方式：
    # 方式 1：OpenAI 兼容 API（覆盖 OpenAI / Azure / vLLM / LiteLLM / Ollama / 智谱 / DeepSeek / 月之暗面 等）
    processor = MediaProcessor.from_openai(api_key="YOUR_API_KEY_HERE", model="gpt-4o")  # placeholder only

    # 方式 2：Anthropic Claude
    processor = MediaProcessor.from_anthropic(api_key="YOUR_API_KEY_HERE", model="claude-3-5-sonnet")  # placeholder only

    # 方式 3：Google Gemini
    processor = MediaProcessor.from_google(api_key="YOUR_API_KEY_HERE", model="gemini-1.5-pro")  # placeholder only

    # 方式 4：Ollama 本地模型
    processor = MediaProcessor.from_ollama(model="llava:13b")

    # 方式 5：小米 MiMo Omni
    processor = MediaProcessor.from_mimo_omni(api_url="http://...", api_key="...")

    # 方式 6：自定义函数
    processor = MediaProcessor(vision_fn=my_vision_fn, audio_fn=my_audio_fn)

    # 方式 7：自动检测环境变量
    processor = MediaProcessor.auto()
"""

from __future__ import annotations

import os
import logging
import base64
import tempfile
import subprocess

from .utils import _validate_url

logger = logging.getLogger(__name__)

# 支持的格式
IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".svg"}
AUDIO_FORMATS = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma"}
VIDEO_FORMATS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv"}
ALL_FORMATS = IMAGE_FORMATS | AUDIO_FORMATS | VIDEO_FORMATS


class MediaProcessor:
    """
    统一的多模态媒体处理器。

    vision_fn 签名: fn(media_bytes: bytes, mime_type: str, prompt: str) -> str
    audio_fn 签名: fn(audio_bytes: bytes, mime_type: str) -> str
    video_fn 签名: fn(video_path: str, prompt: str) -> str
    """

    DEFAULT_IMAGE_PROMPT = (
        "请详细描述这张图片的内容。包括：\n"
        "1. 主要内容和场景\n"
        "2. 如果有文字，请全部提取\n"
        "3. 如果有图表/代码/配置，请完整描述\n"
        "4. 如果有数据/数字，请列出"
    )

    DEFAULT_AUDIO_PROMPT = "请将这段音频完整转写为文字。如果是多人对话，请区分说话人。"

    DEFAULT_VIDEO_PROMPT = (
        "请描述这个视频的内容。包括：\n"
        "1. 主要场景和事件\n"
        "2. 如果有对话，请转写关键内容\n"
        "3. 屏幕上的文字/代码/图表"
    )

    def __init__(
        self,
        vision_fn=None,
        audio_fn=None,
        video_fn=None,
    ):
        """
        参数:
            vision_fn: 图片理解函数 fn(bytes, mime, prompt) -> str
            audio_fn: 音频理解函数 fn(bytes, mime) -> str
            video_fn: 视频理解函数 fn(video_path, prompt) -> str
        """
        self.vision_fn = vision_fn
        self.audio_fn = audio_fn
        self.video_fn = video_fn

    @classmethod
    def from_openai(
        cls,
        api_key: str = None,
        model: str = "gpt-4o",
        base_url: str = None,
    ) -> "MediaProcessor":
        """
        用 OpenAI 兼容 API 创建处理器。

        支持：OpenAI、Azure OpenAI、国内各种兼容接口。
        """
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        base_url = base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

        def vision_fn(media_bytes: bytes, mime_type: str, prompt: str) -> str:
            import urllib.request
            import json

            b64 = base64.b64encode(media_bytes).decode()
            data_url = f"data:{mime_type};base64,{b64}"

            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }]

            payload = json.dumps({
                "model": model,
                "messages": messages,
                "max_tokens": 2000,
            }).encode()

            req = urllib.request.Request(
                f"{base_url}/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
            )
            _validate_url(f"{base_url}/chat/completions")
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]

        def audio_fn(audio_bytes: bytes, mime_type: str) -> str:
            import urllib.request
            import json

            # Whisper API
            boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
            ext = mime_type.split("/")[-1] if "/" in mime_type else "wav"
            body = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="audio.{ext}"\r\n'
                f"Content-Type: {mime_type}\r\n\r\n"
            ).encode() + audio_bytes + (
                f"\r\n--{boundary}\r\n"
                f'Content-Disposition: form-data; name="model"\r\n\r\n'
                f"whisper-1\r\n"
                f"--{boundary}--\r\n"
            ).encode()

            req = urllib.request.Request(
                f"{base_url}/audio/transcriptions",
                data=body,
                headers={
                    "Content-Type": f"multipart/form-data; boundary={boundary}",
                    "Authorization": f"Bearer {api_key}",
                },
            )
            _validate_url(f"{base_url}/audio/transcriptions")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
            return result.get("text", "")

        return cls(vision_fn=vision_fn, audio_fn=audio_fn)

    @classmethod
    def from_mimo_omni(
        cls,
        api_url: str = None,
        api_key: str = None,
    ) -> "MediaProcessor":
        """
        用小米 MiMo Omni 多模态模型创建处理器。
        """
        api_url = api_url or os.environ.get("MIMO_API_URL", "")
        api_key = api_key or os.environ.get("MIMO_API_KEY", "")

        def vision_fn(media_bytes: bytes, mime_type: str, prompt: str) -> str:
            import urllib.request
            import json

            b64 = base64.b64encode(media_bytes).decode()

            payload = json.dumps({
                "image": b64,
                "prompt": prompt,
            }).encode()

            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            req = urllib.request.Request(
                f"{api_url}/analyze_image",
                data=payload,
                headers=headers,
            )
            _validate_url(f"{api_url}/analyze_image")
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
            return result.get("result", result.get("text", ""))

        def audio_fn(audio_bytes: bytes, mime_type: str) -> str:
            import urllib.request
            import json

            b64 = base64.b64encode(audio_bytes).decode()

            payload = json.dumps({
                "audio": b64,
                "prompt": "转录音频内容",
            }).encode()

            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            req = urllib.request.Request(
                f"{api_url}/analyze_audio",
                data=payload,
                headers=headers,
            )
            _validate_url(f"{api_url}/analyze_audio")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
            return result.get("result", result.get("text", ""))

        return cls(vision_fn=vision_fn, audio_fn=audio_fn)

    @classmethod
    def from_anthropic(
        cls,
        api_key: str = None,
        model: str = "claude-3-5-sonnet-20241022",
    ) -> "MediaProcessor":
        """
        用 Anthropic Claude 创建处理器。

        Claude 3.5 Sonnet / Claude 3 Opus 支持图片理解。
        音频需要走其他通道（Anthropic 暂不支持音频）。
        """
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        base_url = "https://api.anthropic.com"

        def vision_fn(media_bytes: bytes, mime_type: str, prompt: str) -> str:
            import urllib.request
            import json

            b64 = base64.b64encode(media_bytes).decode()
            media_type = mime_type.split("/")[-1] if "/" in mime_type else "jpeg"

            messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }]

            payload = json.dumps({
                "model": model,
                "max_tokens": 2000,
                "messages": messages,
            }).encode()

            req = urllib.request.Request(
                f"{base_url}/v1/messages",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                },
            )
            _validate_url(f"{base_url}/v1/messages")
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
            return result["content"][0]["text"]

        return cls(vision_fn=vision_fn, audio_fn=None)

    @classmethod
    def from_google(
        cls,
        api_key: str = None,
        model: str = "gemini-1.5-pro",
    ) -> "MediaProcessor":
        """
        用 Google Gemini 创建处理器。

        Gemini 1.5 Pro/Flash 支持图片、音频、视频。
        """
        api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        base_url = "https://generativelanguage.googleapis.com/v1beta"

        def vision_fn(media_bytes: bytes, mime_type: str, prompt: str) -> str:
            import urllib.request
            import json

            b64 = base64.b64encode(media_bytes).decode()

            payload = json.dumps({
                "contents": [{
                    "parts": [
                        {"inline_data": {"mime_type": mime_type, "data": b64}},
                        {"text": prompt},
                    ]
                }],
                "generationConfig": {"maxOutputTokens": 2000},
            }).encode()

            req = urllib.request.Request(
                f"{base_url}/models/{model}:generateContent",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": api_key,
                },
            )
            _validate_url(f"{base_url}/models/{model}:generateContent")
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
            return result["candidates"][0]["content"]["parts"][0]["text"]

        def audio_fn(audio_bytes: bytes, mime_type: str) -> str:
            import urllib.request
            import json

            b64 = base64.b64encode(audio_bytes).decode()

            payload = json.dumps({
                "contents": [{
                    "parts": [
                        {"inline_data": {"mime_type": mime_type, "data": b64}},
                        {"text": "请将这段音频完整转写为文字。"},
                    ]
                }],
                "generationConfig": {"maxOutputTokens": 4000},
            }).encode()

            req = urllib.request.Request(
                f"{base_url}/models/{model}:generateContent",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": api_key,
                },
            )
            _validate_url(f"{base_url}/models/{model}:generateContent")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
            return result["candidates"][0]["content"]["parts"][0]["text"]

        return cls(vision_fn=vision_fn, audio_fn=audio_fn)

    @classmethod
    def from_ollama(
        cls,
        model: str = "llava:13b",
        host: str = None,
    ) -> "MediaProcessor":
        """
        用 Ollama 本地模型创建处理器。

        支持的视觉模型：llava, llava-llama3, bakllava, moondream
        支持的音频模型：需要搭配 whisper 等
        """
        host = host or os.environ.get("OLLAMA_HOST", os.environ.get("OLLAMA_API_URL", "http://127.0.0.1:11434"))

        def vision_fn(media_bytes: bytes, mime_type: str, prompt: str) -> str:
            import urllib.request
            import json

            b64 = base64.b64encode(media_bytes).decode()

            payload = json.dumps({
                "model": model,
                "prompt": prompt,
                "images": [b64],
                "stream": False,
            }).encode()

            req = urllib.request.Request(
                f"{host}/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            _validate_url(f"{host}/api/generate")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
            return result.get("response", "")

        return cls(vision_fn=vision_fn, audio_fn=None)

    @classmethod
    def from_litellm(
        cls,
        model: str = "gpt-4o",
        api_key: str = None,
        api_base: str = None,
    ) -> "MediaProcessor":
        """
        用 LiteLLM 代理创建处理器。

        LiteLLM 支持 100+ 模型供应商的统一接口：
        openai/gpt-4o, anthropic/claude-3-5-sonnet, gemini/gemini-1.5-pro,
        ollama/llava, azure/gpt-4, deepseek/deepseek-vl, etc.
        """
        api_key = api_key or os.environ.get("LITELLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
        api_base = api_base or os.environ.get("LITELLM_API_BASE", os.environ.get("LITELLM_API_URL", "http://127.0.0.1:4000"))

        def vision_fn(media_bytes: bytes, mime_type: str, prompt: str) -> str:
            import urllib.request
            import json

            b64 = base64.b64encode(media_bytes).decode()
            data_url = f"data:{mime_type};base64,{b64}"

            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }]

            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            payload = json.dumps({
                "model": model,
                "messages": messages,
                "max_tokens": 2000,
            }).encode()

            req = urllib.request.Request(
                f"{api_base}/chat/completions",
                data=payload,
                headers=headers,
            )
            _validate_url(f"{api_base}/chat/completions")
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]

        return cls(vision_fn=vision_fn, audio_fn=None)

    @classmethod
    def auto(cls) -> "MediaProcessor":
        """
        自动检测环境变量，选择最佳后端。

        检测顺序：
        1. OPENAI_API_KEY → OpenAI GPT-4o
        2. ANTHROPIC_API_KEY → Claude 3.5
        3. GOOGLE_API_KEY → Gemini 1.5
        4. MIMO_API_URL → MiMo Omni
        5. OLLAMA_HOST → Ollama 本地
        6. None → 无多模态能力
        """
        if os.environ.get("OPENAI_API_KEY"):
            try:
                p = cls.from_openai()
                logger.info("自动检测: OpenAI (GPT-4o)")
                return p
            except Exception as e:
                logger.debug(f"OpenAI 初始化失败: {e}")

        if os.environ.get("ANTHROPIC_API_KEY"):
            try:
                p = cls.from_anthropic()
                logger.info("自动检测: Anthropic (Claude 3.5)")
                return p
            except Exception as e:
                logger.debug(f"Anthropic 初始化失败: {e}")

        if os.environ.get("GOOGLE_API_KEY"):
            try:
                p = cls.from_google()
                logger.info("自动检测: Google (Gemini 1.5)")
                return p
            except Exception as e:
                logger.debug(f"Google 初始化失败: {e}")

        if os.environ.get("MIMO_API_URL"):
            try:
                p = cls.from_mimo_omni()
                logger.info("自动检测: MiMo Omni")
                return p
            except Exception as e:
                logger.debug(f"MiMo 初始化失败: {e}")

        if os.environ.get("OLLAMA_HOST"):
            try:
                p = cls.from_ollama()
                logger.info("自动检测: Ollama 本地")
                return p
            except Exception as e:
                logger.debug(f"Ollama 初始化失败: {e}")

        return cls()

    def process(
        self,
        file_path: str,
        prompt: str = None,
    ) -> dict:
        """
        处理一个媒体文件，返回结构化结果。

        返回:
        {
            "success": bool,
            "media_type": "image" | "audio" | "video",
            "description": str,        # 模型输出的描述/转写
            "metadata": dict,          # 文件元数据
            "error": str | None,
        }
        """
        if not os.path.exists(file_path):
            return {"success": False, "media_type": None, "description": "", "metadata": {}, "error": "文件不存在"}

        file_size = os.path.getsize(file_path)
        if file_size > 100 * 1024 * 1024:  # 100MB 上限
            return {"success": False, "media_type": None, "description": "", "metadata": {}, "error": "文件过大（上限 100MB）"}

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ALL_FORMATS:
            return {"success": False, "media_type": None, "description": "", "metadata": {}, "error": f"不支持的格式: {ext}"}

        # 判断媒体类型
        if ext in IMAGE_FORMATS:
            return self._process_image(file_path, prompt or self.DEFAULT_IMAGE_PROMPT)
        elif ext in AUDIO_FORMATS:
            return self._process_audio(file_path)
        elif ext in VIDEO_FORMATS:
            return self._process_video(file_path, prompt or self.DEFAULT_VIDEO_PROMPT)

        return {"success": False, "media_type": None, "description": "", "metadata": {}, "error": "未知格式"}

    def _process_image(self, file_path: str, prompt: str) -> dict:
        """处理图片"""
        import mimetypes

        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        mime_type = mimetypes.guess_type(file_path)[0] or "image/png"

        metadata = {"filename": filename, "size_kb": file_size // 1024, "format": mime_type}

        # 提取图片尺寸
        try:
            from PIL import Image
            img = Image.open(file_path)
            metadata["width"] = img.width
            metadata["height"] = img.height
            metadata["format_pil"] = img.format
            img.close()
        except Exception as e:
            logger.warning("media_processor: %s", e)

        # 调用视觉模型
        if self.vision_fn:
            try:
                with open(file_path, "rb") as f:
                    media_bytes = f.read()
                description = self.vision_fn(media_bytes, mime_type, prompt)
                return {
                    "success": True,
                    "media_type": "image",
                    "description": description,
                    "metadata": metadata,
                    "error": None,
                }
            except Exception as e:
                logger.warning("media_processor: %s", e)
                return {
                    "success": False,
                    "media_type": "image",
                    "description": "",
                    "metadata": metadata,
                    "error": f"视觉模型调用失败: {e}",
                }

        # 降级：只返回元数据
        return {
            "success": True,
            "media_type": "image",
            "description": f"图片: {filename} ({metadata.get('width', '?')}x{metadata.get('height', '?')})",
            "metadata": metadata,
            "error": None,
        }

    def _process_audio(self, file_path: str) -> dict:
        """处理音频"""
        import mimetypes

        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        mime_type = mimetypes.guess_type(file_path)[0] or "audio/wav"

        metadata = {"filename": filename, "size_kb": file_size // 1024, "format": mime_type}

        # 获取音频时长
        try:
            import wave
            if file_path.endswith(".wav"):
                with wave.open(file_path, "r") as w:
                    metadata["duration_sec"] = round(w.getnframes() / w.getframerate(), 1)
        except Exception as e:
            logger.warning("media_processor: %s", e)

        # 调用语音模型
        if self.audio_fn:
            try:
                with open(file_path, "rb") as f:
                    audio_bytes = f.read()
                transcript = self.audio_fn(audio_bytes, mime_type)
                return {
                    "success": True,
                    "media_type": "audio",
                    "description": transcript,
                    "metadata": metadata,
                    "error": None,
                }
            except Exception as e:
                logger.warning("media_processor: %s", e)
                return {
                    "success": False,
                    "media_type": "audio",
                    "description": "",
                    "metadata": metadata,
                    "error": f"语音模型调用失败: {e}",
                }

        return {
            "success": True,
            "media_type": "audio",
            "description": f"音频: {filename}",
            "metadata": metadata,
            "error": None,
        }

    def _process_video(self, file_path: str, prompt: str) -> dict:
        """处理视频：提取关键帧 + 音频"""
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        metadata = {"filename": filename, "size_mb": file_size // (1024 * 1024)}

        # 获取视频时长
        duration = self._get_video_duration(file_path)
        if duration:
            metadata["duration_sec"] = duration

        descriptions = []
        transcript = ""

        # 1. 提取关键帧并用视觉模型分析
        if self.vision_fn:
            frames = self._extract_keyframes(file_path, max_frames=3)
            for i, frame_path in enumerate(frames):
                try:
                    frame_result = self._process_image(frame_path, f"这是视频第{i+1}个关键帧。{prompt}")
                    if frame_result["success"]:
                        descriptions.append(f"[关键帧{i+1}] {frame_result['description']}")
                except Exception as e:
                    logger.debug(f"关键帧 {i} 分析失败: {e}")
                finally:
                    # 清理临时帧
                    try:
                        os.unlink(frame_path)
                    except Exception as e:
                        logger.warning("media_processor: %s", e)

        # 2. 提取音频并转写
        if self.audio_fn:
            audio_path = self._extract_audio(file_path)
            if audio_path:
                try:
                    audio_result = self._process_audio(audio_path)
                    if audio_result["success"] and audio_result["description"]:
                        transcript = audio_result["description"]
                        descriptions.append(f"[音频转写] {transcript}")
                except Exception as e:
                    logger.debug(f"音频提取失败: {e}")
                finally:
                    try:
                        os.unlink(audio_path)
                    except Exception as e:
                        logger.warning("media_processor: %s", e)

        result = {
            "success": True,
            "media_type": "video",
            "description": "\n".join(descriptions),
            "transcript": transcript,  # 添加完整转录
            "metadata": metadata,
            "error": None,
        }

        if not descriptions:
            result["description"] = f"视频: {filename} ({metadata.get('duration_sec', '?')}秒)"

        return result

    def process_for_style(self, file_path: str) -> dict:
        """处理媒体文件用于风格分析
        
        Returns:
        {
            "success": bool,
            "content": str,  # 提取的文本内容
            "media_type": "image" | "audio" | "video",
            "metadata": dict,
        }
        """
        result = self.process(file_path)
        if not result["success"]:
            return {
                "success": False,
                "content": "",
                "media_type": result.get("media_type"),
                "metadata": result.get("metadata", {}),
            }
        
        # 提取内容用于风格分析
        content = ""
        if result["media_type"] == "video":
            # 优先使用完整转录
            content = result.get("transcript", result.get("description", ""))
        else:
            content = result.get("description", "")
        
        return {
            "success": True,
            "content": content,
            "media_type": result["media_type"],
            "metadata": result.get("metadata", {}),
        }

    def _extract_keyframes(self, video_path: str, max_frames: int = 3) -> list[str]:
        """用 ffmpeg 提取关键帧"""
        frames = []
        try:
            duration = self._get_video_duration(video_path) or 10
            for i in range(max_frames):
                timestamp = duration * (i + 1) / (max_frames + 1)
                fd, frame_path = tempfile.mkstemp(suffix=".jpg")
                os.close(fd)
                cmd = [
                    "ffmpeg", "-y", "-ss", str(timestamp),
                    "-i", video_path, "-frames:v", "1",
                    "-q:v", "2", frame_path,
                ]
                result = subprocess.run(cmd, capture_output=True, timeout=30)
                if result.returncode == 0 and os.path.exists(frame_path):
                    frames.append(frame_path)
        except FileNotFoundError:
            logger.debug("ffmpeg 未安装，跳过关键帧提取")
        except Exception as e:
            logger.debug(f"关键帧提取失败: {e}")
        return frames

    def _extract_audio(self, video_path: str) -> str | None:
        """用 ffmpeg 提取音频"""
        try:
            fd, audio_path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            cmd = [
                "ffmpeg", "-y", "-i", video_path,
                "-vn", "-acodec", "pcm_s16le",
                "-ar", "16000", "-ac", "1",
                audio_path,
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            if result.returncode == 0 and os.path.exists(audio_path):
                return audio_path
        except FileNotFoundError:
            logger.debug("ffmpeg 未安装，跳过音频提取")
        except Exception as e:
            logger.warning("media_processor: %s", e)
        return None

    def _get_video_duration(self, video_path: str) -> float | None:
        """获取视频时长"""
        try:
            cmd = [
                "ffprobe", "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                video_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return float(result.stdout.strip())
        except Exception as e:
            logger.warning("media_processor: %s", e)
        return None

    @property
    def is_available(self) -> bool:
        return self.vision_fn is not None or self.audio_fn is not None

    def get_stats(self) -> dict:
        return {
            "vision_available": self.vision_fn is not None,
            "audio_available": self.audio_fn is not None,
            "video_available": self.vision_fn is not None and self.audio_fn is not None,
            "supported_image": list(IMAGE_FORMATS),
            "supported_audio": list(AUDIO_FORMATS),
            "supported_video": list(VIDEO_FORMATS),
        }
