#!/usr/bin/env python3
"""对 evalset 每个问题跑检索，产出 runs.jsonl（IR 层输入）与 responses.jsonl（ragas 层骨架）。

三种模式：
  --mode bm25   内置词面 BM25，直接检索 chunks.jsonl（基线/CI/冒烟用，零依赖离线可跑）
  --mode api    调用被测检索 HTTP API：POST --url 模板体，按 json-path 取排序结果
  --mode cmd    每条问题执行 --command（含 {query} 占位符），stdout 输出 JSON
                {"chunk_ids": [...], "texts": [...]}  # texts 可省略

输出：
  runs.jsonl      {"query_id","chunk_ids"}      —— ir_metrics.py 输入
  responses.jsonl {"query_id","response","retrieved_contexts"} —— ragas_eval.py 输入；
                  response 默认留空，用 --answers answers.jsonl（{"query_id","response"}）回填

api 模式响应解析：--hits-path data.hits 点路径定位列表，--id-field / --text-field 取字段。
"""
import argparse
import json
import math
import re
import subprocess
import sys
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def load_jsonl(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def toks(s):
    return re.findall(r"[a-zA-Z0-9]+|[\u4e00-\u9fff]", s.lower())


class Bm25:
    def __init__(self, corpus):
        self.corpus = corpus
        self.N = len(corpus)
        self.df = Counter()
        self.tf = []
        for c in corpus:
            t = Counter(toks(c["text"]))
            self.tf.append(t)
            for k in t:
                self.df[k] += 1
        self.avg = sum(sum(t.values()) for t in self.tf) / max(self.N, 1)

    def rank(self, query):
        q = Counter(toks(query))
        scores = []
        for i, t in enumerate(self.tf):
            s = 0.0
            for term, n in q.items():
                if term not in t:
                    continue
                idf = math.log(1 + (self.N - self.df[term] + .5) / (self.df[term] + .5))
                s += idf * t[term] * 2.2 / (t[term] + 1.2 * (0.25 + 0.75 * sum(t.values()) / self.avg))
            scores.append((s, i))
        scores.sort(reverse=True)
        return [self.corpus[i]["chunk_id"] for _, i in scores]


def dot_get(obj, path):
    for part in path.split("."):
        if isinstance(obj, list):
            obj = obj[int(part)]
        else:
            obj = obj[part]
    return obj


def api_search(url, template, headers, query, timeout):
    body = json.dumps({k: (v.replace("{query}", query) if isinstance(v, str) else v)
                       for k, v in template.items()}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--evalset", required=True)
    ap.add_argument("--mode", required=True, choices=["bm25", "api", "cmd"])
    ap.add_argument("--chunks", help="chunks.jsonl（bm25 必需；提供后 responses 带上检索文本）")
    ap.add_argument("--url", help="api 模式检索端点")
    ap.add_argument("--template", default='{"query": "{query}"}', help="请求体 JSON 模板，{query} 占位")
    ap.add_argument("--headers", default="{}", help="附加请求头 JSON")
    ap.add_argument("--hits-path", default="hits", help="响应中排序结果列表的点路径，如 data.results")
    ap.add_argument("--id-field", default="chunk_id")
    ap.add_argument("--text-field", default="text")
    ap.add_argument("--command", help="cmd 模式命令模板，含 {query} 占位，stdout 须为 JSON")
    ap.add_argument("--k", type=int, default=10, help="截断到 top-K（要 ≥ ir_metrics 的最大评估 K）")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=30)
    ap.add_argument("--out-runs", default="runs.jsonl")
    ap.add_argument("--out-responses", default=None, help="给出该路径则同时产出 responses.jsonl 骨架")
    ap.add_argument("--answers", default=None, help="answers.jsonl（{query_id,response}），回填 response 字段")
    a = ap.parse_args()

    evalset = load_jsonl(a.evalset)
    if not evalset:
        sys.exit("evalset 为空")
    chunks = load_jsonl(a.chunks) if a.chunks else []
    id2text = {c["chunk_id"]: c["text"] for c in chunks}

    bm25 = Bm25(chunks) if a.mode == "bm25" else None
    if a.mode == "bm25" and not chunks:
        sys.exit("bm25 模式需要 --chunks")

    def run_one(row):
        qid, query = row["query_id"], row["query"]
        if a.mode == "bm25":
            top = bm25.rank(query)[:a.k]
            return qid, top, [id2text.get(t, "") for t in top]
        if a.mode == "api":
            resp = api_search(a.url, json.loads(a.template), json.loads(a.headers), query, a.timeout)
            hits = dot_get(resp, a.hits_path)
            top = [h[a.id_field] for h in hits][:a.k]
            texts = [h.get(a.text_field, id2text.get(t, "")) for h, t in zip(hits, top)]
            return qid, top, texts[:a.k]
        out = subprocess.run(a.command.replace("{query}", query), shell=True,
                             capture_output=True, text=True, timeout=a.timeout)
        if out.returncode != 0:
            raise RuntimeError(f"cmd 退出码 {out.returncode}: {out.stderr[:200]}")
        payload = json.loads(out.stdout)
        top = payload["chunk_ids"][:a.k]
        return qid, top, payload.get("texts") or [id2text.get(t, "") for t in top]

    results, errors = {}, []
    with ThreadPoolExecutor(max_workers=a.concurrency if a.mode != "cmd" else 1) as ex:
        futs = {ex.submit(run_one, r): r["query_id"] for r in evalset}
        for fut, qid in futs.items():
            try:
                results[qid] = fut.result()
            except Exception as e:
                errors.append((qid, f"{type(e).__name__}: {str(e)[:200]}"))

    answers = {}
    if a.answers:
        answers = {r["query_id"]: r.get("response", "") for r in load_jsonl(a.answers)}

    order = [r["query_id"] for r in evalset]
    with open(a.out_runs, "w", encoding="utf-8") as f:
        for qid in order:
            if qid in results:
                f.write(json.dumps({"query_id": qid, "chunk_ids": results[qid][1]}, ensure_ascii=False) + "\n")
    print(f"runs -> {a.out_runs}（{len(results)}/{len(order)}）")
    if a.out_responses:
        with open(a.out_responses, "w", encoding="utf-8") as f:
            for qid in order:
                if qid not in results:
                    continue
                _, _, texts = results[qid]
                f.write(json.dumps({"query_id": qid, "response": answers.get(qid, ""),
                                    "retrieved_contexts": [t for t in texts if t]}, ensure_ascii=False) + "\n")
        miss = len(results) - sum(1 for q in order if q in answers)
        print(f"responses -> {a.out_responses}（response 待回填 {miss} 条）")
    if errors:
        print(f"! {len(errors)} 条失败；前 5 条：")
        for qid, e in errors[:5]:
            print(f"  {qid}: {e}")
        sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
