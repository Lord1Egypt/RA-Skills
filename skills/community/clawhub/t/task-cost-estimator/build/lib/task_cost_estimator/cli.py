#!/usr/bin/env python3
"""
Task Cost Estimator — Before you start a task, find the most cost-effective AI model and estimated cost.

Usage:
  task-cost "Build a REST API with user auth in Python"
  task-cost "Write a 2000-word blog post about climate change"
  task-cost "Debug this recursive function that causes stack overflow"

Repo: github.com/minirr890112-byte/HermesMade
"""

import sys, re, json, os
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.hermes/task-cost-history.json")

# ── Model database (shared with api-cost) ──
MODELS = [
    {"name": "GPT-4o",           "provider": "OpenAI",   "in": 2.50,  "out": 10.00, "reasoning": 8, "coding": 8, "writing": 9,  "instruction": 9,  "ctx": 128000},
    {"name": "GPT-4o-mini",      "provider": "OpenAI",   "in": 0.15,  "out": 0.60,  "reasoning": 5, "coding": 5, "writing": 6,  "instruction": 7,  "ctx": 128000},
    {"name": "GPT-4.1",          "provider": "OpenAI",   "in": 2.00,  "out": 8.00,  "reasoning": 8, "coding": 9, "writing": 8,  "instruction": 9,  "ctx": 1000000},
    {"name": "GPT-4.1-mini",     "provider": "OpenAI",   "in": 0.40,  "out": 1.60,  "reasoning": 6, "coding": 7, "writing": 6,  "instruction": 8,  "ctx": 1000000},
    {"name": "o3",               "provider": "OpenAI",   "in": 10.00, "out": 40.00, "reasoning": 10,"coding": 9, "writing": 6,  "instruction": 7,  "ctx": 200000},
    {"name": "o4-mini",          "provider": "OpenAI",   "in": 1.10,  "out": 4.40,  "reasoning": 9, "coding": 8, "writing": 5,  "instruction": 6,  "ctx": 200000},
    {"name": "Claude Opus 4.7",  "provider": "Anthropic","in": 15.00, "out": 75.00, "reasoning": 9, "coding": 10,"writing": 9,  "instruction": 9,  "ctx": 200000},
    {"name": "Claude Sonnet 4.5","provider": "Anthropic","in": 3.00,  "out": 15.00, "reasoning": 8, "coding": 9, "writing": 8,  "instruction": 9,  "ctx": 200000},
    {"name": "Claude Haiku 4.5", "provider": "Anthropic","in": 0.80,  "out": 4.00,  "reasoning": 4, "coding": 7, "writing": 6,  "instruction": 7,  "ctx": 200000},
    {"name": "Gemini 2.5 Pro",   "provider": "Google",   "in": 1.25,  "out": 10.00, "reasoning": 8, "coding": 8, "writing": 7,  "instruction": 8,  "ctx": 1000000},
    {"name": "Gemini 2.5 Flash", "provider": "Google",   "in": 0.15,  "out": 0.60,  "reasoning": 5, "coding": 6, "writing": 5,  "instruction": 6,  "ctx": 1000000},
    {"name": "DeepSeek V4 Pro",  "provider": "DeepSeek", "in": 0.55,  "out": 2.19,  "reasoning": 9, "coding": 8, "writing": 7,  "instruction": 8,  "ctx": 1000000},
    {"name": "DeepSeek V4 Flash","provider": "DeepSeek", "in": 0.14,  "out": 0.28,  "reasoning": 6, "coding": 7, "writing": 6,  "instruction": 7,  "ctx": 1000000},
    {"name": "DeepSeek R1-0528", "provider": "DeepSeek", "in": 0.55,  "out": 2.19,  "reasoning": 10,"coding": 8, "writing": 5,  "instruction": 6,  "ctx": 128000},
    {"name": "Grok 3",           "provider": "xAI",      "in": 3.00,  "out": 15.00, "reasoning": 8, "coding": 7, "writing": 8,  "instruction": 8,  "ctx": 131072},
    {"name": "Grok 3 Mini",      "provider": "xAI",      "in": 0.30,  "out": 1.50,  "reasoning": 5, "coding": 6, "writing": 5,  "instruction": 6,  "ctx": 131072},
    {"name": "Mistral Large 2",  "provider": "Mistral",  "in": 2.00,  "out": 6.00,  "reasoning": 7, "coding": 8, "writing": 8,  "instruction": 8,  "ctx": 128000},
    {"name": "Mistral Small 3",  "provider": "Mistral",  "in": 0.10,  "out": 0.30,  "reasoning": 4, "coding": 6, "writing": 5,  "instruction": 6,  "ctx": 128000},
]

