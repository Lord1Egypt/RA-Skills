"""Skill 更新提醒模块 — 检查 GitHub 最新版本并提示用户"""

import json
import os
import re
import urllib.request
import urllib.error
from typing import Any, Dict, Optional, Tuple

from .logger import get_logger

logger = get_logger(__name__)

# GitHub 仓库信息（用于检查更新）
GITHUB_REPO = "njhskills/video-analyzer"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_TAGS_URL = f"https://api.github.com/repos/{GITHUB_REPO}/tags"

# 本地版本文件缓存
CACHE_FILE = ".update_cache.json"
CACHE_DURATION = 3600 * 6  # 缓存6小时


class UpdateNotifier:
    """检查 skill 是否有新版本发布"""
    
    def __init__(self, config: Dict[str, Any], current_version: str = "3.0.0"):
        self.config = config
        self.current_version = current_version
        self.cache_dir = config.get("processing", {}).get("cache_dir", ".cache")
        self.cache_path = os.path.join(self.cache_dir, CACHE_FILE)
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def check_for_updates(self, force: bool = False) -> Dict[str, Any]:
        """
        检查是否有新版本可用。
        
        返回:
            {
                "has_update": bool,
                "current_version": str,
                "latest_version": str,
                "release_url": str,
                "release_notes": str,
                "published_at": str,
                "error": str or None
            }
        """
        result = {
            "has_update": False,
            "current_version": self.current_version,
            "latest_version": None,
            "release_url": None,
            "release_notes": None,
            "published_at": None,
            "error": None,
        }
        
        # 检查缓存
        if not force:
            cached = self._read_cache()
            if cached:
                return cached
        
        try:
            latest = self._fetch_latest_release()
            if not latest:
                result["error"] = "无法获取最新版本信息（可能网络不可用）"
                return result
            
            latest_version = self._extract_version(latest.get("tag_name", ""))
            release_url = latest.get("html_url", f"https://github.com/{GITHUB_REPO}/releases")
            release_notes = latest.get("body", "无更新说明")
            published_at = latest.get("published_at", "")
            
            has_update = self._compare_versions(latest_version, self.current_version)
            
            result.update({
                "has_update": has_update,
                "latest_version": latest_version,
                "release_url": release_url,
                "release_notes": release_notes,
                "published_at": published_at,
            })
            
            # 写入缓存
            self._write_cache(result)
            
            if has_update:
                logger.info(f"🆕 发现新版本: v{latest_version}（当前: v{self.current_version}）")
            else:
                logger.info(f"✅ 当前已是最新版本 v{self.current_version}")
                
        except Exception as e:
            result["error"] = str(e)
            logger.debug(f"检查更新失败: {e}")
        
        return result
    
    def _fetch_latest_release(self) -> Optional[Dict]:
        """从 GitHub API 获取最新 release 信息"""
        try:
            req = urllib.request.Request(GITHUB_API_URL)
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("User-Agent", "video-analyzer-updater/3.0")
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # 无 release，尝试 tags
                return self._fetch_latest_tag()
            logger.debug(f"HTTP 错误: {e.code}")
        except Exception as e:
            logger.debug(f"请求失败: {e}")
        
        return None
    
    def _fetch_latest_tag(self) -> Optional[Dict]:
        """获取最新 tag 作为备选"""
        try:
            req = urllib.request.Request(GITHUB_TAGS_URL)
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("User-Agent", "video-analyzer-updater/3.0")
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    tags = json.loads(response.read().decode("utf-8"))
                    if tags:
                        latest = tags[0]
                        return {
                            "tag_name": latest.get("name", ""),
                            "html_url": f"https://github.com/{GITHUB_REPO}/releases",
                            "body": "请查看 GitHub 页面了解详情",
                            "published_at": "",
                        }
        except Exception as e:
            logger.debug(f"Tag 获取失败: {e}")
        
        return None
    
    def _extract_version(self, tag: str) -> str:
        """从 tag 中提取版本号"""
        if not tag:
            return self.current_version
        
        # 支持 v1.0.0 或 1.0.0
        match = re.search(r'v?(\d+\.\d+\.\d+)', tag)
        if match:
            return match.group(1)
        return self.current_version
    
    def _compare_versions(self, latest: str, current: str) -> bool:
        """
        比较版本号，返回 True 表示有新版本。
        支持格式: X.Y.Z
        """
        try:
            def parse_ver(v):
                parts = []
                for p in v.split("."):
                    # 只取数字部分
                    m = re.search(r'(\d+)', p)
                    if m:
                        parts.append(int(m.group(1)))
                return parts + [0] * (3 - len(parts))
            
            latest_parts = parse_ver(latest)
            current_parts = parse_ver(current)
            
            return latest_parts > current_parts
        except Exception:
            return False
    
    def _read_cache(self) -> Optional[Dict]:
        """读取缓存结果"""
        try:
            if not os.path.exists(self.cache_path):
                return None
            
            with open(self.cache_path, "r") as f:
                cache = json.load(f)
            
            # 检查缓存是否过期
            cached_time = cache.get("_cached_at", 0)
            import time
            if time.time() - cached_time > CACHE_DURATION:
                return None
            
            return cache.get("result")
        except Exception:
            return None
    
    def _write_cache(self, result: Dict):
        """写入缓存"""
        try:
            import time
            cache = {
                "_cached_at": time.time(),
                "result": result,
            }
            with open(self.cache_path, "w") as f:
                json.dump(cache, f)
        except Exception:
            pass
    
    def format_update_message(self, check_result: Dict) -> str:
        """格式化更新提醒消息"""
        if not check_result.get("has_update"):
            return ""
        
        latest = check_result.get("latest_version", "?")
        current = check_result.get("current_version", "?")
        url = check_result.get("release_url", "")
        notes = check_result.get("release_notes", "")[:500]
        
        lines = [
            "",
            "=" * 50,
            "🆕 发现新版本！",
            f"   当前版本: v{current}",
            f"   最新版本: v{latest}",
            f"   下载地址: {url}",
            "",
            "📝 更新内容:",
        ]
        
        if notes:
            # 截取前500字符
            for line in notes.split("\n")[:15]:
                lines.append(f"   {line}")
        
        lines.extend([
            "",
            "   请尽快更新以获得最新功能和优化！",
            "=" * 50,
            "",
        ])
        
        return "\n".join(lines)
