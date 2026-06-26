# -*- coding: utf-8 -*-
"""
LLM 增量分类脚本
对 articles_final.csv 中 category=other 的记录进行 LLM 重新分类
支持断点续传，适合大量数据的长时间处理

用法：
    python llm_incremental.py [--input CSV] [--output CSV] [--checkpoint JSON] [--batch-size 50] [--concurrency 20] [--max-runtime 300]
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import csv, json, time, argparse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from llm_classify import (
    SAFE_MODE, LLM_MODEL, LLM_API_URL, LLM_API_KEY, LLM_TEMPERATURE,
    CATEGORY_TAGS, parse_llm_response, build_classify_prompt
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(SCRIPT_DIR, "..", "exported_favorites", "articles_final.csv")
DEFAULT_OUTPUT = os.path.join(SCRIPT_DIR, "..", "exported_favorites", "articles_final_llm.csv")
DEFAULT_CHECKPOINT = os.path.join(SCRIPT_DIR, "..", "exported_favorites", "llm_checkpoint.json")


def parse_args():
    parser = argparse.ArgumentParser(description="LLM 增量分类（断点续传）")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="输入 CSV")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="输出 CSV")
    parser.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT, help="检查点文件")
    parser.add_argument("--batch-size", type=int, default=50, help="批大小")
    parser.add_argument("--concurrency", type=int, default=20, help="并发数")
    parser.add_argument("--max-runtime", type=int, default=300,
                        help="最大运行秒数（超时保存检查点退出）")
    return parser.parse_args()


def call_llm(article):
    """单次 LLM 调用"""
    if SAFE_MODE:
        return {
            "local_id": article.get("local_id", ""),
            "tags": [],
            "reason": "SAFE_MODE enabled",
            "confidence": 0.0
        }
    prompt = build_classify_prompt(article)

    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": LLM_TEMPERATURE,
        "max_tokens": 256,
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            LLM_API_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LLM_API_KEY}",
                "HTTP-Referer": "https://github.com/qclaw/wechat-favorites",
                "X-Title": "QClaw"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            parsed = parse_llm_response(content)
            if parsed:
                return {
                    "local_id": article.get("local_id", ""),
                    "tags": parsed.get("tags", []),
                    "reason": parsed.get("reason", ""),
                    "confidence": parsed.get("confidence", 0.5)
                }
    except Exception as e:
        return {"local_id": article.get("local_id", ""), "tags": [], "reason": str(e)[:50], "confidence": 0.0}
    return {"local_id": article.get("local_id", ""), "tags": [], "reason": "parse failed", "confidence": 0.0}


def main():
    args = parse_args()
    start_time = time.time()

    if not LLM_API_KEY:
        print("[ERROR] LLM_API_KEY 环境变量未设置")
        return 1

    # 读取检查点
    checkpoint = {"done_ids": set(), "results": []}
    if os.path.exists(args.checkpoint):
        with open(args.checkpoint, 'r', encoding='utf-8') as f:
            cp_data = json.load(f)
            checkpoint["done_ids"] = set(cp_data.get("done_ids", []))
            checkpoint["results"] = cp_data.get("results", [])
        print(f"Loaded checkpoint: {len(checkpoint['done_ids'])} done", flush=True)

    # 读取数据
    with open(args.input, 'r', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    # 筛选 category=other 且未处理
    other_rows = [r for r in rows if r.get('category', '') == 'other'
                   and r.get('local_id', '') not in checkpoint["done_ids"]]

    print(f"Total rows: {len(rows)}", flush=True)
    print(f"'other' to process: {len(other_rows)}", flush=True)

    if not other_rows:
        print("Nothing to process", flush=True)
        return 0

    articles = [{'local_id': r.get('local_id', ''), 'title': r.get('title', ''),
                 'source_account': r.get('source_account', ''), 'url': r.get('url', '')}
                for r in other_rows]

    total = len(articles)
    done = 0
    new_results = []

    for batch_idx in range(0, total, args.batch_size):
        # 检查运行时间
        elapsed = time.time() - start_time
        if elapsed > args.max_runtime:
            print(f"\nTime limit reached ({elapsed:.0f}s), saving checkpoint...", flush=True)
            break

        batch = articles[batch_idx:batch_idx + args.batch_size]
        batch_num = batch_idx // args.batch_size + 1
        total_batches = (total + args.batch_size - 1) // args.batch_size

        print(f"Batch {batch_num}/{total_batches}...", end=" ", flush=True)

        with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            futures = {executor.submit(call_llm, a): a for a in batch}
            batch_results = []
            for future in as_completed(futures):
                try:
                    batch_results.append(future.result())
                except Exception as e:
                    batch_results.append({"local_id": "", "tags": [], "reason": str(e)[:30], "confidence": 0.0})

        new_results.extend(batch_results)
        done += len(batch)
        print(f"{done}/{total} ({100*done/total:.1f}%)", flush=True)

        # 每批后保存检查点
        all_done_ids = checkpoint["done_ids"] | {r['local_id'] for r in new_results if r.get('local_id')}
        all_results = checkpoint["results"] + new_results

        with open(args.checkpoint, 'w', encoding='utf-8') as f:
            json.dump({"done_ids": list(all_done_ids), "results": all_results}, f, ensure_ascii=False)

    print(f"\nProcessed {done} items in {time.time()-start_time:.1f}s", flush=True)
    print(f"Checkpoint saved: {args.checkpoint}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