# ── Local / open-weight models (run on your hardware) ──
# Cost: electricity ($0.12/kWh) + GPU amortization ($2000/3yr) → hourly rate
# Token speed varies by model size and quantization
LOCAL_MODELS = [
    {"name": "Llama 3.1 8B (Q4)",     "provider": "Local", "in": 0.0, "out": 0.0, "reasoning": 5, "coding": 6, "writing": 6,  "instruction": 7,  "ctx": 8192,  "tokens_per_sec": 60, "cost_per_hour": 0.11},
    {"name": "Qwen2.5 32B (Q4)",      "provider": "Local", "in": 0.0, "out": 0.0, "reasoning": 7, "coding": 8, "writing": 7,  "instruction": 8,  "ctx": 8192,  "tokens_per_sec": 25, "cost_per_hour": 0.18},
    {"name": "DeepSeek R1 32B (Q4)",  "provider": "Local", "in": 0.0, "out": 0.0, "reasoning": 9, "coding": 8, "writing": 5,  "instruction": 7,  "ctx": 8192,  "tokens_per_sec": 20, "cost_per_hour": 0.18},
    {"name": "Mistral 7B (Q4)",       "provider": "Local", "in": 0.0, "out": 0.0, "reasoning": 4, "coding": 5, "writing": 5,  "instruction": 6,  "ctx": 8192,  "tokens_per_sec": 70, "cost_per_hour": 0.08},
    {"name": "Gemma 3 12B (Q4)",      "provider": "Local", "in": 0.0, "out": 0.0, "reasoning": 6, "coding": 6, "writing": 7,  "instruction": 7,  "ctx": 8192,  "tokens_per_sec": 40, "cost_per_hour": 0.14},
    {"name": "Llama 3.1 70B (Q4)",    "provider": "Local", "in": 0.0, "out": 0.0, "reasoning": 8, "coding": 8, "writing": 8,  "instruction": 8,  "ctx": 8192,  "tokens_per_sec": 12, "cost_per_hour": 0.30},
    {"name": "Qwen2.5 7B (Q8)",       "provider": "Local", "in": 0.0, "out": 0.0, "reasoning": 5, "coding": 6, "writing": 5,  "instruction": 6,  "ctx": 8192,  "tokens_per_sec": 55, "cost_per_hour": 0.10},
    {"name": "DeepSeek V3 (Q2)",      "provider": "Local", "in": 0.0, "out": 0.0, "reasoning": 8, "coding": 7, "writing": 6,  "instruction": 7,  "ctx": 4096,  "tokens_per_sec": 8,  "cost_per_hour": 0.50},
]

# ── Task profiling ──
# Keyword → (reasoning_need, coding_need, writing_need, complexity_multiplier)
TASK_SIGNALS = {
    # High reasoning / coding
    "debug":     (9, 8, 2, 0.8),  "fix bug":   (9, 8, 2, 0.8),
    "refactor":  (8, 9, 2, 1.0),  "implement": (8, 9, 3, 1.2),
    "algorithm": (10,9, 2, 1.0),  "optimize":  (9, 8, 2, 1.0),
    "architecture": (9,7,3,1.5),  "design system": (9,7,3,1.5),
    "database schema": (7,8,2,1.0), "sql": (7,8,2,1.0),
    "api":       (7, 9, 3, 1.0),  "rest":      (7, 9, 3, 1.0),
    "microservice":(8,8,3,1.3),   "deploy":    (7, 7, 3, 1.0),
    "security":  (8, 7, 3, 1.0),  "auth":      (7, 8, 3, 0.8),
    "test":      (6, 8, 2, 0.8),  "unit test": (6, 8, 2, 0.7),
    "code review":(7,7,2,0.8),

    # Writing
    "blog post": (4, 1, 9, 1.0),  "article":   (5, 1, 9, 1.0),
    "write":     (4, 2, 9, 1.2),  "essay":     (6, 1, 9, 0.8),
    "document":  (4, 2, 8, 1.2),  "summary":   (5, 1, 7, 0.5),
    "translate": (3, 1, 7, 0.8),  "rewrite":   (4, 1, 8, 0.6),
    "email":     (2, 1, 7, 0.3),  "proposal":  (6, 1, 8, 1.0),
    "tutorial":  (5, 5, 8, 1.5),  "guide":     (5, 4, 8, 1.2),

    # Data / Analysis
    "analyze":   (8, 3, 5, 1.0),  "data":      (6, 5, 3, 1.2),
    "report":    (5, 3, 7, 1.0),  "dashboard": (5, 6, 5, 1.2),
    "visualize": (4, 6, 4, 1.0),  "statistics":(7, 3, 4, 0.8),
    "machine learning": (8,7,3,1.5), "model train":(8,7,3,1.5),
    "research":  (8, 2, 6, 1.5),

    # Chat / simple
    "explain":   (5, 2, 5, 0.5),  "question":  (4, 1, 4, 0.3),
    "help":      (3, 2, 4, 0.4),  "how to":    (4, 3, 5, 0.6),
    "what is":   (3, 1, 4, 0.3),  "difference":(4, 1, 5, 0.5),
    "brainstorm":(5, 1, 7, 0.8),
}

