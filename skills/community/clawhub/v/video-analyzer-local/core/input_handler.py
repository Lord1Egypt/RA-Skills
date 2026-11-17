"""输入处理模块 — 支持本地文件、URL、在线视频链接 + 禁止文件类型拦截"""

import os
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Optional
import shutil

from .logger import get_logger

logger = get_logger(__name__)

# 最大重试次数
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒

# ==================== 禁止的文件类型（死规则） ====================
# Windows 可执行 / 批处理脚本
FORBIDDEN_EXEC_EXTENSIONS = {
    ".bat", ".cmd", ".ps1", ".vbs", ".exe", ".dll", ".lnk", ".msi",
}
# Office 二进制文档
FORBIDDEN_OFFICE_EXTENSIONS = {
    ".docx", ".xlsx", ".pptx", ".doc", ".xls", ".ppt",
    ".xlsm", ".docm", ".pptm",
}
# 二进制镜像 / 安装包
FORBIDDEN_ARCHIVE_EXTENSIONS = {
    ".iso", ".dmg", ".zip", ".rar", ".7z", ".tar", ".gz",
    ".apk", ".jar",
}
# 系统缓存 / 隐藏文件
FORBIDDEN_SYSTEM_EXTENSIONS = {
    ".ds_store", ".env", ".log", ".tmp",
}
# 其他风险脚本
FORBIDDEN_SCRIPT_EXTENSIONS = {
    ".sh", ".com", ".scr", ".hta", ".reg",
}

# 合并所有禁止的扩展名
FORBIDDEN_EXTENSIONS = (
    FORBIDDEN_EXEC_EXTENSIONS
    | FORBIDDEN_OFFICE_EXTENSIONS
    | FORBIDDEN_ARCHIVE_EXTENSIONS
    | FORBIDDEN_SYSTEM_EXTENSIONS
    | FORBIDDEN_SCRIPT_EXTENSIONS
)

# 禁止的文件名（部分系统缓存文件无扩展名或用点开头）
FORBIDDEN_FILENAMES = {".ds_store", "thumbs.db", "desktop.ini"}

# 禁止的目录名
FORBIDDEN_DIR_NAMES = {".git", ".svn", ".hg"}


