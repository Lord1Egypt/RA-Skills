"""图文笔记 — 批量并发下载图片，流式 + 大小限制。"""

from __future__ import annotations
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# 默认单张图片上限（防恶意大图 DoS）
DEFAULT_MAX_IMAGE_BYTES = 30 * 1024 * 1024  # 30 MB
DEFAULT_MAX_WORKERS = 4
_VALID_EXTS = {"jpg", "jpeg", "png", "webp", "gif"}


def download_images(
    urls: list[str],
    outdir: Path,
    timeout: int = 30,
    max_bytes: int = DEFAULT_MAX_IMAGE_BYTES,
    max_workers: int = DEFAULT_MAX_WORKERS,
) -> list[Path]:
    """并发下载图片到 outdir/image_NNN.{ext}。

    单张失败不阻塞整体（其他继续下载）；返回成功保存的本地路径列表。
    保留 urls 顺序对应的索引：image_001.jpg ↔ urls[0]。

    Args:
        urls: 图片 URL 列表
        outdir: 输出目录
        timeout: 单张请求超时
        max_bytes: 单张最大字节数（超限丢弃）
        max_workers: 并发线程数

    Returns:
        成功保存的本地文件路径列表（按 urls 原序）。
    """
    outdir.mkdir(parents=True, exist_ok=True)
    saved: dict[int, Path] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {
            ex.submit(_download_one, url, outdir, idx, timeout, max_bytes): idx
            for idx, url in enumerate(urls, start=1)
        }
        for fut in as_completed(futures):
            idx = futures[fut]
            try:
                result = fut.result()
            except Exception as e:
                print(f"  ⚠️ image_{idx:03d} download failed: {e}")
                continue
            if result is not None:
                saved[idx] = result

    return [saved[i] for i in sorted(saved)]


def _download_one(
    url: str,
    outdir: Path,
    idx: int,
    timeout: int,
    max_bytes: int,
) -> Path | None:
    """下载单张图片（流式 + 大小校验）。"""
    ext = _guess_extension(url)
    dest = outdir / f"image_{idx:03d}.{ext}"
    written = 0
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp, dest.open("wb") as f:
            while True:
                chunk = resp.read(64 * 1024)
                if not chunk:
                    break
                written += len(chunk)
                if written > max_bytes:
                    f.close()
                    dest.unlink(missing_ok=True)
                    raise RuntimeError(
                        f"exceeded {max_bytes // (1024*1024)} MB"
                    )
                f.write(chunk)
        return dest
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as e:
        # 失败时清理半成品
        dest.unlink(missing_ok=True)
        raise


def _guess_extension(url: str) -> str:
    """从 URL 路径段提取文件扩展名（去掉 query string）。

    例:
      https://x.com/a/b.png?token=xxx          → png
      https://x.com/img?ext=jpg                → jpg（兜底，路径无扩展名时）
      https://x.com/uuid                       → jpg（默认）
      https://x.com/a.com_thumb.jpg.webp       → webp（取最后一段）
    """
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    # 取路径最后一段的最后一个 . 之后
    segment = path.rsplit("/", 1)[-1]
    if "." in segment:
        ext = segment.rsplit(".", 1)[-1]
        if ext in _VALID_EXTS:
            return "jpg" if ext == "jpeg" else ext
    return "jpg"  # 默认
