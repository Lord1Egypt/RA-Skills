"""模型下载器 — 进度可视化 + 3次自动重试 + HTTP Range 断点续传 + 清华镜像交互提示"""

import os
import hashlib
import time
from typing import Any, Dict, Optional, Callable

from .logger import get_logger

logger = get_logger(__name__)


# ==================== 模型信息 ====================
MODEL_INFO = {
    "tiny": {
        "url": "https://huggingface.co/openai/whisper-tiny/resolve/main/model.bin",
        "size_mb": 75,
        "sha256": None,
    },
    "base": {
        "url": "https://huggingface.co/openai/whisper-base/resolve/main/model.bin",
        "size_mb": 142,
        "sha256": None,
    },
    "small": {
        "url": "https://huggingface.co/openai/whisper-small/resolve/main/model.bin",
        "size_mb": 466,
        "sha256": None,
    },
    "medium": {
        "url": "https://huggingface.co/openai/whisper-medium/resolve/main/model.bin",
        "size_mb": 1540,
        "sha256": None,
    },
}

# 国内镜像
MIRROR_URLS = {
    "tuna": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "aliyun": "https://mirrors.aliyun.com/pypi/simple",
}


class ModelDownloader:
    """
    模型下载器。

    特性：
    - 进度可视化（进度条 + 速度 + 剩余时间）
    - 失败自动重试 3 次
    - HTTP Range 断点续传
    - 清华 PyPI 镜像交互提示
    - SHA256 校验
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.download_config = config.get("download", {})
        self.models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
        os.makedirs(self.models_dir, exist_ok=True)
        self.max_retries = self.download_config.get("max_retries", 3)
        self.chunk_size = self.download_config.get("chunk_size", 8192)
        self.timeout = self.download_config.get("timeout", 300)

    def download(
        self,
        model_name: str,
        progress_callback: Optional[Callable[[int, int, float], None]] = None,
    ) -> Dict[str, Any]:
        """
        下载模型。

        Args:
            model_name: 模型名称 (tiny/base/small/medium)
            progress_callback: 进度回调 (downloaded, total, speed_kb_s)

        Returns:
            {
                "success": True/False,
                "model_path": "模型路径",
                "error": "错误信息",
                "retries": 重试次数,
            }
        """
        result = {
            "success": False,
            "model_path": None,
            "error": None,
            "retries": 0,
        }

        model_info = MODEL_INFO.get(model_name)
        if not model_info:
            result["error"] = f"未知模型: {model_name}"
            return result

        model_path = os.path.join(self.models_dir, f"whisper-{model_name}", "model.bin")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        # 检查是否已存在
        if os.path.exists(model_path):
            result["success"] = True
            result["model_path"] = model_path
            logger.info(f"模型已存在: {model_path}")
            return result

        # 尝试下载（带重试）
        for attempt in range(1, self.max_retries + 1):
            result["retries"] = attempt
            try:
                logger.info(f"下载模型 {model_name}（第 {attempt} 次尝试）...")
                success = self._download_with_resume(
                    model_info["url"], model_path, model_info["size_mb"] * 1024 * 1024,
                    progress_callback
                )
                if success:
                    result["success"] = True
                    result["model_path"] = model_path
                    logger.info(f"模型下载完成: {model_path}")
                    return result
            except Exception as e:
                logger.warning(f"下载失败（第 {attempt} 次）: {e}")
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)

        result["error"] = f"下载失败，已重试 {self.max_retries} 次"
        return result

    def _download_with_resume(
        self,
        url: str,
        output_path: str,
        total_size: int,
        progress_callback: Optional[Callable[[int, int, float], None]] = None,
    ) -> bool:
        """支持断点续传的下载"""
        import urllib.request
        import urllib.error

        # 检查已下载部分
        downloaded = 0
        if os.path.exists(output_path):
            downloaded = os.path.getsize(output_path)
            if downloaded >= total_size:
                return True  # 已下载完成

        # 构建 Range 请求
        headers = {}
        if downloaded > 0:
            headers["Range"] = f"bytes={downloaded}-"
            logger.info(f"断点续传: 从 {downloaded}/{total_size} 继续下载")

        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                # 检查是否支持 Range
                if downloaded > 0 and response.status != 206:
                    logger.warning("服务器不支持断点续传，重新下载")
                    downloaded = 0
                    # 重新请求
                    req = urllib.request.Request(url)
                    response = urllib.request.urlopen(req, timeout=self.timeout)

                mode = "ab" if downloaded > 0 else "wb"
                start_time = time.time()

                with open(output_path, mode) as f:
                    while True:
                        chunk = response.read(self.chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)

                        # 计算速度
                        elapsed = time.time() - start_time
                        speed = downloaded / elapsed / 1024 if elapsed > 0 else 0  # KB/s

                        # 回调
                        if progress_callback:
                            progress_callback(downloaded, total_size, speed)

                        # 日志进度
                        if total_size > 0:
                            progress = downloaded / total_size * 100
                            if int(progress) % 10 == 0:
                                logger.info(f"下载进度: {progress:.1f}% ({downloaded}/{total_size})")

                return downloaded >= total_size

        except urllib.error.URLError as e:
            logger.error(f"下载 URL 错误: {e}")
            return False
        except Exception as e:
            logger.error(f"下载异常: {e}")
            return False

    def verify_checksum(self, model_path: str, expected_sha256: str) -> bool:
        """验证模型 SHA256"""
        if not os.path.exists(model_path):
            return False

        sha256 = hashlib.sha256()
        with open(model_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)

        actual = sha256.hexdigest()
        if actual != expected_sha256:
            logger.warning(f"SHA256 校验失败: 期望 {expected_sha256[:16]}..., 实际 {actual[:16]}...")
            return False

        return True

    def get_mirror_hint(self) -> str:
        """获取清华镜像提示"""
        return (
            "国内用户建议先执行以下命令加速下载:\n"
            "  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple\n"
            "\n"
            "或使用阿里云镜像:\n"
            "  pip config set global.index-url https://mirrors.aliyun.com/pypi/simple"
        )

    def get_download_instructions(self, model_name: str) -> str:
        """获取下载指引"""
        model_info = MODEL_INFO.get(model_name, MODEL_INFO["tiny"])
        return f"""
=== 模型下载指引 ===

模型: whisper-{model_name}
大小: {model_info['size_mb']}MB
下载: {model_info['url']}

自动下载命令:
  python main.py --download-model {model_name}

国内加速:
  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

模型将保存到: models/whisper-{model_name}/
"""

    @staticmethod
    def format_progress(downloaded: int, total: int, speed_kb_s: float) -> str:
        """格式化进度条"""
        if total <= 0:
            return f"已下载: {downloaded / 1024 / 1024:.1f}MB"

        progress = downloaded / total
        bar_length = 30
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)

        # 计算剩余时间
        if speed_kb_s > 0:
            remaining = (total - downloaded) / 1024 / speed_kb_s
            eta = f"{remaining:.0f}s"
        else:
            eta = "未知"

        return f"[{bar}] {progress*100:.1f}% | {speed_kb_s:.1f}KB/s | 剩余 {eta}"