# ── Token estimation by complexity ──
def estimate_tokens(task: str, complexity: float) -> dict:
    """Estimate input/output tokens based on task length and complexity."""
    word_count = len(task.split())
    # Input: task text + expected context + conversation history
    input_tokens = int(word_count * 1.5 + 1000 * complexity)
    # Output: depends heavily on task type
    # High code tasks produce lots of tokens; simple Q&A few
    output_tokens = int(800 * complexity + 200)
    return {"input": input_tokens, "output": output_tokens}


def profile_task(task: str) -> dict:
    """Analyze task description → capability requirements + token estimates."""
    task_lower = task.lower()

    # Match task signals
    best_signal = None
    best_len = 0
    for signal, (r, c, w, mult) in TASK_SIGNALS.items():
        if signal in task_lower and len(signal) > best_len:
            best_signal = (signal, r, c, w, mult)
            best_len = len(signal)

    if best_signal:
        signal, reasoning, coding, writing, complexity = best_signal
    else:
        # Default: medium everything
        reasoning, coding, writing, complexity = 5, 3, 5, 0.6

    tokens = estimate_tokens(task, complexity)

    return {
        "reasoning_need": reasoning,
        "coding_need": coding,
        "writing_need": writing,
        "instruction_need": max(5, int((reasoning + coding + writing) / 3)),
        "input_tokens": tokens["input"],
        "output_tokens": tokens["output"],
        "complexity": round(complexity, 2),
        "matched_signal": best_signal[0] if best_signal else "generic",
    }


def rank_models(profile: dict, mode: str = "value") -> list:
    """Rank models by capability match + cost-effectiveness.
    
    Modes:
      value   — best capability per dollar (default)
      quality — best raw capability regardless of cost
      balanced — blended: 60% capability + 40% cost
      local   — includes local/open-weight models alongside API models
    """
    include_local = mode == "local"
    if include_local:
        mode = "value"  # use value scoring for fairness

    all_models = list(MODELS)
    if include_local:
        all_models.extend(LOCAL_MODELS)

    results = []

    for m in all_models:
        # Capability score: how well does this model match the task needs?
        cap_match = (
            min(m["reasoning"], profile["reasoning_need"]) / max(profile["reasoning_need"], 1) * 0.35 +
            min(m["coding"], profile["coding_need"]) / max(profile["coding_need"], 1) * 0.35 +
            min(m["writing"], profile["writing_need"]) / max(profile["writing_need"], 1) * 0.20 +
            min(m["instruction"], profile["instruction_need"]) / max(profile["instruction_need"], 1) * 0.10
        )

        # Cost estimate
        if "cost_per_hour" in m:
            # Local model: cost = (time to generate) × hourly rate
            total_toks = profile["input_tokens"] + profile["output_tokens"]
            time_seconds = total_toks / m["tokens_per_sec"]
            total_cost = time_seconds / 3600 * m["cost_per_hour"]
        else:
            # API model: per-token pricing
            in_cost = m["in"] / 1_000_000 * profile["input_tokens"]
            out_cost = m["out"] / 1_000_000 * profile["output_tokens"]
            total_cost = in_cost + out_cost

        # Context window check
        total_tokens = profile["input_tokens"] + profile["output_tokens"]
        ctx_ok = total_tokens <= m["ctx"] * 0.9

        # Scoring per mode
        if mode == "quality":
            # Pure capability — ignore cost
            score = round(cap_match * 100)
        elif mode == "balanced":
            # 60% capability + 40% cost-effectiveness
            cost_score = 1.0 / max(total_cost, 0.0001) * 0.0001  # normalize
            score = round(cap_match * 60 + cost_score * 40)
        else:
            # value: capability / cost
            score = round(cap_match / max(total_cost, 0.0001) * 100)

        results.append({
            "provider": m["provider"],
            "model": m["name"],
            "cap_match": round(cap_match, 2),
            "cost": round(total_cost, 4),
            "value_score": score,
            "ctx_ok": ctx_ok,
            "reasoning": m["reasoning"],
            "coding": m["coding"],
            "writing": m["writing"],
            "ctx": m["ctx"],
        })

    results.sort(key=lambda x: -x["value_score"])
    return results


