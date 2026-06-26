#!/usr/bin/env python3
"""
doubao-image-gen — 豆包 Seedream 文生图脚本
使用火山引擎 ARK API，支持并发批量生成图片，输出图库预览页。

用法：
  python gen.py --prompt "赛博朋克龙虾" --count 4 --api-key YOUR_KEY
  python gen.py --prompt "水墨山水" --size 2K --out-dir ./output
"""

import argparse
import datetime
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


# ─── 常量 ────────────────────────────────────────────────────────────────────

DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_SIZE = "2K"
DEFAULT_WORKERS = 4
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

VALID_SIZES = [
    "1024x1024", "2K", "1280x720", "720x1280",
    "2048x2048", "2048x1152", "1152x2048", "4K",
]


# ─── 工具函数 ─────────────────────────────────────────────────────────────────

def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def _slug(text: str, max_len: int = 40) -> str:
    """将提示词转为安全文件名片段"""
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text).strip("-")
    return s[:max_len] or "image"


def _load_api_key(cli_key: str | None) -> str:
    """按优先级读取 API Key：CLI 参数 > 环境变量 > ~/.doubao-image-gen/.env"""
    if cli_key:
        return cli_key

    if key := os.environ.get("ARK_API_KEY"):
        return key

    env_file = Path.home() / ".doubao-image-gen" / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ARK_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")

    return ""


def _write_gallery(out_dir: Path, items: list[dict]) -> Path:
    """生成图库预览 HTML"""
    html_items = ""
    for it in items:
        fname = it["file"]
        prompt_escaped = it["prompt"].replace("<", "&lt;").replace(">", "&gt;")
        html_items += f"""
        <div class="card">
          <a href="{fname}" target="_blank">
            <img src="{fname}" alt="{prompt_escaped}" loading="lazy">
          </a>
          <div class="meta">
            <div class="prompt">{prompt_escaped}</div>
            <div class="info">{it.get('model','')} · {it.get('size','')} · {it.get('index','')}</div>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>豆包文生图 · 图库</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
    background: #0d1117; color: #e6edf3;
    padding: 32px 24px;
  }}
  h1 {{
    font-size: 22px; font-weight: 600; margin-bottom: 8px;
    color: #60A5FA;
  }}
  .subtitle {{ font-size: 13px; color: #8b949e; margin-bottom: 28px; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }}
  .card {{
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; overflow: hidden;
    transition: transform .2s, box-shadow .2s;
  }}
  .card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(96,165,250,0.2);
  }}
  .card img {{
    width: 100%; display: block;
    aspect-ratio: 1 / 1; object-fit: cover;
  }}
  .meta {{
    padding: 12px 14px;
  }}
  .prompt {{
    font-size: 13px; line-height: 1.6; color: #c9d1d9;
    display: -webkit-box; -webkit-line-clamp: 3;
    -webkit-box-orient: vertical; overflow: hidden;
  }}
  .info {{
    font-size: 11px; color: #8b949e; margin-top: 8px;
  }}
  .stats {{
    font-size: 13px; color: #8b949e;
    margin-bottom: 20px;
  }}
</style>
</head>
<body>
  <h1>🦞 豆包文生图 · 图库</h1>
  <div class="subtitle">由 doubao-image-gen skill 生成 · {_timestamp()}</div>
  <div class="stats">共 {len(items)} 张图片</div>
  <div class="grid">{html_items}
  </div>
</body>
</html>"""

    index_path = out_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")
    return index_path


# ─── 核心生成函数 ──────────────────────────────────────────────────────────────

def generate_one(
    index: int,
    prompt: str,
    model: str,
    size: str,
    api_key: str,
    out_dir: Path,
    watermark: bool,
) -> dict:
    """调用豆包 API 生成单张图片，下载并保存"""
    try:
        from openai import OpenAI
    except ImportError:
        print("请先安装 openai 库：pip install 'openai>=1.0'", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(base_url=ARK_BASE_URL, api_key=api_key)

    print(f"  [{index:02d}] 生成中...", flush=True)
    resp = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        response_format="url",
        extra_body={"watermark": watermark},
    )

    url = resp.data[0].url
    print(f"  [{index:02d}] 下载图片...", flush=True)

    import requests as req_lib
    r = req_lib.get(url, timeout=60)
    r.raise_for_status()

    filename = f"{index:02d}-{_slug(prompt)}.jpeg"
    save_path = out_dir / filename
    save_path.write_bytes(r.content)

    print(f"  [{index:02d}] ✓ 保存: {filename} ({len(r.content)//1024}KB)", flush=True)

    return {
        "index": f"#{index:02d}",
        "file": filename,
        "path": str(save_path),
        "prompt": prompt,
        "model": model,
        "size": size,
        "url": url,
    }


