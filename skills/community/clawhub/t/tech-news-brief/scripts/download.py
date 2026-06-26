#!/usr/bin/env python3
# download.py — 使用 Firecrawl API 抓取网页正文并写入本地文件。
# 用法: python3 scripts/download.py <URL> <输出文件路径>
#
# ⚠️ Firecrawl 额度有限，本脚本仅作 fallback 方案。
#    下载第一优先使用 browser MCP 工具，仅当 browser 失败 2 次后才调用本脚本。
#
# 环境变量:
#   FIRECRAWL_API_KEY  Firecrawl API Key（必须通过环境变量设置）
#   REPORTS_DIR        输出目录根路径（默认 /home/sml/workspace/InternetInformation）

import sys
import os
import json

FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY")
REPORTS_DIR = os.environ.get("REPORTS_DIR", "/home/sml/workspace/InternetInformation")


def download_with_firecrawl(
    url: str,
    output_path: str,
    api_key: str = FIRECRAWL_API_KEY,
) -> bool:
    import urllib.request
    import urllib.error

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    payload = json.dumps({
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.firecrawl.dev/v2/scrape",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return False

    if not raw.get("success"):
        print(f"Firecrawl 返回失败: {raw}", file=sys.stderr)
        return False

    markdown = raw.get("data", {}).get("markdown", "")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    char_count = len(markdown)
    print(f"下载成功: {output_path}")
    print(f"字数统计: {char_count} 字", file=sys.stderr)
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/download.py <URL> <输出文件路径>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    output_path = sys.argv[2]

    ok = download_with_firecrawl(url, output_path)
    sys.exit(0 if ok else 1)
