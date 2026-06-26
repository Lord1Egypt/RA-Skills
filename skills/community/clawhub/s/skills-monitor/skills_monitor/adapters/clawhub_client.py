"""
ClawHub 社区数据采集器 v0.5.0 — 公共 Skill 注册库数据获取
========================================================
从 ClawHub (clawhub.ai) 获取 Skill 的社区元数据:
  - 下载量 (installs)
  - 星标数 (stars)
  - 安全扫描结果
  - 标签/分类
  - 更新时间

由于 ClawHub 无官方 REST API，本模块使用:
  - 优先: 尝试内部 API 端点 (JSON 响应)
  - 降级: 本地维护的热门 Skills 缓存文件

使用方式:
  from skills_monitor.adapters.clawhub_client import ClawHubClient
  client = ClawHubClient()
  meta = client.get_skill_metadata("a-share-short-decision")
  popular = client.get_popular_skills(category="finance", limit=20)
"""

import json
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ClawHub 配置
CLAWHUB_BASE_URL = "https://clawhub.ai"
CLAWHUB_API_BASE = f"{CLAWHUB_BASE_URL}/api"      # 猜测的 API 路径
CLAWHUB_REGISTRY_URL = f"{CLAWHUB_BASE_URL}/registry"

# 缓存配置
CACHE_DIR = os.path.expanduser("~/.skills_monitor/clawhub_cache")
CACHE_TTL_HOURS = 24    # 缓存有效期 24 小时
POPULAR_CACHE_FILE = "popular_skills.json"
METADATA_CACHE_FILE = "skill_metadata.json"

# 本地降级数据
LOCAL_FALLBACK_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data", "clawhub_popular_fallback.json",
)

# 请求配置
REQUEST_TIMEOUT = 15
MAX_RETRIES = 2
RATE_LIMIT_DELAY = 0.5   # 请求间隔（秒）