def load_lifetime() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"tasks": 0, "total_saved": 0.0, "would_have_cost": 0.0, "actually_spent": 0.0}

def save_lifetime(best, expensive, task):
    saved = max(0, expensive["cost"] - best["cost"])
    data = load_lifetime()
    data["tasks"] += 1
    data["total_saved"] = round(data["total_saved"] + saved, 6)
    data["would_have_cost"] = round(data["would_have_cost"] + expensive["cost"], 6)
    data["actually_spent"] = round(data["actually_spent"] + best["cost"], 6)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def reset_lifetime():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


def format_output(task: str, profile: dict, rankings: list, mode: str = "value", quiet: bool = False):
    """Pretty-print the recommendation. quiet=True → single line for agent use."""
    best = rankings[0]
    lifetime = load_lifetime()
    
    if quiet:
        # Single line: ⭐ Model $cost (cap%) | variant | bonus
        line = f"⭐ {best['provider']} {best['model']} ${best['cost']:.4f} ({best['cap_match']:.0%})"
        cheapest = min(rankings, key=lambda x: x["cost"])
        if cheapest["model"] != best["model"]:
            line += f" | 💸 {cheapest['provider']} {cheapest['model']} ${cheapest['cost']:.4f}"
        if lifetime["tasks"] > 0:
            line += f" | 🎁 ${lifetime['total_saved']:.4f}/{lifetime['tasks']}t"
        print(line)
        return

    mode_labels = {"value": "Best Value (capability/$)", "quality": "Best Quality (capability first)", "balanced": "Balanced (60% cap + 40% cost)", "local": "Local vs API (includes open-weight models)"}

    print("=" * 60)
    print(f"  Task Cost Estimator — {mode_labels.get(mode, mode)}")
    print("=" * 60)

    # Task summary
    print(f"\n📋 Task: {task[:100]}{'...' if len(task)>100 else ''}")
    print(f"   Signal: {profile['matched_signal']}")
    print(f"   Needs:  reasoning={profile['reasoning_need']}/10  coding={profile['coding_need']}/10  writing={profile['writing_need']}/10")
    print(f"   Est. tokens: ~{profile['input_tokens']:,} in / ~{profile['output_tokens']:,} out")
    print(f"   Complexity: {profile['complexity']}")

    # Top recommendations
    print(f"\n{'='*70}")
    print(f"  {'Model':<24} {'Value':>6} {'Cost':>8} {'Cap.Match':>9} {'R/C/W':>8}")
    print(f"  {'-'*60}")

    for i, r in enumerate(rankings[:8], 1):
        star = "⭐" if i == 1 else ("★" if i <= 3 else " ")
        cost_str = f"${r['cost']:.4f}"
        cap_str = f"{r['cap_match']:.0%}"
        rcw = f"{r['reasoning']}/{r['coding']}/{r['writing']}"
        ctx_warn = "" if r["ctx_ok"] else " ⚠ctx"

        print(f"{star} {r['provider']:<8} {r['model']:<15} {r['value_score']:>5}  {cost_str:>8} {cap_str:>8} {rcw:>8}{ctx_warn}")

    # Best pick summary
    best = rankings[0]
    print(f"\n{'='*60}")
    print(f"  💡 Best pick: {best['provider']} {best['model']}")
    print(f"     Cost per run: ${best['cost']:.4f}")
    print(f"     If you do this 20×/day: ${best['cost']*20:.2f}/day")

    # Savings vs most expensive viable model (>80% cap match)
    viable = [r for r in rankings if r["cap_match"] >= 0.8]
    if len(viable) >= 2:
        most_expensive = max(viable, key=lambda x: x["cost"])
        saved_this_task = most_expensive["cost"] - best["cost"]
        if saved_this_task > 0:
            print(f"\n  💰 Saved this task: ${saved_this_task:.4f} (vs {most_expensive['provider']} {most_expensive['model']})")

    # Lifetime Bonus
    lifetime = load_lifetime()
    if lifetime["tasks"] > 0:
        print(f"\n  🎁 LIFETIME BONUS: ${lifetime['total_saved']:.4f} saved across {lifetime['tasks']} tasks")
    if lifetime.get("would_have_cost"):
        print(f"     Would have cost: ${lifetime['would_have_cost']:.4f}")
        print(f"     Actually spent:  ${lifetime['actually_spent']:.4f}")

    # Cheapest option
    cheapest = min(rankings, key=lambda x: x["cost"])
    if cheapest["model"] != best["model"]:
        print(f"\n  💸 Cheapest option: {cheapest['provider']} {cheapest['model']} (${cheapest['cost']:.4f})")
        print(f"     Saves ${best['cost'] - cheapest['cost']:.4f} vs best pick")
        if not cheapest["ctx_ok"]:
            print(f"     ⚠ Warning: may exceed context window")

    # Most capable option (if different)
    most_capable = max(rankings, key=lambda x: x["reasoning"] + x["coding"])
    if most_capable["model"] not in (best["model"], cheapest["model"]):
        print(f"\n  🧠 Most capable: {most_capable['provider']} {most_capable['model']} (${most_capable['cost']:.4f})")
        print(f"     Use this if quality matters more than cost")


