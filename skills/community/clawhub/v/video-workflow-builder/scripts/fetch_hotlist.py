#!/usr/bin/env python3
"""Fetch real-time hot lists from a self-hosted DailyHotApi instance.

创作前扫一圈各平台实时热榜（抖音/B站/知乎/微博等），给"选题第零步"提供
实时舆论风向。数据源是自部署的 imsyy/DailyHotApi（免登录、只读公开热榜、
无封号风险），base URL 从环境变量读取。

用法:
    python3 fetch_hotlist.py --platforms douyin,bilibili,zhihu,weibo
    python3 fetch_hotlist.py --platforms douyin --top 15 --json

base URL 读取顺序:
    1. 环境变量 DAILYHOT_API_BASE（如 http://localhost:6688）
    2. skill 目录下 .env 里的 DAILYHOT_API_BASE=xxx
    未配置则报错退出——本工具不返回任何缓存/历史数据。

铁律：抓不到就报错，绝不返回旧数据。偏离实时常识的选题就是垃圾，宁可停下
让用户去修数据源，也不拿过时热榜冒充当下风向。
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

# DailyHotApi 覆盖的常用平台路由；完整列表见该项目 README。
KNOWN_PLATFORMS = [
    "douyin", "bilibili", "zhihu", "weibo", "baidu",
    "toutiao", "kuaishou", "36kr", "juejin", "douban-movie",
]

DEFAULT_TIMEOUT = 10


def _load_api_base():
    """按优先级读取 DailyHotApi base URL：环境变量 > skill 目录 .env。"""
    base = os.environ.get("DAILYHOT_API_BASE")
    if base:
        return base.strip().rstrip("/")
    env_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, _, value = line.partition("=")
                if name.strip() == "DAILYHOT_API_BASE":
                    return value.strip().strip('"').strip("'").rstrip("/")
    except FileNotFoundError:
        pass
    return None


def fetch_platform(base, platform, timeout=DEFAULT_TIMEOUT):
    """拉单个平台热榜，返回 (title, [items])。失败抛异常，绝不吞掉。"""
    url = "%s/%s" % (base, platform)
    req = urllib.request.Request(url, headers={"User-Agent": "peanutcut-hotlist/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    # DailyHotApi 正常返回 {"code":200,"title":...,"data":[{title,hot,...}]}
    if payload.get("code") not in (200, "200", None):
        raise RuntimeError("热榜接口返回异常 code=%r (%s)" % (payload.get("code"), platform))
    data = payload.get("data")
    if not isinstance(data, list):
        raise RuntimeError("热榜接口无 data 数组 (%s)" % platform)
    return payload.get("title") or platform, data


def fetch(platforms, top=20, timeout=DEFAULT_TIMEOUT, base=None):
    """拉多平台热榜。任一平台失败即抛出——不静默跳过、不返回部分旧数据。"""
    base = base or _load_api_base()
    if not base:
        raise RuntimeError(
            "未配置 DAILYHOT_API_BASE。请先自部署 imsyy/DailyHotApi（Docker 或 "
            "Vercel），再把地址写进环境变量或 skill 目录的 .env："
            "DAILYHOT_API_BASE=http://your-host:6688")
    result = {}
    for p in platforms:
        title, items = fetch_platform(base, p, timeout=timeout)
        result[p] = {"title": title, "items": items[:top]}
    return result


def _print_human(result):
    for platform, block in result.items():
        print("\n【%s】%s" % (platform, block["title"]))
        for i, item in enumerate(block["items"], 1):
            hot = item.get("hot")
            hot_s = " (%s)" % hot if hot not in (None, "") else ""
            print("  %2d. %s%s" % (i, item.get("title", ""), hot_s))


def main(argv):
    p = argparse.ArgumentParser(
        description="拉取各平台实时热榜（自部署 DailyHotApi）")
    p.add_argument(
        "--platforms", default="douyin,bilibili,zhihu,weibo",
        help="逗号分隔的平台列表，可选：%s" % ",".join(KNOWN_PLATFORMS))
    p.add_argument("--top", type=int, default=20, help="每个平台取前 N 条")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    p.add_argument("--json", action="store_true", help="输出原始 JSON 而非人类可读格式")
    args = p.parse_args(argv)

    platforms = [x.strip() for x in args.platforms.split(",") if x.strip()]
    try:
        result = fetch(platforms, top=args.top, timeout=args.timeout)
    except (urllib.error.URLError, OSError) as e:
        print("热榜抓取失败（网络/服务不可达）：%s\n"
              "本工具不返回缓存数据——请修好 DailyHotApi 再重试，"
              "不要用过时热榜创作。" % e, file=sys.stderr)
        return 1
    except (ValueError, RuntimeError) as e:
        print("热榜抓取失败：%s" % e, file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_human(result)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