class ClawHubClient:
    """
    ClawHub 社区数据采集器

    数据获取优先级:
      1. 本地缓存 (< 24h)
      2. ClawHub API / 网页请求
      3. 本地降级 JSON 文件
    """

    def __init__(
        self,
        base_url: str = CLAWHUB_BASE_URL,
        cache_ttl_hours: int = CACHE_TTL_HOURS,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_base = f"{self.base_url}/api"
        self.cache_ttl = timedelta(hours=cache_ttl_hours)

        # 确保缓存目录
        Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

        # 加载缓存
        self._metadata_cache: Dict[str, Dict] = self._load_cache(METADATA_CACHE_FILE)
        self._popular_cache: Dict[str, Any] = self._load_cache(POPULAR_CACHE_FILE)

        # 请求会话
        self._session = None
        self._last_request_time = 0.0

    # ──────── 公开 API ────────

    def get_skill_metadata(self, slug: str) -> Dict[str, Any]:
        """
        获取单个 Skill 的社区元数据

        Args:
            slug: Skill 的 slug (e.g. "a-share-short-decision")

        Returns:
            {
                "slug": "...",
                "installs": 1234,
                "stars": 56,
                "star_density": 0.045,  # stars / installs
                "tags": ["finance", "stock"],
                "security_score": "A",
                "last_updated": "2026-03-10",
                "source": "api" | "cache" | "fallback",
            }
        """
        # 1. 检查缓存
        cached = self._get_cached_metadata(slug)
        if cached:
            cached["source"] = "cache"
            return cached

        # 2. 尝试在线获取
        online = self._fetch_skill_metadata_online(slug)
        if online:
            online["source"] = "api"
            self._cache_metadata(slug, online)
            return online

        # 3. 降级到本地文件
        fallback = self._get_fallback_metadata(slug)
        if fallback:
            fallback["source"] = "fallback"
            return fallback

        # 4. 无数据
        return {
            "slug": slug,
            "installs": None,
            "stars": None,
            "star_density": None,
            "tags": [],
            "security_score": None,
            "last_updated": None,
            "source": "none",
        }

    def get_popular_skills(
        self,
        category: str = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        获取热门 Skills 排行

        Args:
            category: 按分类过滤 (可选)
            limit: 返回数量上限

        Returns:
            [{"slug": ..., "installs": ..., "stars": ..., ...}, ...]
        """
        # 1. 检查缓存
        cache_key = f"popular_{category or 'all'}"
        if cache_key in self._popular_cache:
            cached = self._popular_cache[cache_key]
            if self._is_cache_valid(cached.get("cached_at")):
                skills = cached.get("skills", [])
                return skills[:limit]

        # 2. 尝试在线获取
        skills = self._fetch_popular_online(category)
        if skills:
            self._popular_cache[cache_key] = {
                "skills": skills,
                "cached_at": datetime.now().isoformat(),
            }
            self._save_cache(POPULAR_CACHE_FILE, self._popular_cache)
            return skills[:limit]

        # 3. 降级到本地
        fallback = self._load_fallback()
        if fallback:
            skills = fallback
            if category:
                skills = [s for s in skills if category in s.get("tags", [])]
            return skills[:limit]

        return []

    def batch_fetch(self, slugs: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        批量获取多个 Skill 的元数据

        Args:
            slugs: Skill slug 列表

        Returns:
            {slug: metadata_dict, ...}
        """
        results = {}
        for slug in slugs:
            results[slug] = self.get_skill_metadata(slug)
            # 限流
            time.sleep(RATE_LIMIT_DELAY)
        return results

    def get_community_scores(self, slug: str) -> Dict[str, Optional[float]]:
        """
        获取 Skill 的社区评分指标（用于评分引擎）

        Returns:
            {
                "community_popularity": 0.0-1.0 (对数归一化下载量),
                "community_rating": 0.0-1.0 (star density 归一化),
            }
        """
        meta = self.get_skill_metadata(slug)

        popularity = None
        rating = None

        installs = meta.get("installs")
        stars = meta.get("stars")

        if installs is not None and installs > 0:
            import math
            # 对数归一化: log10(installs) / log10(max_expected_installs)
            # 假设最大下载量 100 万
            popularity = min(1.0, math.log10(max(installs, 1)) / 6.0)

        if stars is not None and installs and installs > 0:
            # star density 归一化: star_density / max_expected_density
            # 假设最高 density 0.2 (20% 用户给了 star)
            density = stars / installs
            rating = min(1.0, density / 0.2)

        return {
            "community_popularity": round(popularity, 4) if popularity is not None else None,
            "community_rating": round(rating, 4) if rating is not None else None,
            "source": meta.get("source", "none"),
        }

    # ──────── 在线获取 ────────

    def _fetch_skill_metadata_online(self, slug: str) -> Optional[Dict[str, Any]]:
        """尝试从 ClawHub 在线获取 Skill 元数据"""
        session = self._get_session()

        # 尝试多个可能的 API 端点
        endpoints = [
            f"{self.api_base}/v1/skills/{slug}",
            f"{self.api_base}/skills/{slug}",
            f"{self.api_base}/v1/registry/{slug}",
        ]

        for url in endpoints:
            try:
                self._rate_limit()
                resp = session.get(url, timeout=REQUEST_TIMEOUT)
                if resp.status_code == 200:
                    data = resp.json()
                    return self._normalize_metadata(slug, data)
            except Exception as e:
                logger.debug(f"ClawHub API 请求失败 [{url}]: {e}")
                continue

        # 尝试从公开页面解析
        return self._scrape_skill_page(slug)

    def _scrape_skill_page(self, slug: str) -> Optional[Dict[str, Any]]:
        """从 ClawHub 公开页面提取数据（降级方案）"""
        session = self._get_session()
        url = f"{self.base_url}/skills/{slug}"

        try:
            self._rate_limit()
            resp = session.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                return None

            # 简单的 JSON-LD / meta 标签解析
            # ClawHub 页面可能在 script 标签中包含 JSON 数据
            text = resp.text
            return self._parse_page_data(slug, text)

        except Exception as e:
            logger.debug(f"ClawHub 页面抓取失败 [{slug}]: {e}")
            return None

    def _parse_page_data(self, slug: str, html: str) -> Optional[Dict[str, Any]]:
        """从 HTML 页面中提取结构化数据"""
        import re

        metadata = {
            "slug": slug,
            "installs": None,
            "stars": None,
            "tags": [],
            "security_score": None,
            "last_updated": None,
        }

        # 尝试从 script[type="application/json"] 或 __NEXT_DATA__ 中提取
        patterns = [
            r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>',
            r'"installs?[Cc]ount?":\s*(\d+)',
            r'"stars?":\s*(\d+)',
            r'"downloads?":\s*(\d+)',
        ]

        # 提取 installs
        match = re.search(r'"(?:installs?|downloads?)[Cc]?ount?":\s*(\d+)', html)
        if match:
            metadata["installs"] = int(match.group(1))

        # 提取 stars
        match = re.search(r'"stars?":\s*(\d+)', html)
        if match:
            metadata["stars"] = int(match.group(1))

        # 提取 tags
        tag_matches = re.findall(r'"tags?":\s*\[(.*?)\]', html)
        if tag_matches:
            try:
                tags_str = tag_matches[0]
                metadata["tags"] = [t.strip().strip('"\'') for t in tags_str.split(",") if t.strip()]
            except Exception:
                pass

        # 如果至少获取到一个有效字段
        if metadata["installs"] is not None or metadata["stars"] is not None:
            if metadata["installs"] and metadata["stars"]:
                metadata["star_density"] = round(metadata["stars"] / metadata["installs"], 4)
            return metadata

        return None

    def _fetch_popular_online(self, category: str = None) -> Optional[List[Dict[str, Any]]]:
        """在线获取热门 Skills 列表"""
        session = self._get_session()

        params = {"sort": "popular", "limit": 100}
        if category:
            params["category"] = category

        endpoints = [
            f"{self.api_base}/v1/skills",
            f"{self.api_base}/skills",
            f"{self.api_base}/v1/registry",
        ]

        for url in endpoints:
            try:
                self._rate_limit()
                resp = session.get(url, params=params, timeout=REQUEST_TIMEOUT)
                if resp.status_code == 200:
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get("items", data.get("skills", []))
                    return [self._normalize_metadata(s.get("slug", s.get("id", "")), s) for s in items]
            except Exception as e:
                logger.debug(f"ClawHub 热门列表请求失败 [{url}]: {e}")
                continue

        return None

    # ──────── 数据标准化 ────────

    def _normalize_metadata(self, slug: str, raw: Dict) -> Dict[str, Any]:
        """将不同来源的数据标准化为统一格式"""
        installs = (
            raw.get("installs") or raw.get("installCount") or
            raw.get("downloads") or raw.get("downloadCount") or 0
        )
        stars = raw.get("stars") or raw.get("starCount") or raw.get("favorites") or 0

        tags = raw.get("tags") or raw.get("categories") or raw.get("labels") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        return {
            "slug": slug,
            "name": raw.get("name") or raw.get("title") or slug,
            "installs": int(installs) if installs else 0,
            "stars": int(stars) if stars else 0,
            "star_density": round(int(stars) / max(int(installs), 1), 4) if installs else 0.0,
            "tags": tags,
            "security_score": raw.get("securityScore") or raw.get("security_grade"),
            "last_updated": raw.get("updatedAt") or raw.get("updated_at") or raw.get("lastPublished"),
            "description": (raw.get("description") or "")[:200],
            "author": raw.get("author") or raw.get("publisher") or raw.get("owner"),
        }

    # ──────── 缓存管理 ────────

    def _load_cache(self, filename: str) -> Dict:
        """加载缓存文件"""
        filepath = os.path.join(CACHE_DIR, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_cache(self, filename: str, data: Dict):
        """保存缓存文件"""
        filepath = os.path.join(CACHE_DIR, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存缓存失败: {e}")

    def _get_cached_metadata(self, slug: str) -> Optional[Dict]:
        """获取缓存的元数据"""
        entry = self._metadata_cache.get(slug)
        if entry and self._is_cache_valid(entry.get("cached_at")):
            return entry.get("data")
        return None

    def _cache_metadata(self, slug: str, data: Dict):
        """缓存元数据"""
        self._metadata_cache[slug] = {
            "data": data,
            "cached_at": datetime.now().isoformat(),
        }
        self._save_cache(METADATA_CACHE_FILE, self._metadata_cache)

    def _is_cache_valid(self, cached_at: Optional[str]) -> bool:
        """检查缓存是否有效"""
        if not cached_at:
            return False
        try:
            ct = datetime.fromisoformat(cached_at)
            return datetime.now() - ct < self.cache_ttl
        except (ValueError, TypeError):
            return False

    # ──────── 降级数据 ────────

    def _load_fallback(self) -> Optional[List[Dict]]:
        """加载本地降级数据"""
        try:
            if os.path.exists(LOCAL_FALLBACK_FILE):
                with open(LOCAL_FALLBACK_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    def _get_fallback_metadata(self, slug: str) -> Optional[Dict]:
        """从降级数据中查找特定 Skill"""
        fallback = self._load_fallback()
        if fallback:
            for skill in fallback:
                if skill.get("slug") == slug:
                    return skill
        return None

    # ──────── HTTP 会话 ────────

    def _get_session(self):
        """获取 requests 会话（懒加载）"""
        if self._session is None:
            import requests
            self._session = requests.Session()
            self._session.headers.update({
                "User-Agent": "SkillsMonitor/0.5.0",
                "Accept": "application/json, text/html",
            })
        return self._session

    def _rate_limit(self):
        """简单限流"""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - elapsed)
        self._last_request_time = time.time()

    # ──────── 清理 ────────

    def clear_cache(self):
        """清空所有缓存"""
        self._metadata_cache = {}
        self._popular_cache = {}
        for f in (METADATA_CACHE_FILE, POPULAR_CACHE_FILE):
            try:
                os.remove(os.path.join(CACHE_DIR, f))
            except FileNotFoundError:
                pass

    def close(self):
        """关闭 HTTP 会话"""
        if self._session:
            self._session.close()
            self._session = None