def main():
    # Parse flags
    args = sys.argv[1:]
    mode = "value"
    quiet = False
    task_parts = []

    for a in args:
        if a == "--quality":
            mode = "quality"
        elif a == "--balanced":
            mode = "balanced"
        elif a == "--local":
            mode = "local"
        elif a in ("-q", "--quiet"):
            quiet = True
        elif a == "--value":
            mode = "value"
        elif a == "--reset-bonus":
            reset_lifetime()
            print("🎁 Lifetime bonus reset.")
            return
        elif a == "--bonus":
            lifetime = load_lifetime()
            print(f"🎁 LIFETIME BONUS: ${lifetime['total_saved']:.4f} saved across {lifetime['tasks']} tasks")
            if lifetime.get("would_have_cost"):
                print(f"   Would have cost: ${lifetime['would_have_cost']:.4f}")
                print(f"   Actually spent:  ${lifetime['actually_spent']:.4f}")
            return
        elif a in ("-h", "--help"):
            print("Usage: task-cost [--quality|--balanced|--local] 'task description'")
            print("")
            print("Modes:")
            print("  (default)  Best value — capability per dollar")
            print("  --quality  Best quality — raw capability, ignore cost")
            print("  --balanced Blend 60% capability + 40% cost-effectiveness")
            print("  --local    Include local/open-weight models alongside API")
            print("")
            print("Examples:")
            print("  task-cost 'build a REST API'")
            print("  task-cost --quality 'debug a complex algorithm'")
            print("  task-cost --balanced 'write a blog post'")
            return
        else:
            task_parts.append(a)

    if not task_parts:
        print("Usage: task-cost [--quality|--balanced] 'task description...'")
        sys.exit(1)

    task = " ".join(task_parts)
    profile = profile_task(task)
    rankings = rank_models(profile, mode)
    format_output(task, profile, rankings, mode, quiet)

    # Track lifetime savings
    best = rankings[0]
    viable = [r for r in rankings if r["cap_match"] >= 0.8]
    if len(viable) >= 2:
        expensive = max(viable, key=lambda x: x["cost"])
    else:
        expensive = max(rankings, key=lambda x: x["cost"])
    save_lifetime(best, expensive, task)


if __name__ == "__main__":
    main()
