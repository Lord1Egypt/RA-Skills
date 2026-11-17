#!/usr/bin/env python3
"""arena_runner.py — one arena cycle across ALL configured models, in parallel.

Reads config.arena.models and runs model_runner.run_model_cycle for each on a
thread pool (cycles are IO-bound: venue REST + LLM HTTP). Every model is
isolated: own state/journal files, own lock, own failures. One model crashing
never blocks the others.

CLI: python3 arena_runner.py config.json
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import model_runner  # noqa: E402


def run_arena(config_path, out=sys.stdout):
    with open(config_path) as f:
        config = json.load(f)
    models = (config.get("arena") or {}).get("models") or []
    if not models:
        print(json.dumps({"error": "config.arena.models is empty"}), file=out)
        return {"models": [], "errors": ["no models configured"]}

    results = {}
    with ThreadPoolExecutor(max_workers=len(models)) as pool:
        futures = {pool.submit(model_runner.run_model_cycle,
                               config, config_path, m, None, None, open(os.devnull, "w")):
                   m.get("id") for m in models}
        for fut in as_completed(futures):
            model_id = futures[fut]
            try:
                results[model_id] = fut.result()
            except Exception as e:  # run_model_cycle never raises; belt+braces
                results[model_id] = {"model": model_id,
                                     "errors": ["runner: %s" % e]}
    summary = {"models": results,
               "errors": [e for r in results.values() for e in r.get("errors", [])]}
    print(json.dumps(summary, indent=2, default=str), file=out)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run one arena cycle for all models")
    parser.add_argument("config", help="path to config.json")
    args = parser.parse_args(argv)
    summary = run_arena(args.config)
    return 0 if not summary["errors"] else 2


if __name__ == "__main__":
    sys.exit(main())
