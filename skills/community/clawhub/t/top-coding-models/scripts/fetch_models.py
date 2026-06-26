#!/usr/bin/env python3
"""
Fetch top 20 agentic coding models — live data cross-referenced from:
  1. BenchLM coding leaderboard API  (benchmark scores + category rankings)
  2. OpenRouter models API            (live pricing, context window, max output tokens)

Usage:
    python3 fetch_models.py [--top N]   (default N=20)
    python3 fetch_models.py --json      (raw JSON output instead of markdown)
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime

# ---------------------------------------------------------------------------
# Known OpenRouter model ID mappings for top coding models.
# These supplement fuzzy name-matching when the model appears under a slightly
# different name in OpenRouter's catalogue.
# ---------------------------------------------------------------------------
OR_ID_HINTS = {
    "claude mythos preview": "anthropic/claude-mythos-preview",
    "claude opus 4.6": "anthropic/claude-opus-4.6",
    "claude sonnet 4.6": "anthropic/claude-sonnet-4.6",
    "claude haiku 4.6": "anthropic/claude-haiku-4.6",
    "claude opus 4.5": "anthropic/claude-opus-4.5",
    "claude sonnet 4.5": "anthropic/claude-sonnet-4.5",
    "claude 4 sonnet": "anthropic/claude-sonnet-4",
    "claude 4 opus": "anthropic/claude-opus-4",
    "claude 4.1 opus": "anthropic/claude-opus-4.1",
    "gemini 3.1 pro": "google/gemini-3.1-pro-preview",
    "gemini 3.1 pro preview custom tools": "google/gemini-3.1-pro-preview-customtools",
    "gemini 3 pro": "google/gemini-3.1-pro-preview",
    "gemini 3 pro deep think": "google/gemini-3-pro-deep-think",
    "gemini 3 flash": "google/gemini-3-flash-preview",
    "gemini 2.5 pro": "google/gemini-2.5-pro",
    "gemini 2.5 flash": "google/gemini-2.5-flash",
    "gpt-5.4": "openai/gpt-5.4",
    "gpt-5.3 codex": "openai/gpt-5.3-codex",
    "gpt-5.3 chat": "openai/gpt-5.3-chat",
    "gpt-5.2": "openai/gpt-5.2",
    "gpt-5.2-codex": "openai/gpt-5.2-codex",
    "gpt-5.1": "openai/gpt-5.1",
    "gpt-5": "openai/gpt-5",
    "gpt-5 (high)": "openai/gpt-5",
    "gpt-5 (medium)": "openai/gpt-5",
    "gpt-4.1": "openai/gpt-4.1",
    "gpt-4.1 mini": "openai/gpt-4.1-mini",
    "gpt oss 120b": "openai/gpt-oss-120b",
    "gpt oss 20b": "openai/gpt-oss-20b",
    "o3": "openai/o3",
    "o3-mini": "openai/o3-mini",
    "o4-mini": "openai/o4-mini",
    "o3-pro": "openai/o3-pro",
    "o1": "openai/o1",
    "o1-preview": "openai/o1-preview",
    "grok 4.1": "x-ai/grok-4.1",
    "grok 4": "x-ai/grok-4",
    "grok 4.1 fast": "x-ai/grok-4.1-fast",
    "grok 3": "x-ai/grok-3",
    "grok 3 [beta]": "x-ai/grok-3-beta",
    "grok 3 mini": "x-ai/grok-3-mini",
    "grok code fast 1": "x-ai/grok-code-fast-1",
    "kimi k2.5 (reasoning)": "moonshotai/kimi-k2-thinking",
    "kimi k2.5": "moonshotai/kimi-k2.5",
    "kimi k2 thinking": "moonshotai/kimi-k2-thinking",
    "kimi k2": "moonshotai/kimi-k2",
    "glm-5 (reasoning)": "z-ai/glm-5-reasoning",
    "glm-5.1": "z-ai/glm-5.1",
    "glm-5": "z-ai/glm-5",
    "glm-4.7": "z-ai/glm-4.7",
    "deepseek v3.2 (thinking)": "deepseek/deepseek-v3.2-thinking",
    "deepseek v3.2": "deepseek/deepseek-v3.2-20251201",
    "deepseek coder 2.0": "deepseek/deepseek-coder-v2",
    "deepseek v3 0324": "deepseek/deepseek-v3",
    "deepseek-r1": "deepseek/deepseek-r1",
    "deepseekmath v2": "deepseek/deepseekmath-v2",
    "qwen3 coder": "qwen/qwen3-coder",
    "qwen3.5 397b (reasoning)": "qwen/qwen3.5-397b-reasoning",
    "qwen3.5 397b": "qwen/qwen3.5-397b",
    "qwen3.5-122b-a10b": "qwen/qwen3.5-122b-a10b",
    "qwen3.5-35b-a3b": "qwen/qwen3.5-35b-a3b",
    "qwen3.5-27b": "qwen/qwen3.5-27b",
    "qwen3.6 plus": "qwen/qwen3.6-plus-04-02",
    "qwen2.5-1m": "qwen/qwen2.5-1m",
    "llama 4 maverick": "meta-llama/llama-4-maverick",
    "llama 4 scout": "meta-llama/llama-4-scout",
    "llama 4 behemoth": "meta-llama/llama-4-behemoth",
    "microsoft phi-4": "microsoft/phi-4",
    "phi-4 reasoning": "microsoft/phi-4-reasoning",
    "mimo v2 pro": "xiaomi/mimo-v2-pro-20260318",
    "mimo-v2-flash": "xiaomi/mimo-v2-flash",
    "minimax m2.7": "minimax/minimax-m2.7-20260318",
    "minimax m2.5": "minimax/minimax-m2.5-20260211",
    "codestral 2508": "mistralai/codestral-2508",
    "codestral 2501": "mistralai/codestral-2501",
    "mistral large": "mistralai/mistral-large",
}

BENCHMARKS_URL = "https://benchlm.ai/api/data/leaderboard?category=coding"
OPENROUTER_URL = "https://openrouter.ai/api/v1/models"


def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "OpenCode-TopCodingModels-Skill/1.0",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code} fetching {url}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}", file=sys.stderr)
        sys.exit(1)


def normalize(s):
    """Lowercase, strip spaces, dashes, dots — for fuzzy name matching."""
    return (
        s.lower()
        .replace("-", "")
        .replace(" ", "")
        .replace("_", "")
        .replace(".", "")
        .replace("(", "")
        .replace(")", "")
    )


def build_or_index(or_models):
    """Build a lookup dict: normalized_key -> OR model dict."""
    index = {}
    for m in or_models:
        # Index by full ID
        index[normalize(m["id"])] = m
        # Index by name (strip provider prefix like "Anthropic: ")
        clean_name = m["name"]
        for prefix in [
            "Anthropic: ",
            "OpenAI: ",
            "Google: ",
            "Meta: ",
            "xAI: ",
            "Mistral: ",
            "Microsoft: ",
            "MoonshotAI: ",
            "DeepSeek: ",
            "Qwen: ",
            "Alibaba: ",
            "Z.AI: ",
            "Xiaomi: ",
            "MiniMax: ",
        ]:
            clean_name = clean_name.replace(prefix, "")
        index[normalize(clean_name)] = m
    return index


def find_or_model(bench_name, or_index, or_models_by_id):
    """Find the best matching OpenRouter model for a BenchLM model name."""
    name_lower = bench_name.lower().strip()

    # 1. Try known hints first (exact lowercase match)
    hint_id = OR_ID_HINTS.get(name_lower)
    if hint_id and normalize(hint_id) in or_index:
        return or_index[normalize(hint_id)]
    # Also check if the ID itself exists directly
    if hint_id and hint_id in or_models_by_id:
        return or_models_by_id[hint_id]

    # 2. Exact normalized name match
    key = normalize(bench_name)
    if key in or_index:
        return or_index[key]

    # 3. Partial substring match (longer key wins)
    candidates = []
    for idx_key, model in or_index.items():
        if key in idx_key or idx_key in key:
            candidates.append((len(idx_key), model))
    if candidates:
        candidates.sort(key=lambda x: -x[0])
        return candidates[0][1]

    return None


def format_price(price_per_1m, from_bench=False):
    if price_per_1m is None:
        return "N/A"
    if price_per_1m == 0:
        return "**Free**"
    return f"${price_per_1m:.2f}"


def format_number(n):
    if n is None or n == "" or n == "?":
        return "?"
    try:
        v = int(n)
        if v >= 1_000_000:
            return f"{v // 1_000_000}M"
        if v >= 1_000:
            return f"{v // 1_000}K"
        return str(v)
    except (ValueError, TypeError):
        return str(n)


def main():
    top_n = 20
    raw_json = False

    for arg in sys.argv[1:]:
        if arg == "--json":
            raw_json = True
        elif arg.startswith("--top"):
            try:
                top_n = (
                    int(arg.split("=")[1])
                    if "=" in arg
                    else int(sys.argv[sys.argv.index(arg) + 1])
                )
            except (ValueError, IndexError):
                pass

    today = datetime.now().strftime("%B %d, %Y")

    # ------------------------------------------------------------------ #
    # 1. Fetch data
    # ------------------------------------------------------------------ #
    print("Fetching BenchLM coding leaderboard...", file=sys.stderr)
    bench_data = fetch_json(BENCHMARKS_URL)
    bench_models = bench_data.get("models", [])[:top_n]
    bench_updated = bench_data.get("lastUpdated", "unknown")

    print("Fetching OpenRouter models catalogue...", file=sys.stderr)
    or_data = fetch_json(OPENROUTER_URL)
    or_models = or_data.get("data", [])

    or_index = build_or_index(or_models)
    or_by_id = {m["id"]: m for m in or_models}

    # ------------------------------------------------------------------ #
    # 2. Cross-reference and enrich
    # ------------------------------------------------------------------ #
    results = []
    for bm in bench_models:
        name = bm.get("model", "Unknown")
        creator = bm.get("creator", "?")
        src_type = bm.get("sourceType", "?")
        coding_score = bm.get("categoryScores", {}).get("coding")
        agentic_score = bm.get("categoryScores", {}).get("agentic")
        bench_input = bm.get("inputPrice")
        bench_output = bm.get("outputPrice")

        or_match = find_or_model(name, or_index, or_by_id)

        if or_match:
            pricing = or_match.get("pricing", {})
            inp_raw = float(pricing.get("prompt", 0) or 0)
            out_raw = float(pricing.get("completion", 0) or 0)
            inp_1m = inp_raw * 1_000_000
            out_1m = out_raw * 1_000_000
            ctx = or_match.get("context_length")
            max_out = or_match.get("top_provider", {}).get("max_completion_tokens")
            or_id = or_match["id"]
            supported = or_match.get("supported_parameters", [])
            tools_ok = "tools" in supported
            structured_ok = (
                "structured_outputs" in supported or "response_format" in supported
            )
        else:
            # Fall back to BenchLM pricing data
            inp_1m = bench_input if bench_input is not None else None
            out_1m = bench_output if bench_output is not None else None
            ctx = None
            max_out = None
            or_id = None
            tools_ok = None
            structured_ok = None

        results.append(
            {
                "rank": bm.get("rank", len(results) + 1),
                "name": name,
                "creator": creator,
                "source_type": src_type,
                "coding_score": coding_score,
                "agentic_score": agentic_score,
                "inp_1m": inp_1m,
                "out_1m": out_1m,
                "context_length": ctx,
                "max_output_tokens": max_out,
                "openrouter_id": or_id,
                "tools_support": tools_ok,
                "structured_outputs": structured_ok,
            }
        )

    # ------------------------------------------------------------------ #
    # 3. Output
    # ------------------------------------------------------------------ #
    if raw_json:
        print(json.dumps(results, indent=2))
        return

    # Markdown output
    print(f"# Top {top_n} Agentic Coding Models — Live Rankings")
    print()
    print(f"**Data fetched: {today}** | Benchmarks updated: {bench_updated}")
    print()
    print("**Sources:**")
    print(
        f"- [BenchLM Coding Leaderboard](https://benchlm.ai/coding) — SWE-bench Pro + LiveCodeBench (50/50 weighted)"
    )
    print(
        f"- [OpenRouter Models API](https://openrouter.ai/api/v1/models) — Live pricing & token limits"
    )
    print()
    print("---")
    print()

    # Main table
    header = (
        "| # | Model | Provider | Type | Coding Score | Agentic Score | "
        "Input $/1M | Output $/1M | Context | Max Output | OpenRouter ID | Tools | Structured |"
    )
    sep = "|---|-------|----------|------|:---:|:---:|---:|---:|---:|---:|---|:---:|:---:|"
    print(header)
    print(sep)

    free_models = []
    best_value_candidates = []

    for r in results:
        rank = r["rank"]
        name = r["name"]
        creator = r["creator"]
        src_type = "Open" if "Open" in r["source_type"] else "Prop"
        coding = f"{r['coding_score']:.1f}%" if r["coding_score"] is not None else "—"
        agentic = (
            f"{r['agentic_score']:.1f}%" if r["agentic_score"] is not None else "—"
        )
        inp = format_price(r["inp_1m"])
        out = format_price(r["out_1m"])
        ctx = format_number(r["context_length"])
        max_out = format_number(r["max_output_tokens"])
        or_id = f"`{r['openrouter_id']}`" if r["openrouter_id"] else "—"
        tools = (
            "✓" if r["tools_support"] else ("?" if r["tools_support"] is None else "✗")
        )
        struct = (
            "✓"
            if r["structured_outputs"]
            else ("?" if r["structured_outputs"] is None else "✗")
        )

        print(
            f"| {rank} | {name} | {creator} | {src_type} | {coding} | {agentic} | {inp} | {out} | {ctx} | {max_out} | {or_id} | {tools} | {struct} |"
        )

        # Track free models
        if (r["inp_1m"] == 0 or r["inp_1m"] is None) and r["openrouter_id"]:
            free_models.append(r["name"])

        # Track best value (coding score per dollar)
        if r["coding_score"] and r["inp_1m"] is not None and r["inp_1m"] > 0:
            total_cost = r["inp_1m"] + (r["out_1m"] or 0)
            value = r["coding_score"] / total_cost if total_cost > 0 else 0
            best_value_candidates.append((value, r))

    print()

    # ------------------------------------------------------------------ #
    # 4. Insights
    # ------------------------------------------------------------------ #
    print("---")
    print()
    print("## Key Insights")
    print()

    if results:
        top = results[0]
        print(
            f"**#1 Best Coding Model:** {top['name']} by {top['creator']} "
            f"({top['coding_score']:.1f}% coding score, {top['agentic_score']:.1f}% agentic score)"
        )

    # Best free
    if free_models:
        print(f"**Best Free Models (via OpenRouter):** {', '.join(free_models[:4])}")

    # Best value
    if best_value_candidates:
        best_value_candidates.sort(reverse=True)
        bv = best_value_candidates[0][1]
        total = (bv["inp_1m"] or 0) + (bv["out_1m"] or 0)
        print(
            f"**Best Value (score/cost):** {bv['name']} — "
            f"{bv['coding_score']:.1f}% score at ${total:.2f}/1M tokens combined"
        )

    # Cheapest proprietary with high score
    strong_cheap = [
        r
        for r in results
        if r["inp_1m"] is not None
        and 0 < r["inp_1m"] <= 1.0
        and r["coding_score"]
        and r["coding_score"] >= 60
    ]
    if strong_cheap:
        sc = strong_cheap[0]
        print(
            f"**Best Budget Proprietary:** {sc['name']} — "
            f"{sc['coding_score']:.1f}% score at ${sc['inp_1m']:.2f}/${sc['out_1m']:.2f} per 1M tokens"
        )

    print()

    # ------------------------------------------------------------------ #
    # 5. Agentic IDE Compatibility
    # ------------------------------------------------------------------ #
    print("---")
    print()
    print("## Agentic IDE Compatibility")
    print()
    print(
        "All models with an **OpenRouter ID** are accessible in every major agentic coding IDE via the OpenRouter unified API endpoint:"
    )
    print()
    print("```")
    print("Base URL: https://openrouter.ai/api/v1")
    print("Auth:     Authorization: Bearer <OPENROUTER_API_KEY>")
    print("```")
    print()
    print("| IDE / Tool | Integration Method |")
    print("|---|---|")
    print(
        "| **Claude Code** | `ANTHROPIC_BASE_URL=https://openrouter.ai/api/v1` + OR key |"
    )
    print(
        "| **OpenCode** | Provider: `openrouter` in `~/.config/opencode/config.json` |"
    )
    print("| **Cursor** | Settings → Models → OpenAI-compatible → paste OR base URL |")
    print("| **Windsurf** | Add custom provider with OR base URL + model ID |")
    print(
        "| **Cline / Roo Code** | Provider: `OpenAI Compatible`, base URL + model ID |"
    )
    print(
        "| **Aider** | `--openai-api-base https://openrouter.ai/api/v1 --model <id>` |"
    )
    print("| **Continue.dev** | Custom LLM provider with OR base URL |")
    print(
        "| **GitHub Copilot** | Via Azure OpenAI passthrough or compatible extensions |"
    )
    print("| **Antigravity / Phi** | Use OpenAI SDK, point to OR base URL |")
    print()
    print(
        "> **Tip:** For free-tier models, use the `:free` suffixed model ID on OpenRouter."
    )
    print(
        "> Models with `Tools ✓` support function calling required by agentic frameworks."
    )
    print()

    # ------------------------------------------------------------------ #
    # 6. OpenRouter usage snippet
    # ------------------------------------------------------------------ #
    print("---")
    print()
    print("## Quick Setup Snippet (Python)")
    print()
    if results and results[0]["openrouter_id"]:
        top_id = results[0]["openrouter_id"]
    else:
        top_id = "anthropic/claude-sonnet-4.6"
    print("```python")
    print("from openai import OpenAI")
    print()
    print("client = OpenAI(")
    print('    base_url="https://openrouter.ai/api/v1",')
    print('    api_key="<OPENROUTER_API_KEY>",')
    print(")")
    print()
    print(f"response = client.chat.completions.create(")
    print(f'    model="{top_id}",   # swap for any model ID above')
    print(
        f'    messages=[{{"role": "user", "content": "Write a Python async web scraper"}}],'
    )
    print(f")")
    print("print(response.choices[0].message.content)")
    print("```")
    print()
    print("---")
    print()
    print(f"*Generated by OpenCode `top-coding-models` skill | {today}*")


if __name__ == "__main__":
    main()
