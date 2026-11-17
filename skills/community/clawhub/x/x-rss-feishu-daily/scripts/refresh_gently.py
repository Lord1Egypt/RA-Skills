"""温和刷新 X 博主订阅 —— 避免触发 X 风控。

防风控逻辑（为什么这样做）：
1. X 侧风控主要盯「同一登录态(token)的高频 API 调用」。
   本脚本逐个 feed 刷新，两个 feed 之间强制间隔（默认 60 秒），
   避免连续 3 个 GraphQL 时间线请求扎堆。
2. 日常自动轮询由 Miniflux 控制（compose 里已设 60~120 分钟/轮），
   RSSHub 又有 30 分钟缓存兜底 —— 一天对 X 只有 ~20-40 次请求，
   低于一个真人刷推的量，这是安全的。
3. 只有三种情况需要手动跑本脚本：首次灌入、换 token 后验证、
   怀疑漏推想立刻核对。平时不要反复跑！

用法：
    python refresh_gently.py          # feed 间隔 60 秒
    python refresh_gently.py 120      # 自定义间隔（秒）
"""
import base64
import json
import os
import sys
import time
import urllib.request

BASE = "http://localhost:8088"
BASIC = "Basic " + base64.b64encode(os.environ.get("MINIFLUX_BASIC", "admin:CHANGE_ME").encode()).decode()
GAP = int(sys.argv[1]) if len(sys.argv) > 1 else 60


def api(path, method="GET"):
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("Authorization", BASIC)
    with urllib.request.urlopen(req, timeout=300) as r:
        body = r.read()
    return json.loads(body) if body else {}


def main():
    feeds = api("/v1/feeds")
    print(f"共 {len(feeds)} 个订阅，间隔 {GAP}s\n")
    for i, f in enumerate(feeds):
        print(f"[{i+1}/{len(feeds)}] 刷新 {f['title']} …", flush=True)
        try:
            api(f"/v1/feeds/{f['id']}/refresh", "PUT")
        except Exception as e:
            print("   刷新失败：", e)
        if i < len(feeds) - 1:
            print(f"   等 {GAP}s 再刷下一个（拉开对 X 的请求）", flush=True)
            time.sleep(GAP)
    print("\n=== 结果 ===")
    for f in api("/v1/feeds"):
        d = api(f"/v1/feeds/{f['id']}/entries?limit=1&order=published_at&direction=desc")
        total = d.get("total", 0)
        entries = d.get("entries") or []
        latest = entries[0]["title"][:50].replace("\n", " ") if entries else "(无)"
        err = f" | 错误: {f['parsing_error_count']}" if f.get("parsing_error_count") else ""
        print(f"{f['title']}: {total} 条{err} | 最新: {latest}")


if __name__ == "__main__":
    main()
