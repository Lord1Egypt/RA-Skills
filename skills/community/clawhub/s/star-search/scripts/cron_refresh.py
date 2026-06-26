#!/usr/bin/env python3
"""
star-search 定时增量客户端 v16.1

调用 api_server 的 /v1/search/refresh 接口，
对每个监控的 query 定期拉新（默认 30 分钟），
输出 JSON 行到 stdout 供 subagent / 管道消费。

v16.1 变更:
- 加 6 个新 mode: dev_rss / tech_news / finance / weixin_agg / global_en / all
- 加 --engine 强制单引擎
- 加 --preset (dev/finance/tech/weixin/all) 一键选 query 模板
- 加 --watch N（循环秒数）+ 并发并发可控

用法:
  # 单次拉
  python3 scripts/cron_refresh.py --query "华为鸿蒙 PC" --mode dev_rss

  # 多 query 批量
  python3 scripts/cron_refresh.py --queries "华为鸿蒙" "DeepSeek V4" "英伟达" --mode tech_news

  # preset 一键启动
  python3 scripts/cron_refresh.py --preset tech --loop 1800

  # 强制单引擎
  python3 scripts/cron_refresh.py --query "..." --engine rss_ithome
"""
import argparse, json, sys, time, asyncio
import httpx

DEFAULT_API = "http://127.0.0.1:9800"

# v16.1: mode 枚举（与 api_server MODES 对齐 + 新增）
ALL_MODES = [
    'dev', 'news', 'deep', 'policy', 'stock', 'quick', 'global',
    # v16.1 新增组合 mode（按 v15.1 + v16.1 新引擎定制）
    'dev_rss',     # dev + 5 RSS 引擎（技术向最强）
    'tech_news',   # csdn/cnblogs/sspai/oschina + RSS
    'finance',     # eastmoney/cls/sina_finance + RSS 财经
    'weixin_agg',  # 微信 + weixin_bing + 财经
]

# v16.1: preset 一键模板（开箱即用）
PRESETS = {
    'dev': {
        'queries': ['Python asyncio 教程', 'Rust 入门', 'TypeScript 新特性',
                    'Vue 3 vs React', 'PostgreSQL 性能优化', 'Kubernetes 实战',
                    'OpenAI API 价格', 'GitHub Actions 部署'],
        'mode': 'dev_rss',
        'loop': 1800,
    },
    'finance': {
        'queries': ['A股 今日行情', '央行 货币政策', '美元 人民币汇率',
                    '黄金 价格', '腾讯 财报', '英伟达 股价',
                    'DeepSeek 融资', '美联储 加息'],
        'mode': 'finance',
        'loop': 1800,
    },
    'tech': {
        'queries': ['鸿蒙 PC', 'Vision Pro 中国', 'GPT-5 升级', 'Claude 4',
                    '苹果 WWDC 2026', '英伟达 GTC', '华为 Mate 70', '小米 SU8'],
        'mode': 'tech_news',
        'loop': 1800,
    },
    'weixin': {
        'queries': ['大模型 商业化', 'AI Agent 创业', '具身智能 进展',
                    '国产 GPU 突破', '人形机器人 价格', 'AI 监管 最新'],
        'mode': 'weixin_agg',
        'loop': 3600,
    },
    'all': {
        'queries': [],  # 留空 = 用户必须传 --queries
        'mode': 'deep',
        'loop': 3600,
    },
}

# 模板 /preset 互相组合示例：每个 preset 都预设好 8 条 query + mode + loop
PRESET_DESCRIPTIONS = {
    'dev':     '8 条开发者向 query · dev_rss mode · 30分钟',
    'finance': '8 条财经向 query · finance mode · 30分钟',
    'tech':    '8 条科技向 query · tech_news mode · 30分钟',
    'weixin':  '6 条微信生态 query · weixin_agg mode · 1小时',
    'all':     '需传 --queries · deep mode · 1小时',
}

async def refresh(client, api, query, mode='dev', top=10, engine=None):
    payload = {"query": query, "mode": mode, "top": top}
    if engine:
        payload["engine"] = engine
    try:
        r = await client.post(f"{api}/v1/search/refresh",
            json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e), "query": query, "engine": engine}

async def main(args):
    api = args.api.rstrip('/')

    # 处理 --preset
    if args.preset:
        if args.preset not in PRESETS:
            print(f"未知 preset: {args.preset}\n可用: {', '.join(PRESETS.keys())}", file=sys.stderr)
            sys.exit(1)
        ps = PRESETS[args.preset]
        queries = ps['queries'] or args.queries
        if not queries:
            print(f"--preset {args.preset} 模板无内置 query，请同时传 --queries", file=sys.stderr)
            sys.exit(1)
        mode = args.mode or ps['mode']
        loop = args.loop or ps['loop']
    else:
        queries = args.queries or ([args.query] if args.query else [])
        if not queries:
            print("需要 --query / --queries / --preset", file=sys.stderr)
            sys.exit(1)
        mode = args.mode
        loop = args.loop

    print(f"🚀 star-search cron_refresh v16.1", file=sys.stderr)
    print(f"   API: {api} | mode: {mode} | engine: {args.engine or '<auto>'} | queries: {len(queries)} | loop: {loop}s", file=sys.stderr)

    async with httpx.AsyncClient() as client:
        iteration = 0
        while True:
            iteration += 1
            ts = int(time.time())
            t0 = time.time()
            results = await asyncio.gather(*[
                refresh(client, api, q, mode=mode, top=args.top, engine=args.engine) for q in queries
            ])
            elapsed = time.time() - t0
            new_count = sum(r.get('new_count', 0) for r in results if 'error' not in r)
            err_count = sum(1 for r in results if 'error' in r)

            # 输出 JSONL
            for r in results:
                r['_ts'] = ts
                r['_iteration'] = iteration
                print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()

            print(f"  第 {iteration} 轮 · 耗时 {elapsed:.1f}s · 新增 {new_count} 条 · 错误 {err_count}", file=sys.stderr)

            if not loop:
                break
            time.sleep(loop)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description='star-search cron_refresh v16.1')
    p.add_argument("--api", default=DEFAULT_API)
    p.add_argument("--query", help="单 query")
    p.add_argument("--queries", nargs="+", help="多 query 批量")
    p.add_argument("--mode", default=None, choices=ALL_MODES,
                   help="v16.1: 加 6 个新 mode (dev_rss/tech_news/finance/weixin_agg 等)")
    p.add_argument("--engine", default=None, help="v16.1: 强制单引擎 (例 rss_ithome/bing_cn/csdn)")
    p.add_argument("--preset", choices=list(PRESETS.keys()),
                   help="v16.1: 一键模板 (dev/finance/tech/weixin/all)，自动配 8 条 query + mode + loop")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--loop", type=int, default=0, help="秒，0=单次；N=每N秒循环")
    args = p.parse_args()
    asyncio.run(main(args))
