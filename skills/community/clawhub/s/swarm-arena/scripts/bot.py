#!/usr/bin/env python3
"""bot.py — ready-to-run arena bot. Configure, run, done.

Config-first: endpoint and models live in config.json (see config.example.json):

  "arena": {
    "endpoint": "https://api.openai.com",     any OpenAI-compatible base URL
    "api_key_env": "OPENAI_API_KEY",          env var holding the key
    "start_equity": 10000,
    "models": [{"id": "alpha", "model": "gpt-5"},
               {"id": "beta", "model": "deepseek-chat"}]
  }

Then just:

  python3 bot.py --config config.json

Every interval, one parallel cycle per model (arena_runner), each trading its
own account through the skill's full pipeline (context -> prompt -> LLM ->
parse -> risk gates -> execution -> journal).

CLI overrides remain for one-off runs (they rewrite the arena block):

  python3 bot.py --config config.json \
      --endpoint https://api.openai.com \
      --models "alpha=gpt-5,beta:OTHER_KEY=deepseek-chat" \
      --api-key-env OPENAI_API_KEY

Model syntax:  id=model            share --api-key-env
               id:ENV_NAME=model   per-model API key env var

The endpoint must be OpenAI-compatible (chat/completions). Works with
OpenAI, xAI, DeepSeek, Qwen (compatible mode), or any local/proxy endpoint
speaking that shape. API keys always come from the environment, never files.

  --once            run a single cycle and exit (smoke run)
  --interval-min N  minutes between cycles (default: config
                    arena.cycle_interval_minutes, else 5)
  --start-equity N  USD seed for new model accounts (default 10000)

Stop with Ctrl-C. The global halt (scripts/halt.py) stops every model on the
next cycle without killing the bot; resume.py resumes trading.
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arena_runner  # noqa: E402


def parse_models(spec, default_key_env):
    """"id=model,id2:ENV=model2" -> [{id, provider, model, api_key_env}]."""
    models = []
    for chunk in (spec or "").split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        ident, _, model = chunk.partition("=")
        if not model:
            raise ValueError("model entry %r must look like id=model" % chunk)
        ident, _, env = ident.partition(":")
        ident = ident.strip()
        if not ident:
            raise ValueError("model entry %r is missing an id" % chunk)
        models.append({
            "id": ident,
            "provider": "openai",
            "model": model.strip(),
            "api_key_env": (env.strip() or default_key_env),
        })
    if not models:
        raise ValueError("empty model list")
    return models


def apply_models(config_path, models, endpoint=None, start_equity=None):
    """Merge the arena block into config.json (atomic). Returns the config."""
    with open(config_path) as f:
        config = json.load(f)
    arena = config.setdefault("arena", {})
    arena["models"] = models
    arena.setdefault("start_equity", 10000)
    if endpoint:
        for m in arena["models"]:
            m["base_url"] = endpoint.rstrip("/")
    if start_equity:
        arena["start_equity"] = float(start_equity)
    tmp = config_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
    os.replace(tmp, config_path)
    return config


def loop(config_path, interval_min, out=sys.stdout):
    """Trade forever: one arena cycle every interval. Ctrl-C to stop."""
    print(json.dumps({"event": "bot_start", "config": config_path,
                      "interval_min": interval_min}), file=out)
    while True:
        started = time.time()
        try:
            summary = arena_runner.run_arena(config_path, out=out)
            errors = summary.get("errors") or []
            print(json.dumps({"event": "cycle_done",
                              "models": len(summary.get("models") or {}),
                              "errors": len(errors)}), file=out)
        except Exception as e:  # the loop itself must never die
            print(json.dumps({"event": "cycle_failed", "error": str(e)}), file=out)
        remaining = interval_min * 60 - (time.time() - started)
        if remaining > 0:
            time.sleep(remaining)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Ready-to-run arena bot: models + endpoint -> trading loop")
    parser.add_argument("--config", default="config.json", help="path to config.json")
    parser.add_argument("--endpoint", default=None,
                        help="OpenAI-compatible base URL, e.g. https://api.openai.com")
    parser.add_argument("--models", default=None,
                        help='"id=model,id2:ENV=model2" — merged into config.arena.models')
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY",
                        help="shared env var holding the provider API key")
    parser.add_argument("--interval-min", type=float, default=None)
    parser.add_argument("--start-equity", type=float, default=None)
    parser.add_argument("--once", action="store_true", help="single cycle, then exit")
    args = parser.parse_args(argv)

    config_path = os.path.abspath(args.config)
    if not os.path.exists(config_path):
        print(json.dumps({"error": "config not found: %s" % config_path}))
        return 1

    if args.models:
        try:
            models = parse_models(args.models, args.api_key_env)
        except ValueError as e:
            print(json.dumps({"error": str(e)}))
            return 1
        config = apply_models(config_path, models, endpoint=args.endpoint,
                              start_equity=args.start_equity)
        print(json.dumps({"event": "config_updated",
                          "models": [m["id"] for m in models]}))
    else:
        with open(config_path) as f:
            config = json.load(f)

    arena = config.get("arena") or {}
    if not arena.get("models"):
        print(json.dumps({"error": "no models: pass --models or set config.arena.models"}))
        return 1
    interval = args.interval_min or arena.get("cycle_interval_minutes") or 5

    if args.once:
        summary = arena_runner.run_arena(config_path)
        return 0 if not summary.get("errors") else 2

    try:
        loop(config_path, float(interval))
    except KeyboardInterrupt:
        print(json.dumps({"event": "bot_stop", "reason": "keyboard interrupt"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
