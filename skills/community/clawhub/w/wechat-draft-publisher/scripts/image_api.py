"""
通用 AI 文生图模块
支持任何兼容 OpenAI 格式的文生图 API（SiliconFlow、Kimi、智谱、通义等）
"""

import json
import os
import time
import requests


class AIImageGenerator:
    """通用 AI 文生图客户端"""

    def __init__(self, api_key: str, api_base_url: str, model: str = ""):
        self.api_key = api_key
        self.api_base_url = api_base_url.rstrip("/")
        self.model = model

        if not self.api_key:
            raise ValueError("未配置 image_api.api_key，请在 config.json 中填写")
        if not self.api_base_url:
            raise ValueError("未配置 image_api.api_base_url，请在 config.json 中填写")

    def _generate(self, prompt: str, size: str = "1024x1024") -> str:
        """调用文生图 API，返回生成图片的 URL"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"prompt": prompt, "size": size}
        if self.model:
            payload["model"] = self.model

        resp = requests.post(
            self.api_base_url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            timeout=120,
        )

        data = resp.json()

        # 异步任务模式（部分服务返回 task_id 需要轮询）
        if "task_id" in data:
            return self._poll_task(data["task_id"])

        # OpenAI 标准格式: {"data": [{"url": "..."}]}
        if "data" in data and data["data"]:
            return data["data"][0].get("url", "")

        # 部分服务格式: {"images": [{"url": "..."}]}
        if "images" in data and data["images"]:
            return data["images"][0].get("url", "")

        # 返回 base64 的情况
        if "data" in data and data["data"]:
            b64 = data["data"][0].get("b64_json", "")
            if b64:
                return f"data:image/png;base64,{b64}"

        raise RuntimeError(f"图片生成失败: {data}")

    def _poll_task(self, task_id: str, max_wait: int = 120) -> str:
        """轮询异步任务直到完成"""
        # 从 api_base_url 推断任务查询地址
        base = self.api_base_url.rsplit("/", 1)[0]
        status_url = f"{base}/tasks/{task_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        start = time.time()
        while time.time() - start < max_wait:
            resp = requests.get(status_url, headers=headers, timeout=10)
            data = resp.json()
            status = data.get("status", "")

            if status in ("SUCCEEDED", "succeeded", "completed"):
                images = data.get("output", {}).get("images", [])
                if images:
                    return images[0].get("url", "")
                # 尝试其他格式
                if "data" in data and data["data"]:
                    return data["data"][0].get("url", "")
                raise RuntimeError(f"任务完成但未返回图片: {data}")

            if status in ("FAILED", "failed", "CANCELLED", "cancelled"):
                raise RuntimeError(f"图片生成任务失败: {data}")

            time.sleep(3)

        raise TimeoutError(f"图片生成超时（等待 {max_wait}s）")

    def _download_image(self, url: str, save_path: str) -> str:
        """下载图片到本地"""
        if url.startswith("data:"):
            # base64 数据直接写入
            import base64
            b64_data = url.split(",", 1)[1]
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(b64_data))
        else:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(resp.content)
        return save_path

    def generate_article_image(
        self, prompt: str, save_dir: str, index: int = 0
    ) -> str:
        """生成文章配图，返回本地图片路径"""
        enhanced_prompt = (
            f"{prompt}, high quality, detailed illustration, "
            f"clean composition, professional, vivid colors"
        )
        url = self._generate(enhanced_prompt, size="1024x1024")
        save_path = os.path.join(save_dir, f"article_img_{index}.png")
        return self._download_image(url, save_path)

    def generate_cover_image(self, prompt: str, save_dir: str) -> str:
        """生成封面图（宽幅横图），返回本地图片路径"""
        enhanced_prompt = (
            f"{prompt}, wide banner style, eye-catching, "
            f"clean design, professional, minimal text area on left"
        )
        url = self._generate(enhanced_prompt, size="1440x720")
        save_path = os.path.join(save_dir, "cover.png")
        return self._download_image(url, save_path)
