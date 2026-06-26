#!/usr/bin/env python3
"""
将本地 PDF 转为 Markdown，
并把文中的图片 URL 下载到本地，将 ![](url) 替换为相对路径引用。
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import base64
import requests

# --------------------------------------------------------------------------- #
# Session
# --------------------------------------------------------------------------- #

_API_BASE = os.environ.get("WPS_API_BASE") or "https://api.wps.cn"


def _resolve_sid() -> str:
    sid = (
        os.environ.get("TMP_LX_UUID")
        or os.environ.get("wps_sid")
        or os.environ.get("WPS_SID")
    )
    if not sid:
        raise SystemExit("缺少认证凭证：未设置环境变量 TMP_LX_UUID / wps_sid / WPS_SID")
    return sid


class _Session:
    _HDR = {
        "Origin": "https://365.kdocs.cn",
        "Referer": "https://365.kdocs.cn/",
    }

    def __init__(self, sid: str):
        self._http = requests.Session()
        self._http.cookies.set("wps_sid", sid)
        self._http.cookies.set("csrf", sid)
        self._http.headers.update(self._HDR)

    def post_multipart(
        self,
        url: str,
        files: dict,
        data: Optional[dict] = None,
        timeout: int = 300,
    ) -> requests.Response:
        return self._http.post(url, files=files, data=data, timeout=timeout)

    def get_bytes(self, url: str, timeout: int = 120) -> bytes:
        r = self._http.get(url, timeout=timeout, stream=True)
        r.raise_for_status()
        return r.content


# --------------------------------------------------------------------------- #
# 核心逻辑
# --------------------------------------------------------------------------- #

_KS3_INTERNAL = "ks3-cn-beijing-internal"
_KS3_PUBLIC = "ks3-cn-beijing"

# 匹配 ![alt](src)，src 可能很长（data URI），用非贪婪匹配括号内全部内容
_MD_IMG = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)", re.DOTALL)

# data URI：data:image/jpeg;base64,....
_DATA_URI = re.compile(r"^data:image/(\w+);base64,(.+)$", re.DOTALL)


def _public_url(url: str) -> str:
    """内网 KS3 地址 → 公网地址（与 cooffice/tools/parse_document.py 一致）"""
    if _KS3_INTERNAL in url:
        return url.replace(_KS3_INTERNAL, _KS3_PUBLIC)
    return url


def _is_http(u: str) -> bool:
    return u.startswith("http://") or u.startswith("https://")


def _decode_data_uri(data_uri: str) -> tuple[bytes, str]:
    """解析 data:image/xxx;base64,... → (bytes, ext)"""
    m = _DATA_URI.match(data_uri.strip())
    if not m:
        raise ValueError("无效的 data URI")
    fmt, b64 = m.group(1).lower(), m.group(2).strip()
    ext = ".jpg" if fmt in ("jpeg", "jpg") else f".{fmt}"
    return base64.b64decode(b64), ext


def export_and_localize(
    pdf_path: Path,
    out_md: Path,
    images_subdir: str = "images",
    sid: Optional[str] = None,
) -> Path:
    pdf_path = pdf_path.resolve()
    if not pdf_path.is_file():
        raise FileNotFoundError(pdf_path)

    session = _Session(sid or _resolve_sid())

    name = pdf_path.name
    content = pdf_path.read_bytes()

    resp = session.post_multipart(
        f"{_API_BASE}/v7/longtask/exporter/export_file_content",
        files={"form_file": (name, content, "application/pdf")},
        data={"format": "markdown", "include_elements": "all", "filename": name},
    )
    resp.raise_for_status()
    body = resp.json()
    if body.get("code") != 0:
        raise RuntimeError(f"API 错误: {body}")

    md_text = (body.get("data") or {}).get("markdown")
    if md_text is None:
        raise RuntimeError("响应中无 data.markdown")

    out_md = out_md.resolve()
    out_dir = out_md.parent
    img_dir = out_dir / images_subdir
    out_dir.mkdir(parents=True, exist_ok=True)

    seq = [1]

    def replacer(m: re.Match) -> str:
        alt, raw = m.group(1), m.group(2).strip()
        idx = seq[0]
        seq[0] += 1
        dest_parent = img_dir
        dest_parent.mkdir(parents=True, exist_ok=True)

        if raw.startswith("data:image/"):
            # base64 data URI → 直接解码写文件
            try:
                img_bytes, ext = _decode_data_uri(raw)
            except Exception as e:
                raise RuntimeError(f"base64 解码失败（img_{idx:03d}）: {e}") from e
            local_name = f"img_{idx:03d}{ext}"
            (dest_parent / local_name).write_bytes(img_bytes)
        elif _is_http(raw):
            # HTTP URL → 替换内网 host 后下载
            suf = Path(urlparse(raw).path).suffix.lower()
            ext = suf if suf in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp") else ".jpg"
            local_name = f"img_{idx:03d}{ext}"
            try:
                (dest_parent / local_name).write_bytes(session.get_bytes(_public_url(raw)))
            except Exception as e:
                raise RuntimeError(f"下载图片失败: {raw}\n{e}") from e
        else:
            # 已是本地路径或其他格式，保持不动
            seq[0] -= 1
            return m.group(0)

        abs_path = str((dest_parent / local_name).resolve()).replace("\\", "/")
        return f"![{alt}]({abs_path})"

    out_md.write_text(_MD_IMG.sub(replacer, md_text), encoding="utf-8")
    return out_md


# --------------------------------------------------------------------------- #
# 对外接口
# --------------------------------------------------------------------------- #

def parse(pdf_path: str | Path, output_path: str | Path) -> None:
    """将 PDF 转为 Markdown，结果写到 output_path/content.md，图片写到 output_path/images/。"""
    pdf = Path(pdf_path).resolve()
    out_dir = Path(output_path).resolve()
    out_md = out_dir / "content.md"

    export_and_localize(pdf, out_md, images_subdir="images")

    img_dir = out_dir / "images"
    imgs = sorted(img_dir.glob("img_*")) if img_dir.exists() else []

    print(f"成功解析 {pdf.name} 文件\n\n")
    print(f"Markdown 文件路径：{out_md}\n\n")
    if imgs:
        suffixes = sorted({i.suffix for i in imgs})
        suffix_str = "/".join(s.lstrip(".") for s in suffixes)
        print(f"图片文件路径：{img_dir}（共 {len(imgs)} 张，格式 img_NNN.{suffix_str}）")
    else:
        print("图片文件：无")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main() -> None:
    p = argparse.ArgumentParser(description="WPS PDF → Markdown，图片落盘并改写为绝对路径")
    p.add_argument("pdf", type=Path, help="PDF 文件路径")
    p.add_argument("-o", "--output", type=Path, required=True, help="输出目录")
    args = p.parse_args()
    parse(args.pdf, args.output)


if __name__ == "__main__":
    main()
