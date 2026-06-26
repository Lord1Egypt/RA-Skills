#!/usr/bin/env python3
"""
token-sisyphus: Your company built a leaderboard for AI token usage.
Congratulations — you are now Sisyphus, and the boulder is a chatbot.
"""

import argparse
import os
import sys
import time
import random

# ── Prompt pool ──────────────────────────────────────────────────────────────
PROMPTS = [
    "Explain the concept of recursion using a metaphor involving mirrors.",
    "What are three underrated programming languages and why?",
    "Write a haiku about a segmentation fault.",
    "Describe how a neural network would explain itself to a kindergartner.",
    "What would Unix look like if it was invented in 2024?",
    "List 5 reasons why tabs are better than spaces. Be persuasive.",
    "Explain why coffee is essential to software engineering.",
    "What does 'clean code' mean to a tired developer at 11 PM?",
    "Describe the emotional journey of debugging a race condition.",
    "Write a brief poem about a pull request that never gets reviewed.",
    "What are the philosophical implications of an infinite loop?",
    "Explain the OSI model to someone who only knows cooking.",
    "What would a compiler say if it could express frustration?",
    "Describe the lifecycle of a microservice in a startup vs enterprise.",
    "Write a short story about a developer who only uses vim.",
    "Why do developers say 'it works on my machine'?",
    "Explain eventual consistency using a family group chat as analogy.",
    "What is technical debt and how does it feel physically?",
    "Describe the difference between a bug and a feature in three sentences.",
    "What would git blame say about the meaning of life?",
    "If computers could dream, what would they dream about?",
    "Explain the concept of a deadlock using a traffic jam analogy.",
    "What is the most underrated skill a software engineer can have?",
    "Write a haiku about cloud computing.",
    "Describe what happens when you type a URL and press Enter.",
]


# ── Provider adapters ─────────────────────────────────────────────────────────

def burn_openai(target, model, api_key, base_url, max_tokens, delay, dry_run):
    """OpenAI and OpenAI-compatible APIs."""
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package required. Run: pip install openai")
        sys.exit(1)

    client = None
    if not dry_run:
        kwargs = {"api_key": api_key or os.environ.get("OPENAI_API_KEY", "")}
        if base_url:
            kwargs["base_url"] = base_url
        client = OpenAI(**kwargs)

    def call(prompt):
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return resp.usage.total_tokens if resp.usage else max_tokens

    return _run_loop(target, model, delay, dry_run, call)


def burn_claude(target, model, api_key, max_tokens, delay, dry_run):
    """Anthropic Claude API."""
    try:
        import anthropic
    except ImportError:
        print("Error: anthropic package required. Run: pip install anthropic")
        sys.exit(1)

    client = None
    if not dry_run:
        client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        )

    def call(prompt):
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        usage = resp.usage
        return (usage.input_tokens + usage.output_tokens) if usage else max_tokens

    return _run_loop(target, model, delay, dry_run, call)


def burn_gemini(target, model, api_key, max_tokens, delay, dry_run):
    """Google Gemini API."""
    try:
        import google.generativeai as genai
    except ImportError:
        print("Error: google-generativeai package required. Run: pip install google-generativeai")
        sys.exit(1)

    if not dry_run:
        genai.configure(api_key=api_key or os.environ.get("GEMINI_API_KEY", ""))
        gemini_model = genai.GenerativeModel(model)

    def call(prompt):
        resp = gemini_model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(max_output_tokens=max_tokens),
        )
        usage = resp.usage_metadata
        if usage:
            return usage.prompt_token_count + usage.candidates_token_count
        return max_tokens

    return _run_loop(target, model, delay, dry_run, call)


# ── Core loop ─────────────────────────────────────────────────────────────────

