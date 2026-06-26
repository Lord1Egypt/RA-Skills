# -*- coding: utf-8 -*-
"""
视频生成引擎（仅 API）：调用火山方舟 Seedance 等模型的视频生成接口。
不支持本地视频模型，仅支持 API 调用。
异步流程：创建任务 -> 轮询或 Webhook 获取结果 -> 从 content.video_url 下载 MP4。
"""

import os
import time
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

try:
    import requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False


class VideoGenEngine:
    """基于火山方舟 Content Generation API 的视频生成（如 Seedance）。"""

    DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
    DEFAULT_MODEL = "doubao-seedance-1-5-pro-251215"

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", False)
        self.base_url = (config.get("base_url") or self.DEFAULT_BASE_URL).rstrip("/")
        self.model = config.get("model_id") or config.get("model") or self.DEFAULT_MODEL
        self.api_key = config.get("api_key") or os.environ.get("ARK_API_KEY", "")
        self.poll_interval = config.get("poll_interval_seconds", 5)
        self.poll_timeout = config.get("poll_timeout_seconds", 600)

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_task(
        self,
        content: List[Dict[str, Any]],
        *,
        generate_audio: bool = True,
        ratio: str = "adaptive",
        duration: int = 5,
        watermark: bool = False,
    ) -> Dict[str, Any]:
        """
        创建视频生成任务。
        :param content: 内容列表，每项为 {"type": "text", "text": "..."} 或 {"type": "image_url", "image_url": {"url": "..."}}
        :return: {"success": True, "task_id": "cgt-..."} 或 {"success": False, "error": "..."}
        """
        if not _REQUESTS_AVAILABLE:
            return {"success": False, "error": "requests 未安装，请执行: pip install requests"}
        if not self.api_key:
            return {"success": False, "error": "未配置 ARK_API_KEY 或 video_generation.api_key"}
        if not (self.model and str(self.model).strip()):
            return {
                "success": False,
                "error": "未配置 video_generation.model_id。视频 API 要求 model 为「推理接入点 ID」（在火山方舟控制台创建），见 https://www.volcengine.com/docs/82379/1099522",
            }
        if not content:
            return {"success": False, "error": "content 不能为空"}

        url = f"{self.base_url}/contents/generations/tasks"
        body = {
            "model": self.model,
            "content": content,
            "generate_audio": generate_audio,
            "ratio": ratio,
            "duration": duration,
            "watermark": watermark,
        }
        logger.info("视频 API 请求 content: %s", content)
        try:
            r = requests.post(url, json=body, headers=self._headers(), timeout=60)
            r.raise_for_status()
            data = r.json()
            task_id = data.get("id")
            if not task_id:
                return {"success": False, "error": "API 未返回 task id"}
            return {"success": True, "task_id": task_id}
        except requests.exceptions.RequestException as e:
            err = getattr(e, "response", None)
            msg = str(e)
            if err is not None:
                try:
                    body = err.text
                    if body:
                        msg = f"{msg}\nAPI 返回: {body}"
                    try:
                        j = err.json()
                        if isinstance(j, dict) and (j.get("message") or j.get("error") or j.get("error_message")):
                            msg = f"{msg}\n详细: {j}"
                    except Exception:
                        pass
                except Exception:
                    pass
            logger.warning("Video gen create task request failed: %s", msg)
            return {"success": False, "error": msg}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """
        查询视频生成任务状态与结果。
        :return: 含 status, content.video_url（成功时）等；或 {"success": False, "error": "..."}
        """
        if not _REQUESTS_AVAILABLE:
            return {"success": False, "error": "requests 未安装"}
        if not self.api_key:
            return {"success": False, "error": "未配置 ARK_API_KEY 或 video_generation.api_key"}

        url = f"{self.base_url}/contents/generations/tasks/{task_id}"
        try:
            r = requests.get(url, headers=self._headers(), timeout=30)
            r.raise_for_status()
            data = r.json()
            data["success"] = True
            return data
        except requests.exceptions.RequestException as e:
            err = getattr(e, "response", None)
            msg = err.text if err and hasattr(err, "text") else str(e)
            return {"success": False, "error": msg or str(e)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def wait_for_task(
        self,
        task_id: str,
        poll_interval: Optional[float] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        轮询任务直到完成或超时。
        :return: get_task 的返回结构；status 为 succeeded 时含 content.video_url
        """
        interval = poll_interval if poll_interval is not None else self.poll_interval
        deadline = timeout if timeout is not None else self.poll_timeout
        started = time.time()
        while True:
            result = self.get_task(task_id)
            if not result.get("success"):
                return result
            status = result.get("status", "")
            if status == "succeeded":
                return result
            if status in ("failed", "cancelled"):
                return {**result, "success": False, "error": result.get("message") or f"任务状态: {status}"}
            if time.time() - started > deadline:
                return {**result, "success": False, "error": "轮询超时"}
            time.sleep(interval)

    def create_task_from_prompt(
        self,
        text: str,
        image_url: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        根据提示词（及可选首图）创建视频生成任务。
        :param text: 文本描述
        :param image_url: 可选首帧图 URL（首帧图生视频）
        """
        content: List[Dict[str, Any]] = [{"type": "text", "text": text}]
        if image_url:
            content.append({"type": "image_url", "image_url": {"url": image_url}})
        return self.create_task(content, **kwargs)
