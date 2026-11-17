#!/usr/bin/env python3
"""批量自查 SkillHub 的 slug 是否已被占用。

判据：下载接口 `GET /api/v1/download?slug=<slug>`
    200 -> 平台上已有同名「已发布」技能
    404 -> 公开层面无此技能

⚠️ 手工用 curl 探时的两个坑（脚本本身不受影响，因为 urllib 自动跟随重定向）：
  1. **域名必须是 `api.skillhub.cn`**。`skillhub.cn` 是前端 SPA，任何 slug（含乱码）
     都返回 200 + 同一个 HTML 外壳 —— 拿它判重会得出「全都被占用」的假结论。
  2. **原始响应是 `302` 重定向到 zip 包**，`curl` 不加 `-L` 看到的就是 302。
     所以判据要读作：**302 或 200 = 已发布 / 404 = 未占用**。
     回归校验：拿一个确定不存在的 slug（如 `zzz-not-a-real-skill-987654321`）应得 404。

⚠️ 重要局限（务必先读）：
  1. 搜索接口 search?q= 不能用来判重 —— 它是模糊匹配，对 `ym-xxx` 这类带短前缀的词
     直接返回兜底热门列表，看着像"无结果"其实只是没匹配上。
  2. 404 **不等于**可用。已被占用但尚未公开发布（草稿/审核中/私有）的 slug 同样是 404。
     实测反例：`skill-generator` 被占用（发布被拒），但下载接口 404、搜索也零命中。
  因此本脚本只能用来「批量排除已经被别人发布的名字」，最终仍需在发布表单里由服务端
  给出权威判定。

用法:
    python check_slug.py ym-skill-generator ym-skill-forge
    python check_slug.py --file candidates.txt
    python check_slug.py --json ym-skill-generator
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DOWNLOAD_API = "https://api.skillhub.cn/api/v1/download?slug={slug}"
HEADERS = {"User-Agent": "ym-skillhub/2.0"}
TIMEOUT = 15


def probe(slug: str) -> tuple[int | str, str]:
    """返回 (状态码或 'ERR', 判定文本)。"""
    url = DOWNLOAD_API.format(slug=urllib.parse.quote(slug))
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            resp.read(0)
            return resp.status, "已存在（已被别人发布）"
    except urllib.error.HTTPError as e:
        e.read()
        if e.code == 404:
            return 404, "公开层面无此技能（未发布占用的仍查不到）"
        return e.code, "未知状态，需人工确认"
    except Exception as e:  # noqa: BLE001 - 网络异常一律降级报告
        return "ERR", f"请求失败: {type(e).__name__}"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="批量自查 SkillHub slug 占用情况（判据：下载接口）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("slugs", nargs="*", help="候选 slug 列表")
    ap.add_argument("--file", help="从文本文件读取候选（每行一个，# 开头忽略）")
    ap.add_argument("--json", dest="as_json", action="store_true", help="以 JSON 输出")
    ap.add_argument("--delay", type=float, default=0.25, help="请求间隔秒数（默认 0.25）")
    args = ap.parse_args()

    slugs = list(args.slugs)
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    slugs.append(line)

    slugs = list(dict.fromkeys(slugs))  # 去重且保序
    if not slugs:
        ap.error("至少给一个 slug，或用 --file 指定文件")

    results = []
    for i, slug in enumerate(slugs):
        code, verdict = probe(slug)
        results.append({"slug": slug, "http": code, "verdict": verdict})
        if not args.as_json:
            mark = "占用" if code == 200 else ("待验" if code == 404 else "未知")
            print(f"[{mark}] {slug:<28} HTTP {code}  {verdict}")
        if i < len(slugs) - 1:
            time.sleep(args.delay)

    if args.as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))

    taken = [r["slug"] for r in results if r["http"] == 200]
    if taken and not args.as_json:
        print(f"\n已确认被占用的 {len(taken)} 个，建议排除：{', '.join(taken)}")
        print("其余仅代表「公开层面查不到」，不等于可用，仍需在发布表单里最终确认。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