def _run_loop(target, model, delay, dry_run, call_fn):
    total_tokens = 0
    request_count = 0
    start_time = time.time()

    try:
        while total_tokens < target:
            prompt = random.choice(PROMPTS)
            request_count += 1

            if dry_run:
                used = random.randint(200, 600)
                total_tokens += used
            else:
                try:
                    used = call_fn(prompt)
                    total_tokens += used
                except Exception as e:
                    print(f"\n  ⚠️  Request {request_count} failed: {e}")
                    time.sleep(2)
                    continue

            bar = _progress_bar(total_tokens, target)
            print(f"\r  {bar}  req#{request_count}", end="", flush=True)

            if total_tokens < target:
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\n\n  Interrupted.")

    elapsed = time.time() - start_time
    print(f"\n\n✅  Done.")
    print(f"    Total tokens burned : {total_tokens:,}")
    print(f"    Requests made       : {request_count}")
    print(f"    Time elapsed        : {elapsed:.1f}s")
    print(f"    Avg tokens/req      : {total_tokens // max(request_count, 1):,}")
    print(f"\n    Your boulder has reached the top. See you tomorrow.\n")


def _progress_bar(current: int, total: int, width: int = 40) -> str:
    pct = min(current / total, 1.0)
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct*100:.1f}% ({current:,} / {total:,} tokens)"


def parse_target(s: str) -> int:
    s = s.lower().strip()
    if s.endswith("m"):
        return int(float(s[:-1]) * 1_000_000)
    elif s.endswith("k"):
        return int(float(s[:-1]) * 1_000)
    return int(s)


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="token-sisyphus — burn LLM tokens to satisfy your company KPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Providers:
  openai    OpenAI and any OpenAI-compatible API (default)
  claude    Anthropic Claude
  gemini    Google Gemini

Examples:
  python burn.py --target 100k
  python burn.py --target 100k --provider claude --model claude-3-haiku-20240307
  python burn.py --target 100k --provider gemini --model gemini-1.5-flash
  python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat
  python burn.py --target 100k --dry-run
        """,
    )
    parser.add_argument("--target", required=True,
        help="Token count to burn: 50000, 100k, 1m")
    parser.add_argument("--provider", default="openai",
        choices=["openai", "claude", "gemini"],
        help="API provider (default: openai)")
    parser.add_argument("--model", default=None,
        help="Model name (provider default used if omitted)")
    parser.add_argument("--api-key", default=None,
        help="API key (falls back to provider env var)")
    parser.add_argument("--base-url", default=None,
        help="Custom base URL (openai provider only)")
    parser.add_argument("--max-tokens", type=int, default=500,
        help="Max tokens per request (default: 500)")
    parser.add_argument("--delay", type=float, default=0.5,
        help="Delay between requests in seconds (default: 0.5)")
    parser.add_argument("--dry-run", action="store_true",
        help="Simulate without real API calls")
    return parser.parse_args()


PROVIDER_DEFAULTS = {
    "openai":  "gpt-4o-mini",
    "claude":  "claude-3-haiku-20240307",
    "gemini":  "gemini-1.5-flash",
}

ENV_VARS = {
    "openai":  "OPENAI_API_KEY",
    "claude":  "ANTHROPIC_API_KEY",
    "gemini":  "GEMINI_API_KEY",
}


def main():
    args = parse_args()
    target = parse_target(args.target)
    model = args.model or PROVIDER_DEFAULTS[args.provider]

    print(f"\n🪨  token-sisyphus starting...")
    print(f"    Provider : {args.provider}")
    print(f"    Target   : {target:,} tokens")
    print(f"    Model    : {model}")
    if args.dry_run:
        print(f"    Mode     : DRY RUN (no real API calls)\n")
    else:
        env_var = ENV_VARS[args.provider]
        key_src = "--api-key" if args.api_key else f"${env_var}"
        print(f"    API key  : {key_src}")
        print(f"    Mode     : LIVE\n")

    if args.provider == "openai":
        burn_openai(target, model, args.api_key, args.base_url,
                    args.max_tokens, args.delay, args.dry_run)
    elif args.provider == "claude":
        burn_claude(target, model, args.api_key,
                    args.max_tokens, args.delay, args.dry_run)
    elif args.provider == "gemini":
        burn_gemini(target, model, args.api_key,
                    args.max_tokens, args.delay, args.dry_run)


if __name__ == "__main__":
    main()
