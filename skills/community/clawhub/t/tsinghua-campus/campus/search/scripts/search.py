"""search.py — 校园信息多源搜索（统一入口）

在多个校园站点搜索，返回统一结果列表，每条带来源(source)。

用法:
  search.py --query <关键词> [--source info|its|learn|all] [--limit N]

输出 JSON:
  {"status":"ok", "results":[{"source":"its", "title":"...", "url":"...", "snippet":"..."}]}

来源:
  - info:  info.tsinghua.edu.cn（信息门户通知/公告，直连）
  - its:   its.tsinghua.edu.cn（信息化服务说明，Lucene 站内搜索）
  - learn: learn.tsinghua.edu.cn（网络学堂，课件/公告）
"""
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common

SOURCES = {}


def _register_sources():
    """动态加载各源模块。"""
    src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources")
    sys.path.insert(0, src_dir)
    for mod_name in ["info", "its", "learn"]:
        try:
            mod = __import__(mod_name)
            if hasattr(mod, "search") and hasattr(mod, "SOURCE_NAME"):
                SOURCES[mod.SOURCE_NAME] = mod
                common.log(f"[search] 加载源: {mod.SOURCE_NAME}")
        except Exception as e:
            common.log(f"[search] 源 {mod_name} 加载失败: {e}")


def main():
    ap = argparse.ArgumentParser(description="校园信息多源搜索")
    ap.add_argument("--query", required=True, help="搜索关键词")
    ap.add_argument("--source", default="all", help="来源: info/its/learn/all（默认 all）")
    ap.add_argument("--limit", type=int, default=5, help="每源返回条数（默认 5）")
    args = ap.parse_args()

    _register_sources()

    if not args.query.strip():
        common.output_json({"status": "error", "message": "关键词不能为空"})
        sys.exit(1)

    # 选源
    if args.source == "all":
        sources = list(SOURCES.values())
    elif args.source in SOURCES:
        sources = [SOURCES[args.source]]
    else:
        common.output_json({"status": "error", "message": f"未知来源 {args.source}", "available": list(SOURCES.keys())})
        sys.exit(1)

    if not sources:
        common.output_json({"status": "error", "message": "没有可用搜索源"})
        sys.exit(1)

    # 逐源搜索
    all_results = []
    per_source = {}
    for mod in sources:
        try:
            res = mod.search(args.query, limit=args.limit)
            per_source[mod.SOURCE_NAME] = {"ok": True, "count": len(res)}
            all_results.extend(res)
        except Exception as e:
            per_source[mod.SOURCE_NAME] = {"ok": False, "error": str(e)[:100]}
            common.log(f"[search] {mod.SOURCE_NAME} 失败: {e}")

    # 搜索结束，关闭 CDP 浏览器（防残留；learn 源用 session 不受影响）
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "base-cas", "scripts"))
        import browser as _browser
        if _browser.is_running():
            _browser.stop_cdp()
            common.log("[search] CDP 浏览器已关闭")
    except Exception as e:
        common.log(f"[search] 关闭浏览器失败: {e}")

    common.output_json({
        "status": "ok",
        "query": args.query,
        "per_source": per_source,
        "results": all_results,
    })


if __name__ == "__main__":
    main()
