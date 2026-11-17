#!/usr/bin/env python3
"""对 responses.jsonl 跑 ragas LLM 裁判指标（对照 evalset.jsonl）。

responses.jsonl 每行：
  {"query_id": "q0001", "response": "...", "retrieved_contexts": ["..."]}

使用 ragas >=0.4 新版指标（ragas.metrics.collections）：异步 + 限并发 +
单条 3 次指数退避重试 + 逐条增量落盘（中途崩溃不丢已完成分数）。
需要环境变量 OPENAI_API_KEY。
"""
import argparse
import asyncio
import json
import os
import statistics
import sys
from pathlib import Path

METRIC_SPECS = {
    "faithfulness": ("Faithfulness", ["user_input", "response", "retrieved_contexts"], False),
    "answer_relevancy": ("AnswerRelevancy", ["user_input", "response"], True),
    "context_precision": ("ContextPrecision", ["user_input", "reference", "retrieved_contexts"], False),
    "context_recall": ("ContextRecall", ["user_input", "reference", "retrieved_contexts"], False),
    "answer_correctness": ("AnswerCorrectness", ["user_input", "response", "reference"], True),
}


def load_jsonl(path):
    rows = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"{path}:{n}: JSON 格式错误：{e}")
    return rows


async def ascore_retry(metric, kwargs, attempts=3):
    last = None
    for i in range(attempts):
        try:
            return await metric.ascore(**kwargs)
        except Exception as e:  # 服务端抖动、结构化输出偶发校验失败
            last = e
            if i < attempts - 1:
                await asyncio.sleep(2 ** i)
    raise last


async def run(a):
    from openai import AsyncOpenAI
    from ragas.llms import llm_factory
    from ragas.embeddings import OpenAIEmbeddings
    import ragas.metrics.collections as mc

    chosen = [m.strip() for m in a.metrics.split(",") if m.strip()]
    bad = [m for m in chosen if m not in METRIC_SPECS]
    if bad:
        sys.exit(f"未知指标 {bad}；可选：{sorted(METRIC_SPECS)}")

    cache = None
    if a.cache_dir:
        from ragas.cache import DiskCacheBackend
        cache = DiskCacheBackend(cache_dir=a.cache_dir)

    client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=a.base_url or None)
    extra = json.loads(a.model_kwargs) if a.model_kwargs else {}
    llm = llm_factory(a.llm_model, client=client, cache=cache, **extra)
    embeddings = OpenAIEmbeddings(client=client, model=a.embed_model, cache=cache)

    evalset = {r["query_id"]: r for r in load_jsonl(a.evalset)}
    resp_rows = load_jsonl(a.responses)
    responses = [r for r in resp_rows if r.get("query_id") in evalset]
    skipped = len(resp_rows) - len(responses)
    if skipped:
        print(f"! {skipped} 行 response 的 query_id 在 evalset 中不存在，已跳过")
    if not responses:
        sys.exit("没有可打分的行：检查 evalset 与 responses 的 query_id 是否对齐")
    print(f"对 {len(responses)} 条回答打分，指标：{chosen}")

    metrics = {}
    for name in chosen:
        cls, _, needs_emb = METRIC_SPECS[name]
        kwargs = {"llm": llm}
        if needs_emb:
            kwargs["embeddings"] = embeddings
        metrics[name] = getattr(mc, cls)(**kwargs)

    sem = asyncio.Semaphore(a.concurrency)
    results = {name: [] for name in chosen}
    failures = []
    out_f = open(a.out, "w", encoding="utf-8") if a.out else None

    async def score_one(resp):
        ev = evalset[resp["query_id"]]
        fields = {
            "user_input": ev["query"],
            "response": resp.get("response", ""),
            "reference": ev.get("reference_answer") or "",
            "retrieved_contexts": resp.get("retrieved_contexts") or [],
        }
        row = {"query_id": resp["query_id"]}
        for name in chosen:
            _, needed, _ = METRIC_SPECS[name]
            missing = [f for f in needed if not fields[f]]
            if missing:
                failures.append((resp["query_id"], name, f"缺字段：{missing}"))
                continue
            async with sem:
                try:
                    r = await ascore_retry(metrics[name], {f: fields[f] for f in needed})
                    v = float(r.value)
                    results[name].append(v)
                    row[name] = v
                except Exception as e:
                    failures.append((resp["query_id"], name, f"{type(e).__name__}: {e}"))
        if out_f:
            out_f.write(json.dumps(row, ensure_ascii=False) + "\n")
            out_f.flush()

    await asyncio.gather(*(score_one(r) for r in responses))
    if out_f:
        out_f.close()

    print("\n| 指标 | n | 均值 | 标准差 | 失败数 |")
    print("|---|---|---|---|---|")
    for name in chosen:
        scores = results[name]
        fails = sum(1 for _, m, _ in failures if m == name)
        if not scores:
            print(f"| {name} | 0 | - | - | {fails} |")
            continue
        std = statistics.pstdev(scores) if len(scores) > 1 else 0.0
        print(f"| {name} | {len(scores)} | {statistics.mean(scores):.4f} | {std:.4f} | {fails} |")
    if failures:
        print(f"\n共 {len(failures)} 次失败；前 5 条：")
        for qid, m, err in failures[:5]:
            print(f"  {qid} [{m}]: {err[:160]}")
    if a.out:
        print(f"\n-> 逐条分数：{a.out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--evalset", required=True)
    ap.add_argument("--responses", required=True)
    ap.add_argument("--metrics", default="faithfulness,answer_relevancy", help="逗号分隔的指标名")
    ap.add_argument("--llm-model", default="gpt-4o-mini", help="裁判模型")
    ap.add_argument("--embed-model", default="text-embedding-3-small")
    ap.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL"))
    ap.add_argument("--model-kwargs", default=None, help='裁判模型参数 JSON，如 {"temperature":0}')
    ap.add_argument("--cache-dir", default=None, help="磁盘缓存目录，重复调用零成本")
    ap.add_argument("--concurrency", type=int, default=8, help="并发上限（实测端点 32 并发无衰减，可到 16-32）")
    ap.add_argument("--out", default=None, help="逐条分数 jsonl 输出路径（增量写）")
    a = ap.parse_args()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("未设置 OPENAI_API_KEY")
    asyncio.run(run(a))


if __name__ == "__main__":
    main()
