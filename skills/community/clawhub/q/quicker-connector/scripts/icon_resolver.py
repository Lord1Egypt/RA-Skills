#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quicker 动作图标解析器：把 CSV「图标」列的取值解析成真实的 PNG 图片文件。

支持三类取值：
1. https://...png        —— Quicker 云端图标。优先命中 Quicker 本地缓存
   （%LOCALAPPDATA%\\Quicker\\ImageCache\\<SHA1(完整URL)大写>.png，完全离线），
   未命中再联网下载并缓存。
2. fa:Style_Name[:#AARRGGBB] —— FontAwesome 字体图标（Style: Solid/Regular/Light/Brands，
   #AARRGGBB 为可选颜色）。用 Quicker 自带的 FontAwesome5 SVG 数据 + 纯 Python
   栅格化渲染成 PNG。
3. 本地文件路径 / 空值     —— 直接使用 / 返回 None。

批量解析用 `resolve_many()`：先去重 + 本地缓存快速命中（不进线程池），
只有真正需要下载/渲染的取值才走 ThreadPoolExecutor 并发。
单条 `resolve()` 的行为（返回值、stats 语义）保持不变。
"""
from __future__ import annotations

import hashlib
import os
import re
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from svg_raster import render_icon, render_svg
import fa_icons

DEFAULT_IMAGE_CACHE = Path(os.environ.get("LOCALAPPDATA", "")) / "Quicker" / "ImageCache"
DEFAULT_COLOR = (0x00, 0x00, 0x00, 0xFF)  # Quicker 默认字体图标颜色（黑）
DEFAULT_MAX_WORKERS = 8

_FA_RE = re.compile(r"^fa:([A-Za-z]+)_(.+?)(?::#([0-9A-Fa-f]{8}))?$")
_LOCAL_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico")

# kind 取值：描述一次解析最终走的是哪条路径
KIND_URL_CACHE = "url_cache"        # URL 图标命中本地缓存（技能缓存或 Quicker ImageCache）
KIND_URL_DOWNLOAD = "url_download"  # URL 图标联网下载
KIND_FA_CACHE = "fa_cache"          # fa: 字体图标命中已渲染缓存
KIND_FA_RENDER = "fa_render"        # fa: 字体图标本次真正栅格化渲染
KIND_LOCAL_FILE = "local_file"      # 图标取值本身就是本地图片路径
KIND_MISS = "miss"                  # 无法解析


def _is_svg(data: bytes) -> bool:
    head = data[:256]
    head = head.lstrip(b"\xef\xbb\xbf\xff\xfe\x00 \t\r\n")  # 去 BOM
    return head.startswith(b"<") and b"<svg" in head.lower()


class IconResolver:
    """图标取值 -> 本地 PNG 文件路径"""

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        quicker_image_cache: Optional[str] = None,
        size: int = 48,
        timeout: int = 15,
        log: Optional[Callable[[str], None]] = None,
        max_workers: int = DEFAULT_MAX_WORKERS,
    ):
        """
        Args:
            cache_dir: 技能自己的 PNG 缓存目录（默认 <技能>/.cache/icons）
            quicker_image_cache: Quicker 本地 ImageCache 目录
            size: 输出图标像素尺寸
            timeout: 单个网络请求超时（秒）
            log: 日志回调
            max_workers: resolve_many() 默认并发线程数
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Path(__file__).resolve().parent.parent / ".cache" / "icons"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.image_cache = Path(quicker_image_cache) if quicker_image_cache else DEFAULT_IMAGE_CACHE
        self.size = size
        self.timeout = timeout
        self.log = log or (lambda msg: None)
        self.max_workers = max(1, int(max_workers))
        self._lock = threading.Lock()
        # stats：单次/累计混合计数（语义与旧版一致），额外提供 reused / elapsed_sec
        self.stats: Dict[str, Any] = {
            "url_cache": 0,
            "url_download": 0,
            "fa_render": 0,
            "miss": 0,
            "local_file": 0,
            "reused": 0,          # 去重复用计数（同一取值被重复请求而不再解析的次数）
            "elapsed_sec": 0.0,   # 累计批量解析（resolve_many）耗时
        }
        # 每个取值最后一次解析的结果明细：{取值: {"value","kind","path"}}
        self.records: Dict[str, Dict[str, Any]] = {}

    # ---------- 内部工具 ----------
    def _inc(self, key: str, n: int = 1) -> None:
        """线程安全地累加统计计数"""
        with self._lock:
            self.stats[key] = self.stats.get(key, 0) + n

    def _record(self, value: str, kind: str, path: Optional[str]) -> None:
        """记录某个取值的解析明细（供上层做来源统计与清单）"""
        with self._lock:
            self.records[value] = {"value": value, "kind": kind, "path": path}

    @staticmethod
    def _ok(path: Path) -> bool:
        """缓存文件存在且非空即为可用"""
        try:
            return path.exists() and path.stat().st_size > 0
        except OSError:
            return False

    @staticmethod
    def _url_key(url: str) -> str:
        """Quicker ImageCache 文件名规则：SHA1(完整URL) 大写"""
        return hashlib.sha1(url.encode("utf-8")).hexdigest().upper()

    def _url_target(self, url: str) -> Path:
        """URL 图标在技能缓存中的目标文件"""
        return self.cache_dir / "url" / f"{self._url_key(url)}.png"

    def _fa_target(self, value: str) -> Optional[Path]:
        """fa: 取值对应的缓存文件；写法非法返回 None"""
        m = _FA_RE.match(value)
        if not m:
            return None
        style, name, color_hex = m.group(1), m.group(2), m.group(3)
        return self.cache_dir / "fa" / f"{style}_{name}_{self.size}_{color_hex or 'default'}.png"

    # ---------- 对外：单条 ----------
    def resolve(self, icon_value: str) -> Optional[str]:
        """返回 PNG 文件路径；无法解析返回 None"""
        v = (icon_value or "").strip()
        if not v:
            self._inc("miss")
            self._record(v, KIND_MISS, None)
            return None

        try:
            if v.lower().startswith(("http://", "https://")):
                return self._resolve_url(v)
            if v.lower().startswith("fa:"):
                return self._resolve_fa(v)
            # 本地文件
            p = Path(v)
            if p.exists() and p.suffix.lower() in _LOCAL_EXTS:
                self._inc("local_file")
                self._record(v, KIND_LOCAL_FILE, str(p))
                return str(p)
        except Exception as e:  # 单个图标失败不影响整体导出
            self.log(f"图标解析失败 {v[:60]}: {e}")
        self._inc("miss")
        self._record(v, KIND_MISS, None)
        return None

    # ---------- 对外：批量并发 ----------
    def try_local(self, icon_value: str) -> Tuple[bool, Optional[str]]:
        """
        本地快速通道：只做缓存命中判定，不联网、不渲染。

        Returns:
            (是否已本地解决, PNG 路径或 None)。False 表示需要走 resolve() 真正干活。
        """
        v = (icon_value or "").strip()

        # URL 图标：技能缓存已有 → 直接复用；Quicker ImageCache 命中也判定为"本地可解决"
        if v.lower().startswith(("http://", "https://")):
            target = self._url_target(v)
            if self._ok(target):
                self._inc("url_cache")
                self._record(v, KIND_URL_CACHE, str(target))
                return True, str(target)
            local = self.image_cache / f"{self._url_key(v)}.png"
            if self._ok(local):
                data = local.read_bytes()
                if not _is_svg(data):
                    # 本地已有原始 PNG：只需落一份到技能缓存，无需下载
                    try:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(data)
                        self._inc("url_cache")
                        self._record(v, KIND_URL_CACHE, str(target))
                        return True, str(target)
                    except Exception as e:
                        self.log(f"本地缓存复制失败 {v[:60]}: {e}")
            return False, None

        # 字体图标：已渲染过 → 直接复用
        if v.lower().startswith("fa:"):
            cache_file = self._fa_target(v)
            if cache_file is None:
                return False, None  # 写法非法，交给 resolve() 统一报错
            if self._ok(cache_file):
                self._inc("fa_render")  # 与旧版统计口径一致（缓存命中也算 fa_render）
                self._record(v, KIND_FA_CACHE, str(cache_file))
                return True, str(cache_file)
            return False, None

        # 空值
        if not v:
            self._inc("miss")
            self._record(v, KIND_MISS, None)
            return True, None

        # 本地图片路径
        p = Path(v)
        if p.exists() and p.suffix.lower() in _LOCAL_EXTS:
            self._inc("local_file")
            self._record(v, KIND_LOCAL_FILE, str(p))
            return True, str(p)
        return False, None

    def resolve_many(
        self,
        values: Iterable[str],
        max_workers: Optional[int] = None,
    ) -> Dict[str, Optional[str]]:
        """
        批量并发解析图标取值。

        流程：去重（重复项计入 reused）→ 本地缓存快速命中（不进线程池）
        → 剩余需要下载/渲染的取值丢进线程池并发 → 汇总为 {取值: PNG路径}。

        Args:
            values: 图标取值可迭代对象（可含重复）
            max_workers: 并发线程数，None 时用 self.max_workers

        Returns:
            {图标取值: PNG 路径或 None}，key 为 strip 后的取值
        """
        t0 = time.perf_counter()
        workers = max(1, int(max_workers or self.max_workers))

        # 1) 去重（保持首次出现顺序）
        unique: List[str] = []
        seen = set()
        for v in values:
            key = (v or "").strip()
            if key in seen:
                self._inc("reused")
                continue
            seen.add(key)
            unique.append(key)

        # 2) 本地快速通道
        results: Dict[str, Optional[str]] = {}
        pending: List[str] = []
        for key in unique:
            handled, path = self.try_local(key)
            if handled:
                results[key] = path
            else:
                pending.append(key)

        # 3) 需要下载/渲染的才并发
        if pending:
            if workers == 1 or len(pending) == 1:
                for key in pending:
                    results[key] = self.resolve(key)
            else:
                with ThreadPoolExecutor(max_workers=min(workers, len(pending))) as pool:
                    futures = {pool.submit(self.resolve, key): key for key in pending}
                    for fut, key in futures.items():
                        try:
                            results[key] = fut.result()
                        except Exception as e:  # 单条失败不影响整体
                            self.log(f"并发解析失败 {key[:60]}: {e}")
                            results[key] = None

        dt = time.perf_counter() - t0
        with self._lock:
            self.stats["elapsed_sec"] = round(self.stats.get("elapsed_sec", 0.0) + dt, 3)
        return results

    def kind_of(self, icon_value: str) -> Optional[str]:
        """查询某个取值的来源类型（KIND_* 之一），未解析过返回 None"""
        key = (icon_value or "").strip()
        rec = self.records.get(key)
        return rec["kind"] if rec else None

    # ---------- URL 图标 ----------
    def _resolve_url(self, url: str) -> Optional[str]:
        target = self._url_target(url)
        if self._ok(target):
            # 我们自己的缓存只存规范化后的 PNG
            self._inc("url_cache")
            self._record(url, KIND_URL_CACHE, str(target))
            return str(target)

        # 数据来源：优先 Quicker 本地缓存（离线），其次联网下载
        data = None
        from_local = False
        local = self.image_cache / f"{self._url_key(url)}.png"
        if self._ok(local):
            data = local.read_bytes()
            from_local = True
            self._inc("url_cache")
        if data is None:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 QuickerConnector"})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = resp.read()
            if not data:
                raise ValueError("空响应")
            self._inc("url_download")

        target.parent.mkdir(parents=True, exist_ok=True)
        if _is_svg(data):
            # SVG 图标（如 *_icons/<hash>.svg）栅格化成 PNG
            render_svg(data.decode("utf-8", "replace"), size=self.size).save(target, "PNG")
        else:
            from PIL import Image as _PILImage
            from io import BytesIO as _BytesIO
            with _PILImage.open(_BytesIO(data)) as im:  # 校验是有效图片
                im.load()
            target.write_bytes(data)

        self._record(url, KIND_URL_CACHE if from_local else KIND_URL_DOWNLOAD, str(target))
        return str(target)

    # ---------- FontAwesome 字体图标 ----------
    def _resolve_fa(self, value: str) -> Optional[str]:
        m = _FA_RE.match(value)
        if not m:
            raise ValueError(f"无法解析的字体图标写法: {value}")
        style, name, color_hex = m.group(1), m.group(2), m.group(3)
        key = f"{style}_{name}"

        color = DEFAULT_COLOR
        if color_hex:
            a = int(color_hex[0:2], 16)
            r = int(color_hex[2:4], 16)
            g = int(color_hex[4:6], 16)
            b = int(color_hex[6:8], 16)
            color = (r, g, b, a)

        cache_file = self._fa_target(value)
        if cache_file is not None and self._ok(cache_file):
            self._inc("fa_render")
            self._record(value, KIND_FA_CACHE, str(cache_file))
            return str(cache_file)

        data = fa_icons.get(key)
        if not data:
            self.log(f"字体图标缺失: {key}")
            self._inc("miss")
            self._record(value, KIND_MISS, None)
            return None

        path_d, w, h = data
        img = render_icon(path_d, w, h, size=self.size, color=color)
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        img.save(cache_file)
        self._inc("fa_render")
        self._record(value, KIND_FA_RENDER, str(cache_file))
        return str(cache_file)