class InputHandler:
    """处理各种视频输入来源，统一转为本地路径"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.temp_dir = config.get("processing", {}).get("temp_dir", ".temp")
        self.timeout = config.get("processing", {}).get("download_timeout", 300)
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def process(self, input_source: str) -> str:
        """
        处理输入，返回本地视频文件路径。
        
        Args:
            input_source: 本地路径、URL 或在线视频链接
            
        Returns:
            本地文件绝对路径
        """
        source = input_source.strip()
        
        # 判断输入类型
        if self._is_local_path(source):
            return self._handle_local(source)
        elif self._is_url(source):
            return self._handle_url(source)
        else:
            # 尝试作为本地路径处理
            if os.path.exists(source):
                return os.path.abspath(source)
            raise ValueError(f"无法识别的输入: {input_source}")
    
    def _validate_not_forbidden(self, path: Path) -> None:
        """
        验证文件类型是否被禁止，禁止则抛出异常。
        
        Args:
            path: 要验证的文件路径
            
        Raises:
            ValueError: 文件类型被禁止时抛出
        """
        filename = path.name.lower()
        suffix = path.suffix.lower() if path.suffix else ""
        
        # 检查文件名（如 .ds_store）
        if filename in FORBIDDEN_FILENAMES:
            raise ValueError(
                f"🚫 禁止的文件类型: {path.name}\n"
                f"   系统缓存/隐藏文件不在支持范围内。\n"
                f"   请提供视频文件（如 .mp4, .mkv, .avi, .mov 等）。"
            )
        
        # 检查扩展名
        if suffix in FORBIDDEN_EXTENSIONS:
            # 分类说明
            if suffix in FORBIDDEN_EXEC_EXTENSIONS:
                category = "Windows 可执行/脚本文件"
            elif suffix in FORBIDDEN_OFFICE_EXTENSIONS:
                category = "Office 二进制文档"
            elif suffix in FORBIDDEN_ARCHIVE_EXTENSIONS:
                category = "压缩包/镜像文件"
            elif suffix in FORBIDDEN_SYSTEM_EXTENSIONS:
                category = "系统缓存/配置文件"
            elif suffix in FORBIDDEN_SCRIPT_EXTENSIONS:
                category = "风险脚本文件"
            else:
                category = "不支持的文件类型"
            
            raise ValueError(
                f"🚫 禁止的文件类型: {suffix}\n"
                f"   类别: {category}\n"
                f"   文件: {path.name}\n"
                f"   本工具仅支持视频文件分析，不支持压缩包、可执行程序、"
                f"Office 文档等其他格式。"
            )
    
    def _is_local_path(self, source: str) -> bool:
        """判断是否为本地路径"""
        return (
            os.path.exists(source) or
            (len(source) >= 2 and source[0].isalpha() and source[1] == ":") or
            source.startswith(("/", "\\", "./", "../"))
        )
    
    def _is_url(self, source: str) -> bool:
        """判断是否为 URL"""
        return source.startswith(("http://", "https://", "ftp://"))
    
    def _handle_local(self, source: str) -> str:
        """处理本地文件路径"""
        path = Path(source).resolve()

        if not path.exists():
            raise FileNotFoundError(
                f"文件不存在: {source}\n"
                f"请确认文件路径是否正确，并确保有读取权限。"
            )

        if not path.is_file():
            raise ValueError(f"不是有效文件: {source}")

        # ==================== 禁止文件类型拦截 ====================
        self._validate_not_forbidden(path)

        # 验证是否为视频文件
        valid_extensions = {
            ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
            ".m4v", ".mpg", ".mpeg", ".ts", ".m3u8"
        }
        if path.suffix.lower() not in valid_extensions:
            logger.warning(f"文件扩展名可能不是视频格式: {path.suffix}")
        
        logger.info(f"本地文件: {path}")
        return str(path)
    
    def _handle_url(self, url: str) -> str:
        """下载远程视频到本地（带自动重试）"""
        logger.info(f"下载远程视频: {url}")
        
        # 生成本地文件名
        filename = self._get_filename_from_url(url)
        local_path = os.path.join(self.temp_dir, filename)
        
        # 如果文件已存在，直接返回
        if os.path.exists(local_path):
            logger.info(f"文件已缓存: {local_path}")
            return local_path
        
        # 尝试多种下载方式，每种最多重试 3 次
        download_methods = [
            ("yt-dlp", self._try_ytdlp),
            ("curl", self._try_curl),
            ("requests", self._try_requests),
        ]
        
        last_error = None
        for method_name, method_func in download_methods:
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    if method_func(url, local_path):
                        return local_path
                except Exception as e:
                    last_error = e
                    logger.debug(f"{method_name} 第 {attempt} 次尝试失败: {e}")
                
                if attempt < MAX_RETRIES:
                    logger.info(f"第 {attempt} 次下载失败，{RETRY_DELAY}秒后重试...")
                    time.sleep(RETRY_DELAY)
        
        # 所有方法均失败
        error_msg = (
            f"无法下载视频（已重试 {MAX_RETRIES} 次）: {url}\n"
            f"请检查：\n"
            f"  1. URL 是否可正常访问\n"
            f"  2. 网络连接是否稳定\n"
            f"  3. 对于 YouTube/B站等网站，请安装 yt-dlp: pip install yt-dlp"
        )
        if last_error:
            error_msg += f"\n最后错误: {last_error}"
        
        raise RuntimeError(error_msg)
    
    def _get_filename_from_url(self, url: str) -> str:
        """从 URL 中提取文件名"""
        try:
            parsed = urllib.parse.urlparse(url)
            path = parsed.path
            filename = os.path.basename(path)
            if filename and "." in filename:
                return filename
        except Exception:
            pass
        return f"video_{hash(url) % 10000:04d}.mp4"
    
    def _try_ytdlp(self, url: str, output_path: str) -> bool:
        """尝试使用 yt-dlp 下载"""
        try:
            import subprocess
            cmd = [
                "yt-dlp",
                "-f", "best[ext=mp4]/best",
                "-o", output_path,
                "--no-check-certificates",
                "--quiet",
                "--no-warnings",
                url
            ]
            result = subprocess.run(
                cmd, capture_output=True, timeout=self.timeout
            )
            return result.returncode == 0 and os.path.exists(output_path)
        except FileNotFoundError:
            logger.debug("yt-dlp 未安装")
            return False
        except Exception as e:
            logger.debug(f"yt-dlp 下载失败: {e}")
            return False
    
    def _try_curl(self, url: str, output_path: str) -> bool:
        """尝试使用 curl 下载"""
        try:
            import subprocess
            cmd = [
                "curl",
                "-L",  # 跟随重定向
                "-o", output_path,
                "--connect-timeout", "30",
                "--max-time", str(self.timeout),
                "--silent",
                "--show-error",
                url
            ]
            result = subprocess.run(
                cmd, capture_output=True, timeout=self.timeout + 30
            )
            return result.returncode == 0 and os.path.exists(output_path)
        except FileNotFoundError:
            logger.debug("curl 未安装")
            return False
        except Exception as e:
            logger.debug(f"curl 下载失败: {e}")
            return False
    
    def _try_requests(self, url: str, output_path: str) -> bool:
        """使用 Python requests 下载"""
        try:
            import requests
            response = requests.get(
                url, stream=True, timeout=self.timeout, verify=False
            )
            response.raise_for_status()
            
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return os.path.exists(output_path) and os.path.getsize(output_path) > 0
        except Exception as e:
            logger.debug(f"requests 下载失败: {e}")
            return False
    
    def cleanup(self):
        """清理临时文件"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