# ─── 主函数 ───────────────────────────────────────────────────────────────────

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="doubao-image-gen",
        description="豆包 Seedream 文生图 — 支持并发批量生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python gen.py --prompt "赛博朋克龙虾" --api-key YOUR_KEY
  python gen.py --prompt "水墨山水画" --count 4 --size 2K
  python gen.py --prompt "未来城市夜景" --out-dir ./my-images --workers 2
        """,
    )

    parser.add_argument("--prompt", "-p", required=True, help="图像描述提示词")
    parser.add_argument("--count", "-n", type=int, default=1, help="生成数量（默认1）")
    parser.add_argument("--size", "-s", default=DEFAULT_SIZE,
                        choices=VALID_SIZES, help=f"图像尺寸（默认 {DEFAULT_SIZE}）")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="模型名称")
    parser.add_argument("--out-dir", "-o", default=None, help="输出目录")
    parser.add_argument("--api-key", "-k", default=None, help="ARK API Key")
    parser.add_argument("--workers", "-w", type=int, default=DEFAULT_WORKERS,
                        help=f"并发线程数（默认 {DEFAULT_WORKERS}）")
    parser.add_argument("--watermark", action="store_true", default=False,
                        help="添加水印（默认关闭）")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅打印参数，不调用 API")

    args = parser.parse_args(argv)

    # 读取 API Key
    api_key = _load_api_key(args.api_key)
    if not api_key and not args.dry_run:
        print("❌ 未找到 API Key，请通过以下方式之一提供：", file=sys.stderr)
        print("   1. --api-key YOUR_KEY", file=sys.stderr)
        print("   2. 环境变量 ARK_API_KEY=YOUR_KEY", file=sys.stderr)
        print("   3. ~/.doubao-image-gen/.env 文件写入 ARK_API_KEY=YOUR_KEY", file=sys.stderr)
        return 2

    # 输出目录
    out_dir = Path(args.out_dir) if args.out_dir else Path(f"doubao-output-{_timestamp()}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # dry-run 模式
    if args.dry_run:
        print("=== DRY RUN ===")
        print(f"prompt  : {args.prompt}")
        print(f"count   : {args.count}")
        print(f"size    : {args.size}")
        print(f"model   : {args.model}")
        print(f"workers : {args.workers}")
        print(f"out_dir : {out_dir}")
        return 0

    print(f"🚀 开始生成 {args.count} 张图片（并发数: {min(args.workers, args.count)}）")
    print(f"   模型: {args.model} | 尺寸: {args.size} | 输出: {out_dir}\n")

    items = []
    errors = []
    workers = min(args.workers, args.count)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                generate_one,
                i, args.prompt, args.model, args.size,
                api_key, out_dir, args.watermark,
            ): i
            for i in range(1, args.count + 1)
        }
        for future in as_completed(futures):
            idx = futures[future]
            try:
                result = future.result()
                items.append(result)
            except Exception as e:
                errors.append((idx, str(e)))
                print(f"  [{idx:02d}] ❌ 失败: {e}", file=sys.stderr)

    # 按序号排序
    items.sort(key=lambda x: x["index"])

    # 保存 prompts.json
    json_path = out_dir / "prompts.json"
    json_path.write_text(
        json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 生成图库预览
    if items:
        index_path = _write_gallery(out_dir, items)
        print(f"\n✅ 完成！生成 {len(items)} 张，失败 {len(errors)} 张")
        print(f"   输出目录: {out_dir}")
        print(f"   图库预览: {index_path}")
        # 输出图片路径供 AI 直接引用
        print("\n--- 图片路径 ---")
        for it in items:
            print(f"GENERATED_IMAGE: {it['path']}")
    else:
        print("\n❌ 全部生成失败", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
