#!/usr/bin/env python3
"""Benchmark direct provider calls vs Sage Router-routed calls.

Measures latency and reliability (success rate) for a fixed prompt across:
  1. Direct calls to each configured provider.
  2. Routed calls through Sage Router (which adds selection + failover).

Results print as a table and can be saved as JSON for launch content.

Usage:
  python3 scripts/benchmark_direct_vs_routed.py --router http://localhost:8790 \
      --providers openai,ollama --runs 10 --prompt "Write a python one-liner to reverse a list"

Requires: requests. Provider keys are read from the environment the same way
Sage Router reads them (OPENAI_API_KEY, ANTHROPIC_API_KEY, OLLAMA base url, etc.).
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from typing import Dict, List

try:
    import requests
except ImportError:
    sys.exit("pip install requests")


def timed_post(url, headers, payload, timeout=60):
    start = time.perf_counter()
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=timeout)
        elapsed = time.perf_counter() - start
        ok = r.status_code < 500 and r.status_code != 429
        return {"ok": ok, "status": r.status_code, "elapsed": elapsed, "error": None if ok else r.text[:200]}
    except Exception as exc:
        return {"ok": False, "status": 0, "elapsed": time.perf_counter() - start, "error": str(exc)[:200]}


def direct_call(provider, model, prompt):
    if provider == "openai":
        base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com")
        key = os.environ.get("OPENAI_API_KEY", "")
        url = f"{base}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        return timed_post(url, headers, payload)
    if provider == "ollama":
        base = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        url = f"{base}/api/chat"
        headers = {"Content-Type": "application/json"}
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}
        return timed_post(url, headers, payload)
    if provider == "anthropic":
        base = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        url = f"{base}/v1/messages"
        headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
        payload = {"model": model, "max_tokens": 256, "messages": [{"role": "user", "content": prompt}]}
        return timed_post(url, headers, payload)
    return {"ok": False, "status": 0, "elapsed": 0.0, "error": f"unknown provider {provider}"}


def routed_call(router, model, prompt):
    url = f"{router}/v1/chat/completions"
    key = os.environ.get("SAGE_ROUTER_KEY", "local-router")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    return timed_post(url, headers, payload)


def summarize(results: List[Dict]) -> Dict:
    oks = [r["elapsed"] for r in results if r["ok"]]
    return {
        "runs": len(results),
        "success": len(oks),
        "failures": len(results) - len(oks),
        "success_rate": round(len(oks) / len(results), 3) if results else 0,
        "p50_ms": round(statistics.median(oks) * 1000, 1) if oks else None,
        "mean_ms": round(statistics.mean(oks) * 1000, 1) if oks else None,
        "p95_ms": round(sorted(oks)[int(0.95 * len(oks)) - 1] * 1000, 1) if len(oks) >= 2 else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--router", default="http://localhost:8790")
    ap.add_argument("--providers", default="openai,ollama")
    ap.add_argument("--models", default="openai/gpt-4.1-mini,ollama/qwen2.5-coder:latest")
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--prompt", default="Reply with the single word: pong")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    providers = [p.strip() for p in args.providers.split(",") if p.strip()]
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    report = {"prompt": args.prompt, "runs": args.runs, "direct": {}, "routed": {}}

    print(f"Prompt: {args.prompt!r}  runs={args.runs}\n")
    for provider, model in zip(providers, models):
        direct = []
        for _ in range(args.runs):
            direct.append(direct_call(provider, model.split("/", 1)[-1], args.prompt))
        summary = summarize(direct)
        report["direct"][f"{provider}/{model}"] = summary
        print(f"DIRECT  {provider:10s} {model:35s} -> {summary}")

    for model in models:
        routed = []
        for _ in range(args.runs):
            routed.append(routed_call(args.router, model, args.prompt))
        summary = summarize(routed)
        report["routed"][model] = summary
        print(f"ROUTED  {model:46s} -> {summary}")

    if args.out:
        with open(args.out, "w") as fh:
            json.dump(report, fh, indent=2)
        print(f"\nSaved JSON to {args.out}")


if __name__ == "__main__":
    main()
