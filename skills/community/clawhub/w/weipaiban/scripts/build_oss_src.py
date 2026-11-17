#!/usr/bin/env python3
"""按画布占位框给站内 CDN 原图拼接 x-oss-process（先 crop 再 resize）。

算法对齐 packages/image-crop：
- 仅 svg-cdn.creatby.com
- 去掉 _large/_middle/_thumb，去掉旧 x-oss-process
- cover：按目标宽高比从原图切溢出（重力默认 center）
- contain：不按目标比裁切，只缩长边
- 长边上限默认 1080，只缩小不放大
- 顺序：image/crop,.../resize,m_lfit,w_*,h_*
- query 里 / 与 , 不编码
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

CDN_HOST = "svg-cdn.creatby.com"
SIZE_SUFFIX = re.compile(r"_(?:large|middle|thumb)$")
GRAVITIES = {
    "nw",
    "north",
    "ne",
    "west",
    "center",
    "east",
    "sw",
    "south",
    "se",
}
RATIO_EPS = 0.02


def strip_size_suffix(pathname: str) -> str:
    parts = pathname.split("/")
    if not parts:
        return pathname
    parts[-1] = SIZE_SUFFIX.sub("", parts[-1])
    return "/".join(parts)


def get_processable_url(url: str) -> str | None:
    try:
        parsed = urlparse(url)
    except ValueError:
        return None
    if parsed.hostname != CDN_HOST:
        return None
    path = strip_size_suffix(parsed.path)
    pairs = [
        (k, v)
        for k, v in parse_qsl(parsed.query, keep_blank_values=True)
        if k != "x-oss-process"
    ]
    query = urlencode(pairs)
    return urlunparse((parsed.scheme, parsed.netloc, path, "", query, ""))


def compute_output_size(
    crop_w: int, crop_h: int, max_edge: int | None
) -> tuple[int, int]:
    w = max(1, round(crop_w))
    h = max(1, round(crop_h))
    if max_edge is None or max_edge <= 0:
        return w, h
    long_edge = max(w, h)
    if long_edge <= max_edge:
        return w, h
    scale = max_edge / long_edge
    return max(1, round(w * scale)), max(1, round(h * scale))


def clamp_rect(
    x: float, y: float, w: float, h: float, nw: int, nh: int
) -> tuple[int, int, int, int]:
    max_w = max(1, round(nw))
    max_h = max(1, round(nh))
    w_i = max(1, min(round(w), max_w))
    h_i = max(1, min(round(h), max_h))
    x_i = max(0, min(round(x), max_w - w_i))
    y_i = max(0, min(round(y), max_h - h_i))
    w_i = min(w_i, max_w - x_i)
    h_i = min(h_i, max_h - y_i)
    return max(0, x_i), max(0, y_i), max(1, w_i), max(1, h_i)


def cover_crop(nw: int, nh: int, tw: int, th: int) -> tuple[int, int, int, int]:
    """原图内切出目标宽高比（铺满占位，切溢出）。"""
    target = max(1e-6, tw) / max(1e-6, th)
    if nw / nh > target:
        ch = float(nh)
        cw = ch * target
    else:
        cw = float(nw)
        ch = cw / target
    x = (nw - cw) / 2
    y = (nh - ch) / 2
    return clamp_rect(x, y, cw, ch, nw, nh)


def aspects_close(nw: int, nh: int, tw: int, th: int) -> bool:
    sr = nw / max(1, nh)
    tr = tw / max(1, th)
    return abs(sr - tr) / tr < RATIO_EPS


def build_crop_segment(
    w: int,
    h: int,
    gravity: str,
    x: int | None = None,
    y: int | None = None,
) -> str:
    if x is not None and y is not None:
        return f"crop,x_{x},y_{y},w_{w},h_{h}"
    g = gravity if gravity in GRAVITIES else "center"
    return f"crop,w_{w},h_{h},g_{g}"


def build_image_process(crop: dict | None, resize: dict | None) -> str | None:
    segments: list[str] = []
    if crop:
        segments.append(
            build_crop_segment(
                crop["w"],
                crop["h"],
                crop.get("g", "center"),
                crop.get("x"),
                crop.get("y"),
            )
        )
    if resize:
        segments.append(f"resize,m_lfit,w_{resize['w']},h_{resize['h']}")
    if not segments:
        return None
    return "image/" + "/".join(segments)


def attach_process(base: str, process: str) -> str:
    parsed = urlparse(base)
    pairs = [
        (k, v)
        for k, v in parse_qsl(parsed.query, keep_blank_values=True)
        if k != "x-oss-process"
    ]
    other = urlencode(pairs)
    process_query = f"x-oss-process={process}"
    query = f"{other}&{process_query}" if other else process_query
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}"


def build_oss_src(
    url: str,
    natural_w: int,
    natural_h: int,
    target_w: int,
    target_h: int,
    crop_mode: str = "cover",
    gravity: str = "center",
    max_edge: int = 1080,
) -> dict:
    base = get_processable_url(url)
    if not base:
        return {"ok": False, "error": "href 必须是 svg-cdn.creatby.com 站内 CDN"}

    nw = max(1, int(natural_w))
    nh = max(1, int(natural_h))
    tw = max(1, int(target_w))
    th = max(1, int(target_h))
    mode = crop_mode if crop_mode in {"cover", "contain"} else "cover"
    g = gravity if gravity in GRAVITIES else "center"

    crop = None
    crop_w, crop_h = nw, nh
    if mode == "cover" and not aspects_close(nw, nh, tw, th):
        _x, _y, crop_w, crop_h = cover_crop(nw, nh, tw, th)
        crop = {"w": crop_w, "h": crop_h, "g": g}

    rw, rh = compute_output_size(crop_w, crop_h, max_edge)
    resize = None
    if (rw, rh) != (crop_w, crop_h):
        resize = {"w": rw, "h": rh}

    process = build_image_process(crop, resize)
    src = attach_process(base, process) if process else base
    return {
        "ok": True,
        "src": src,
        "originSrc": base,
        "ossProcess": process,
        "outputWidth": rw,
        "outputHeight": rh,
        "naturalWidth": nw,
        "naturalHeight": nh,
        "boxWidth": tw,
        "boxHeight": th,
        "cropMode": mode,
        "cropGravity": g,
        "crop": crop,
        "resize": resize,
    }


def self_test() -> None:
    cases = []

    r = build_oss_src(
        "https://svg-cdn.creatby.com/hash.png_large",
        2048,
        2048,
        390,
        168,
        "cover",
        "center",
        1080,
    )
    assert r["ok"]
    assert r["originSrc"] == "https://svg-cdn.creatby.com/hash.png"
    assert r["crop"]["w"] == 2048
    assert r["crop"]["h"] == 882  # 2048 * 168 / 390
    assert r["outputWidth"] == 1080
    assert r["ossProcess"].startswith("image/crop,")
    assert "/resize,m_lfit,w_1080," in r["ossProcess"]
    cases.append("cover-wide")

    r = build_oss_src(
        "https://svg-cdn.creatby.com/hash.png",
        800,
        800,
        64,
        64,
        "contain",
        "center",
        1080,
    )
    assert r["ok"]
    assert r["crop"] is None
    assert r["resize"] is None
    assert r["src"] == r["originSrc"]
    cases.append("contain-small")

    r = build_oss_src(
        "https://svg-cdn.creatby.com/hash.png",
        2000,
        2000,
        64,
        64,
        "contain",
        "center",
        1080,
    )
    assert r["resize"] == {"w": 1080, "h": 1080}
    assert r["ossProcess"] == "image/resize,m_lfit,w_1080,h_1080"
    cases.append("contain-resize")

    r = build_oss_src("https://example.com/a.png", 100, 100, 50, 50)
    assert r["ok"] is False
    cases.append("reject-foreign")

    print(json.dumps({"ok": True, "cases": cases}, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="为 creatby CDN 图拼接 OSS crop/resize")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--url")
    parser.add_argument("--natural-w", type=int)
    parser.add_argument("--natural-h", type=int)
    parser.add_argument("--target-w", type=int)
    parser.add_argument("--target-h", type=int)
    parser.add_argument("--crop-mode", default="cover", choices=["cover", "contain"])
    parser.add_argument("--gravity", default="center")
    parser.add_argument("--max-edge", type=int, default=1080)
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    missing = [
        name
        for name in ("url", "natural_w", "natural_h", "target_w", "target_h")
        if getattr(args, name) in (None, "")
    ]
    if missing:
        parser.error(f"缺少参数: {', '.join(missing)}")

    result = build_oss_src(
        args.url,
        args.natural_w,
        args.natural_h,
        args.target_w,
        args.target_h,
        args.crop_mode,
        args.gravity,
        args.max_edge,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
