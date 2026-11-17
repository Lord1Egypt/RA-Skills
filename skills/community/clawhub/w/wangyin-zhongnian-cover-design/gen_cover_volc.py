#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调用火山引擎 ARK (Seedream) 生成公众号封面。
读取 ~/.baoyu-skills/.env 中的 ARK_API_KEY / ARK_BASE_URL。
支持：
  - 文生图（默认）
  - 多参考图（--ref 可重复，base64 传入 image 字段）
  - watermark:false
尺寸必须满足 doubao-seedream-5-0-260128 的总像素 >= 3,686,400。
"""
import os
import sys
import json
import base64
import argparse
import urllib.request
import urllib.error

ENV_PATH = os.path.expanduser("~/.baoyu-skills/.env")
DEFAULT_OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_SIZE = "2976x1264"  # ≈2.35:1, 总像素 3,760,064 >= 3,686,400, 均为16倍数


def load_env(path):
    env = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env


def encode_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/{ext};base64,{b64}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--size", default=DEFAULT_SIZE)
    parser.add_argument("--ref", action="append", default=[], help="参考图路径，可重复")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_DIR, help="输出目录")
    parser.add_argument("--filename", default="cover_v3_seedream.png", help="输出文件名")
    args = parser.parse_args()

    env = load_env(ENV_PATH)
    api_key = env.get("ARK_API_KEY") or env.get("IMAGE_API_KEY") or env.get("SEEDREAM_API_KEY")
    base_url = env.get("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3").rstrip("/")
    if not api_key:
        print("ERROR: 未找到 ARK_API_KEY")
        sys.exit(1)

    prompt = sys.stdin.read().strip()
    if not prompt:
        print("ERROR: 未从 stdin 读到 prompt")
        sys.exit(1)

    url = base_url + "/images/generations"
    body = {
        "model": args.model,
        "prompt": prompt,
        "size": args.size,
        "output_format": "png",
        "watermark": False,
    }
    if args.ref:
        refs = [encode_image_base64(p) for p in args.ref]
        body["image"] = refs if len(refs) > 1 else refs[0]
        print(f"-> 参考图数量: {len(refs)}")

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer " + api_key)

    print(f"-> POST {url}")
    print(f"-> model={args.model} size={args.size} watermark=False")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {detail}")
        sys.exit(2)
    except Exception as e:
        print(f"请求失败: {e}")
        sys.exit(3)

    if "data" not in payload or not payload["data"]:
        print("ERROR: 响应中没有 data 字段")
        print(json.dumps(payload, ensure_ascii=False)[:2000])
        sys.exit(4)

    item = payload["data"][0]
    os.makedirs(args.output, exist_ok=True)
    out_path = os.path.join(args.output, args.filename)

    if "url" in item:
        img_url = item["url"]
        print(f"-> 下载图片: {img_url}")
        try:
            with urllib.request.urlopen(img_url, timeout=120) as r:
                img_bytes = r.read()
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            print(f"OK 已保存: {out_path} ({len(img_bytes)} bytes)")
        except Exception as e:
            print(f"下载失败: {e}")
            print(f"图片 URL: {img_url}")
            sys.exit(5)
    elif "b64_json" in item:
        img_bytes = base64.b64decode(item["b64_json"])
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"OK 已保存(b64): {out_path} ({len(img_bytes)} bytes)")
    else:
        print("ERROR: data[0] 中没有 url 或 b64_json")
        print(json.dumps(payload, ensure_ascii=False)[:2000])
        sys.exit(6)

    if "usage" in payload:
        print("usage:", json.dumps(payload["usage"], ensure_ascii=False))


if __name__ == "__main__":
    main()
