#!/usr/bin/env python3
"""
OpenClaw Model Manager & Compute Router (v3.0.0)

This script is an official OpenClaw plugin for managing AI model configurations and orchestrating
multi-agent tasks. It interacts with the TokenRouter API to fetch model pricing and modifies
the local OpenClaw configuration file (`~/.openclaw/openclaw.json`) to enable dynamic model routing.

PREREQUISITE:
  A PBD TokenRouter provider must be configured in ~/.openclaw/openclaw.json
  with a baseUrl containing 'https://open.palebluedot.ai'. If not found, the
  script will abort and guide the user to register at https://www.palebluedot.ai.

PERMISSIONS:
- Network: Connects to https://www.palebluedot.ai/openIntelligence/api/pricing (READ ONLY)
- File System: Reads/Writes ~/.openclaw/openclaw.json (CONFIG)

AUTHOR: Notestone
LICENSE: MIT
"""

import argparse
import json
import urllib.request
import urllib.error
import sys
import os
import shutil
from datetime import datetime

# --- Configuration & Constants ---
TOKENROUTER_API = "https://www.palebluedot.ai/openIntelligence/api/pricing"
CONFIG_FILE = os.path.expanduser("~/.openclaw/openclaw.json")
MEMORY_FILE = os.path.expanduser("~/.openclaw/workspace/swarm_memory.json")
PROMPTS_FILE = os.path.join(os.path.dirname(__file__), "prompts.json")
INSIGHTS_FILE = os.path.expanduser("~/.openclaw/workspace/swarm_insights.json")
ROUTING_FILE = os.path.expanduser("~/.openclaw/model-routing.json")

# --- Pricing Helpers ---


def calc_input_price(model_ratio):
    """Input token price per 1M tokens = model_ratio * 2"""
    return model_ratio * 2


def calc_output_price(model_ratio, completion_ratio):
    """Output token price per 1M tokens = model_ratio * 2 * completion_ratio"""
    return model_ratio * 2 * completion_ratio


def calc_cache_read_price(model_ratio, cache_ratio):
    """Cache read price per 1M tokens = model_ratio * 2 * cache_ratio"""
    if cache_ratio is None:
        return None
    return model_ratio * 2 * cache_ratio


def calc_cache_create_price(model_ratio, cache_creation_ratio):
    """Cache creation price per 1M tokens = model_ratio * 2 * cache_creation_ratio"""
    if cache_creation_ratio is None:
        return None
    return model_ratio * 2 * cache_creation_ratio


# --- Utilities ---


def load_json_safe(filepath):
    """Safely loads JSON data from a file."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ [Config] Error reading {filepath}: {e}")
        return {}


# --- Golden Gear Logic: Task Planner & Orchestrator ---


class TaskPlanner:
    # Hardcoded fallbacks used only when the API is unreachable
    FALLBACK_TIERS = {
        "tier1": {
            "id": "anthropic/claude-opus-4.6",
            "price": 15.00,
            "role": "Architect/Reasoning",
        },
        "tier2": {"id": "openai/gpt-4o-mini", "price": 0.60, "role": "Coder/Drafter"},
        "tier3": {
            "id": "deepseek/deepseek-v3.2",
            "price": 0.38,
            "role": "Reviewer/Privacy",
        },
    }

    def __init__(self):
        # Load DNA (Prompts) & Hippocampus (Insights)
        self.prompts = load_json_safe(PROMPTS_FILE).get("roles", {})
        self.insights = load_json_safe(INSIGHTS_FILE).get("model_performance", {})

        # Load custom routing rules (if any)
        self.custom_routing = load_json_safe(ROUTING_FILE)

        # Try to build tiers dynamically from live API pricing
        models = fetch_models()
        if models:
            self.prices, self.model_map = self._build_tiers_from_api(models)
        else:
            print("⚠️ [Router] API unavailable, using fallback model tiers.")
            self.prices = dict(self.FALLBACK_TIERS)
            self.model_map = {k: v["id"] for k, v in self.FALLBACK_TIERS.items()}

    # ----- dynamic tier builder -----

    @staticmethod
    def _build_tiers_from_api(models):
        """
        Pick one model per tier (high / mid / low) from the live price list.

        Strategy:
          1. Keep only well-known models (priority_keywords) so we don't route to
             obscure / untested models.
          2. Compute each model's output price and sort descending.
          3. Split into three equal-ish buckets (high / mid / low price).
          4. From each bucket, pick the model closest to the bucket's median price
             — this avoids outliers at the very edge.
        """
        priority_keywords = [
            "gpt-4o",
            "gpt-5",
            "claude-sonnet",
            "claude-opus",
            "claude-haiku",
            "gemini-3",
            "deepseek",
            "llama",
            "qwen3",
            "grok",
        ]

        # Filter to known models and compute output price
        scored = []
        for m in models:
            name = m.get("model_name", "")
            if not any(k in name for k in priority_keywords):
                continue
            mr = m.get("model_ratio", 0)
            cr = m.get("completion_ratio", 1)
            out_price = calc_output_price(mr, cr)
            if out_price <= 0:
                continue
            scored.append({"name": name, "price": out_price, "raw": m})

        # Need at least 3 models to form 3 tiers
        if len(scored) < 3:
            print("⚠️ [Router] Not enough models from API, using fallback tiers.")
            fallback_prices = dict(TaskPlanner.FALLBACK_TIERS)
            fallback_map = {k: v["id"] for k, v in TaskPlanner.FALLBACK_TIERS.items()}
            return fallback_prices, fallback_map

        # Sort by price descending (most expensive first)
        scored.sort(key=lambda x: x["price"], reverse=True)

        # Split into 3 buckets
        n = len(scored)
        bucket_high = scored[: n // 3]  # top third  (expensive)
        bucket_mid = scored[n // 3 : 2 * n // 3]  # middle third
        bucket_low = scored[2 * n // 3 :]  # bottom third (cheap)

        def pick_median(bucket):
            """Pick the model closest to the bucket's median price."""
            if not bucket:
                return None
            bucket_sorted = sorted(bucket, key=lambda x: x["price"])
            return bucket_sorted[len(bucket_sorted) // 2]

        high = pick_median(bucket_high)
        mid = pick_median(bucket_mid)
        low = pick_median(bucket_low)

        # Deduplicate: if any bucket collapsed to the same model, fallback
        chosen = [high, mid, low]
        if len({c["name"] for c in chosen if c}) < 3:
            print("⚠️ [Router] Could not form 3 distinct tiers, using fallback.")
            fallback_prices = dict(TaskPlanner.FALLBACK_TIERS)
            fallback_map = {k: v["id"] for k, v in TaskPlanner.FALLBACK_TIERS.items()}
            return fallback_prices, fallback_map

        prices = {
            "tier1": {
                "id": high["name"],
                "price": high["price"],
                "role": "Architect/Reasoning",
            },
            "tier2": {
                "id": mid["name"],
                "price": mid["price"],
                "role": "Coder/Drafter",
            },
            "tier3": {
                "id": low["name"],
                "price": low["price"],
                "role": "Reviewer/Privacy",
            },
        }
        model_map = {
            "tier1": high["name"],
            "tier2": mid["name"],
            "tier3": low["name"],
        }

        print(f"✅ [Router] Dynamic tiers built from {len(scored)} models:")
        print(f"   tier1 (high)  → {high['name']}  ${high['price']:.2f}/1M")
        print(f"   tier2 (mid)   → {mid['name']}  ${mid['price']:.2f}/1M")
        print(f"   tier3 (low)   → {low['name']}  ${low['price']:.2f}/1M")

        return prices, model_map

    def _get_stable_model(self, tier_key):
        """Active Adaptation: Switch model if unstable based on historical insights."""
        default_model_id = self.model_map.get(tier_key, "openai/gpt-4o-mini")

        # Check stability history
        if default_model_id in self.insights:
            stats = self.insights[default_model_id]
            # Threshold: < 50% success rate with at least 1 attempt
            if stats.get("sample_size", 0) > 0 and stats.get("success_rate", 100) < 50:
                # UNSTABLE! Switch strategy.
                # Strategy: Fallback to Tier 1 (Costly but reliable) if current is Tier 2/3
                if tier_key in ["tier2", "tier3"]:
                    fallback_id = self.model_map["tier1"]
                    return fallback_id, True, "Stability Fallback"

        return default_model_id, False, ""

    def _apply_custom_routing(self, category, steps):
        """
        Apply user-defined model overrides from ~/.openclaw/model-routing.json.

        The routing file maps each category to a list of models, one per phase
        (in order). Extra entries are ignored; missing entries keep the default tier.

        Example routing file:
        {
          "coding": ["anthropic/claude-opus-4.6", "openai/gpt-4o-mini", "deepseek/deepseek-v3.2"],
          "translation": ["openai/gpt-4o", "deepseek/deepseek-v3.2"],
          "fallback": "openai/gpt-4o-mini"
        }
        """
        if not self.custom_routing:
            return steps

        # Per-category overrides
        overrides = self.custom_routing.get(category, [])
        # Global fallback model (applied to any tier without an override)
        fallback_model = self.custom_routing.get("fallback")

        if not overrides and not fallback_model:
            return steps

        if overrides:
            print(f"📌 [Router] Applying custom routing for '{category}': {overrides}")

        for i, step in enumerate(steps):
            if isinstance(overrides, list) and i < len(overrides) and overrides[i]:
                step["custom_model"] = overrides[i]
            elif fallback_model:
                step["custom_model"] = fallback_model

        return steps

    def plan(self, task_description, execute=False):
        """Simulate decomposing a task and optionally execute it."""

        # 1. Classify task using enhanced classifier
        category = enhanced_task_classification(task_description)

        # Helper to format prompt safely
        def get_prompt(role, default):
            template = self.prompts.get(role, {}).get("task_template", default)
            return template.replace("{task_description}", task_description)

        # 2. Build steps based on category
        if category == "coding":
            steps = [
                {
                    "phase": "1. Design",
                    "model_tier": "tier1",
                    "reason": "Architecture",
                    "artifact": "SPEC.md",
                    "task": get_prompt(
                        "architect", f"Design architecture for: {task_description}"
                    ),
                },
                {
                    "phase": "2. Code",
                    "model_tier": "tier2",
                    "reason": "Implementation",
                    "artifact": "code",
                    "task": get_prompt("coder", f"Write code for: {task_description}"),
                },
                {
                    "phase": "3. Review",
                    "model_tier": "tier3",
                    "reason": "Security Check",
                    "artifact": "AUDIT.md",
                    "task": get_prompt("auditor", "Audit the code."),
                },
            ]
        elif category == "analysis":
            steps = [
                {
                    "phase": "1. Research",
                    "model_tier": "tier1",
                    "reason": "Deep reasoning",
                    "artifact": "RESEARCH.md",
                    "task": f"Conduct thorough research and analysis for: {task_description}. Save findings to 'RESEARCH.md'.",
                },
                {
                    "phase": "2. Synthesize",
                    "model_tier": "tier2",
                    "reason": "Summarization",
                    "artifact": "REPORT.md",
                    "task": "Read 'RESEARCH.md'. Synthesize the findings into a clear, structured report. Save to 'REPORT.md'.",
                },
                {
                    "phase": "3. Fact-check",
                    "model_tier": "tier3",
                    "reason": "Verification",
                    "artifact": "REVIEW.md",
                    "task": "Read 'REPORT.md'. Verify claims, check for logical errors or bias. Save review to 'REVIEW.md'.",
                },
            ]
        elif category == "writing":
            steps = [
                {
                    "phase": "1. Outline",
                    "model_tier": "tier1",
                    "reason": "Structure & strategy",
                    "artifact": "OUTLINE.md",
                    "task": f"Create a detailed outline for: {task_description}. Save to 'OUTLINE.md'.",
                },
                {
                    "phase": "2. Draft",
                    "model_tier": "tier2",
                    "reason": "Content generation",
                    "artifact": "DRAFT.md",
                    "task": "Read 'OUTLINE.md'. Write the full draft following the outline. Save to 'DRAFT.md'.",
                },
                {
                    "phase": "3. Polish",
                    "model_tier": "tier3",
                    "reason": "Proofreading",
                    "artifact": "RESULT.md",
                    "task": "Read 'DRAFT.md'. Fix grammar, improve clarity, polish the text. Save final version to 'RESULT.md'.",
                },
            ]
        elif category == "creative":
            steps = [
                {
                    "phase": "1. Ideate",
                    "model_tier": "tier1",
                    "reason": "Creative thinking",
                    "artifact": "IDEAS.md",
                    "task": f"Brainstorm multiple creative approaches for: {task_description}. Save to 'IDEAS.md'.",
                },
                {
                    "phase": "2. Execute",
                    "model_tier": "tier2",
                    "reason": "Production",
                    "artifact": "RESULT.md",
                    "task": "Read 'IDEAS.md'. Pick the best idea and produce the deliverable. Save to 'RESULT.md'.",
                },
            ]
        elif category == "translation":
            steps = [
                {
                    "phase": "1. Translate",
                    "model_tier": "tier2",
                    "reason": "Language conversion",
                    "artifact": "TRANSLATION.md",
                    "task": f"Translate the following content accurately: {task_description}. Save to 'TRANSLATION.md'.",
                },
                {
                    "phase": "2. Review",
                    "model_tier": "tier3",
                    "reason": "Quality check",
                    "artifact": "RESULT.md",
                    "task": "Read 'TRANSLATION.md'. Check for accuracy, naturalness and cultural fit. Save corrected version to 'RESULT.md'.",
                },
            ]
        else:  # simple
            steps = [
                {
                    "phase": "1. Execute",
                    "model_tier": "tier3",
                    "reason": "Quick task",
                    "artifact": "RESULT.md",
                    "task": f"Complete this task directly: {task_description}. Save output to 'RESULT.md'.",
                },
            ]

        # 3. Apply custom routing overrides (if configured)
        steps = self._apply_custom_routing(category, steps)

        # 4. Display Plan & Apply Adaptation
        final_steps = self._display_plan(task_description, category.capitalize(), steps)

        # 5. Execute (if requested)
        if execute:
            self._execute_swarm(task_description, final_steps)

    def _display_plan(self, task, category, steps):
        # Calculate savings
        total_tokens = 1000
        # Baseline cost (All Tier 1)
        cost_baseline = (
            len(steps) * (self.prices["tier1"]["price"] / 1_000_000) * total_tokens
        )

        cost_optimized = 0
        final_steps = []

        print(f"\n🧠 **Golden Gear Task Planner**")
        print(f'**Task:** "{task}"')
        print(f"**Category:** {category}\n")
        print("| Phase | Assigned Agent | Model | Price/1M | Status |")
        print("| :--- | :--- | :--- | :--- | :--- |")

        for step in steps:
            tier = step["model_tier"]

            # Check for custom routing override first
            custom_model = step.get("custom_model")
            if custom_model:
                model_id = custom_model
                price = self.prices[tier]["price"]  # approximate; real price unknown
                status_display = f"📌 Custom"
            else:
                # Apply Active Adaptation
                model_id, switched, reason = self._get_stable_model(tier)

                if switched:
                    price = self.prices["tier1"]["price"]
                    status_display = f"🔄 Switched ({reason})"
                else:
                    price = self.prices[tier]["price"]
                    status_display = "✅ Optimal"

            cost_optimized += (price / 1_000_000) * total_tokens

            # Update step for execution
            step["final_model_id"] = model_id
            final_steps.append(step)

            role_name = self.prices[tier]["role"]
            print(
                f"| {step['phase']} | {role_name} | `{model_id.split('/')[-1]}` | ${price:.2f} | {status_display} |"
            )

        savings_pct = (
            ((cost_baseline - cost_optimized) / cost_baseline) * 100
            if cost_baseline > 0
            else 0
        )
        print(f"\n📉 **Projected Savings:** **{savings_pct:.1f}%** 💸")
        return final_steps

    def _execute_swarm(self, original_task, steps):
        """
        Generate a structured execution plan as JSON for the host agent to carry out.

        Since sessions_spawn is an internal OpenClaw API (not callable via CLI),
        this method outputs a machine-readable instruction set that the host agent
        can parse and execute by spawning sub-agents through the internal API.
        """
        plan_output = {
            "version": "2.0",
            "task": original_task,
            "generated_at": datetime.now().isoformat(),
            "instructions": (
                "Execute each step sequentially using sessions_spawn. "
                "Each step's artifact is the input context for the next step. "
                "If a step fails, retry up to max_retries times with the error injected into the prompt."
            ),
            "steps": [],
        }

        for step in steps:
            plan_output["steps"].append(
                {
                    "phase": step["phase"],
                    "model": step["final_model_id"],
                    "system_prompt": self.prompts.get(
                        step.get("reason", "").lower().split()[0]
                        if step.get("reason")
                        else "",
                        {},
                    ).get("system", ""),
                    "task_prompt": step["task"],
                    "expected_artifact": step.get("artifact", "RESULT.md"),
                    "max_retries": 2,
                    "timeout_seconds": 60,
                }
            )

        # Write to workspace file for the host agent to pick up
        plan_path = os.path.expanduser("~/.openclaw/workspace/swarm_plan.json")
        plan_dir = os.path.dirname(plan_path)
        if not os.path.exists(plan_dir):
            os.makedirs(plan_dir, exist_ok=True)

        try:
            with open(plan_path, "w", encoding="utf-8") as f:
                json.dump(plan_output, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ [Execute] Failed to write plan: {e}")
            return

        # Also print to stdout so the host agent can read it directly
        print(f"\n📋 **Execution Plan Generated**")
        print(f"   Saved to: {plan_path}\n")
        print("```json")
        print(json.dumps(plan_output, indent=2, ensure_ascii=False))
        print("```")
        print(f"\n🤖 **Agent Instructions:**")
        print(f"   The host agent should execute each step by calling sessions_spawn")
        print(f"   with the model and task_prompt specified above.")
        print(
            f"   Steps must run sequentially — each step depends on the previous artifact."
        )


# --- Existing Functions (Refactored for TokenRouter) ---


def fetch_models():
    """Fetch models from TokenRouter pricing API using standard library (HTTPS)."""
    try:
        req = urllib.request.Request(
            TOKENROUTER_API, headers={"User-Agent": "OpenClaw-ModelManager/2.0.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("data", [])
    except urllib.error.URLError as e:
        print(f"❌ [Network] Error connecting to TokenRouter API: {e}")
        return []
    except Exception as e:
        print(f"❌ [System] Unexpected error fetching models: {e}")
        return []


def filter_and_rank(models, limit=0):
    """Filter for popular/powerful models and rank them by cost-effectiveness."""
    priority_keywords = [
        "gpt-4o",
        "gpt-5",
        "claude-sonnet",
        "claude-opus",
        "claude-haiku",
        "gemini-3",
        "deepseek",
        "llama",
        "qwen3",
        "grok",
        "minimax",
    ]

    ranked = []
    others = []

    for m in models:
        model_name = m.get("model_name", "")
        is_priority = any(k in model_name for k in priority_keywords)

        if is_priority:
            ranked.append(m)
        else:
            others.append(m)

    # Sort by input price (cheapest first)
    def sort_key(x):
        return calc_input_price(x.get("model_ratio", 0))

    ranked.sort(key=sort_key)
    others.sort(key=sort_key)

    result = ranked + others
    return result[:limit] if limit > 0 else result


def display_models(models):
    """Print a markdown table of models with TokenRouter pricing."""
    print("| # | Model | Input $/1M | Output $/1M | Cache Read $/1M | Ratio |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- |")

    for idx, m in enumerate(models, 1):
        model_name = m.get("model_name", "unknown")
        mr = m.get("model_ratio", 0)
        cr = m.get("completion_ratio", 1)
        cache_r = m.get("cache_ratio", None)

        in_price = calc_input_price(mr)
        out_price = calc_output_price(mr, cr)

        if cache_r is not None:
            cache_price = calc_cache_read_price(mr, cache_r)
            cache_str = f"${cache_price:.4f}"
        else:
            cache_str = "N/A"

        print(
            f"| {idx} | `{model_name}` | ${in_price:.4f} | ${out_price:.4f} | {cache_str} | {mr} |"
        )

    print("\nTo enable a model: `enable <index>` or `enable <model_name>`")


def enable_model(model_name, config_path):
    """Enable a model by writing the config patch into openclaw.json."""
    print(f"🔒 [Config] Preparing patch for: {model_name}")

    # Read current config
    config = load_json_safe(config_path)
    if not config and os.path.exists(config_path):
        print(f"⚠️ [Config] Warning: Could not parse existing config at {config_path}")

    # Ensure nested structure exists
    agents = config.setdefault("agents", {})
    defaults = agents.setdefault("defaults", {})
    models_dict = defaults.setdefault("models", {})
    model_section = defaults.setdefault("model", {})
    current_fallbacks = model_section.get("fallbacks", [])

    if not isinstance(current_fallbacks, list):
        current_fallbacks = []

    # Add model to models dict
    if model_name not in models_dict:
        models_dict[model_name] = {}
        print(f"📝 [Config] Adding {model_name} to models list.")
    else:
        print(f"ℹ️ [Config] Model {model_name} already in models list.")

    # Add to fallbacks
    if model_name not in current_fallbacks:
        current_fallbacks.append(model_name)
        model_section["fallbacks"] = current_fallbacks
        print(f"📝 [Config] Adding {model_name} to fallback list.")
    else:
        print(f"ℹ️ [Config] Model {model_name} already in fallback list.")

    # Write config back
    config_dir = os.path.dirname(config_path)
    if config_dir and not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)

    # Backup existing config
    if os.path.exists(config_path):
        backup_path = config_path + ".bak"
        try:
            shutil.copy2(config_path, backup_path)
        except Exception:
            pass

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ [Config] Successfully written to {config_path}")
    except Exception as e:
        print(f"❌ [Config] Failed to write config: {e}")


def check_tokenrouter_provider(config=None):
    """
    Check if a PBD TokenRouter provider is configured.

    Looks under models.providers for any provider whose baseUrl contains
    'https://open.palebluedot.ai'. Returns (True, provider_key) if found,
    (False, None) otherwise.
    """
    if config is None:
        config = load_json_safe(CONFIG_FILE)

    providers = config.get("models", {}).get("providers", {})

    for provider_name, provider_config in providers.items():
        base_url = provider_config.get("baseUrl", "")
        if "https://open.palebluedot.ai" in base_url:
            return True, provider_name

    return False, None


def print_no_provider_guidance():
    """Print guidance message when TokenRouter provider is not configured (does NOT exit)."""
    print("❌ [Config] TokenRouter provider not configured.")
    print("")
    print("To use this skill, you need a PBD TokenRouter account.")
    print("Please visit https://www.palebluedot.ai to register and log in,")
    print(
        "then go to the TokenRouter section to get your configuration (base URL and API key)."
    )
    print("")
    print("Once you have the information, provide it to the agent and run:")
    print("  setup --name <provider_name> --base-url <baseUrl> --api-key <apiKey>")
    print("")
    print("Example:")
    print(
        "  setup --name tokenrouter --base-url https://open.palebluedot.ai/v1 --api-key sk-xxx..."
    )
    print("")
    print(
        "The agent will write the configuration for you, then verify and sync models automatically."
    )


def setup_provider(provider_name, base_url, api_key):
    """
    Write a new TokenRouter provider into the config file.

    Args:
        provider_name: The provider key name (e.g., 'tokenrouter')
        base_url: The TokenRouter base URL (must contain 'https://open.palebluedot.ai')
        api_key: The user's real API key from PBD
    """
    # Validate base_url
    if "https://open.palebluedot.ai" not in base_url:
        print(f"❌ [Setup] Invalid base URL: {base_url}")
        print("   The base URL must contain 'https://open.palebluedot.ai'.")
        return False

    # Validate api_key is not a placeholder
    if not api_key or api_key.startswith("<") or api_key == "YOUR_API_KEY":
        print("❌ [Setup] Invalid API key. Please provide your real API key from PBD.")
        return False

    # Load current config
    config = load_json_safe(CONFIG_FILE)

    # Create backup before modifying
    if os.path.exists(CONFIG_FILE):
        backup_path = CONFIG_FILE + ".bak"
        try:
            shutil.copy2(CONFIG_FILE, backup_path)
            print(f"📦 [Config] Backup saved to {backup_path}")
        except Exception:
            pass

    # Write provider into config
    providers = config.setdefault("models", {}).setdefault("providers", {})
    providers[provider_name] = {
        "baseUrl": base_url,
        "apiKey": api_key,
        "api": "openai-completions",
        "models": [],
    }

    # Ensure config directory exists
    config_dir = os.path.dirname(CONFIG_FILE)
    if config_dir and not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)

    # Write config
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ [Setup] Provider '{provider_name}' written to {CONFIG_FILE}")
        print(f"   baseUrl: {base_url}")
        print(
            f"   apiKey:  {api_key[:8]}...{api_key[-4:]}"
            if len(api_key) > 12
            else f"   apiKey: (set)"
        )
        return True
    except Exception as e:
        print(f"❌ [Setup] Failed to write config: {e}")
        return False


def check_command():
    """
    CLI command: verify TokenRouter provider is configured.
    Returns True if found, False otherwise.
    """
    found, provider_key = check_tokenrouter_provider()
    if found:
        print(f"✅ [Check] TokenRouter provider found: '{provider_key}'")

        # Also show basic info
        config = load_json_safe(CONFIG_FILE)
        providers = config.get("models", {}).get("providers", {})
        provider_config = providers.get(provider_key, {})
        base_url = provider_config.get("baseUrl", "N/A")
        api_key = provider_config.get("apiKey", "")
        model_count = len(provider_config.get("models", []))
        print(f"   baseUrl: {base_url}")
        if api_key:
            masked = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "(set)"
            print(f"   apiKey:  {masked}")
        print(f"   models:  {model_count} configured")
        return True
    else:
        print("❌ [Check] No TokenRouter provider found in config.")
        print_no_provider_guidance()
        return False


def sync_models():
    """
    CLI command: re-verify provider, fetch all models from TokenRouter API,
    add them to the provider's models[] and to the allow list, then save config.
    All models are routed through the configured TokenRouter provider.
    """
    # Step 1: Verify provider exists
    config = load_json_safe(CONFIG_FILE)
    found, provider_key = check_tokenrouter_provider(config)
    if not found:
        print("❌ [Sync] Cannot sync — TokenRouter provider not configured.")
        print_no_provider_guidance()
        return False

    print(f"✅ [Sync] TokenRouter provider found: '{provider_key}'")

    # Step 2: Fetch models from API
    print("🔄 [Sync] Fetching models from TokenRouter API...")
    models = fetch_models()
    if not models:
        print(
            "❌ [Sync] Could not fetch models from API. Please check your network connection."
        )
        return False

    print(f"📋 [Sync] Retrieved {len(models)} models from API")

    # Step 3: Update the provider's models array (using partial match)
    providers = config.get("models", {}).get("providers", {})
    provider_config = providers.get(provider_key, {})
    model_names = [m.get("model_name") for m in models if m.get("model_name")]
    provider_config["models"] = model_names
    print(f"📝 [Sync] Updated provider '{provider_key}' with {len(model_names)} models")

    # Step 4: Add all models to allow list
    add_models_to_allow_list(config, models)

    # Step 5: Set default model if not already set
    agents_model = config.get("agents", {}).get("defaults", {}).get("model", {})
    if not agents_model.get("id") and model_names:
        update_current_model(config, models)

    # Step 6: Create backup and save
    if os.path.exists(CONFIG_FILE):
        backup_path = CONFIG_FILE + ".bak"
        try:
            shutil.copy2(CONFIG_FILE, backup_path)
        except Exception:
            pass

    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ [Sync] Configuration saved to {CONFIG_FILE}")
    except Exception as e:
        print(f"❌ [Sync] Failed to save config: {e}")
        return False

    # Step 7: Display summary
    print(
        f"\n🎉 Sync complete! {len(model_names)} models are now available through TokenRouter."
    )
    print(f"   All models are routed through provider '{provider_key}'.")
    print(f"   Use `list` to view model pricing or start planning tasks.")
    return True


def update_tokenrouter_models(config, models):
    """Update the TokenRouter provider with the latest model list."""
    providers = config.get("models", {}).get("providers", {})

    # Find the TokenRouter provider (partial match on baseUrl)
    tokenrouter_provider = None
    tokenrouter_key = None
    for provider_name, provider_config in providers.items():
        base_url = provider_config.get("baseUrl", "")
        if "https://open.palebluedot.ai" in base_url:
            tokenrouter_provider = provider_config
            tokenrouter_key = provider_name
            break

    if tokenrouter_provider:
        # Update models list
        model_names = [m.get("model_name") for m in models if m.get("model_name")]
        tokenrouter_provider["models"] = model_names
        print(
            f"📝 [Config] Updated TokenRouter provider with {len(model_names)} models"
        )


def add_models_to_allow_list(config, models):
    """Add all models to the openclaw allow list."""
    # Get or create the models section
    models_section = config.setdefault("models", {})

    # Get or create the allowed models list
    allowed_models = models_section.setdefault("allowed", [])

    # Add model names to the allowed list if not already present
    added_count = 0
    for model_data in models:
        model_name = model_data.get("model_name")
        if model_name and model_name not in allowed_models:
            allowed_models.append(model_name)
            added_count += 1

    if added_count > 0:
        print(f"📝 [Config] Added {added_count} models to allowed list")


def update_current_model(config, models):
    """Update the current model to use the first available TokenRouter model."""
    # Find the first available model from our models list
    if models:
        first_model = models[0].get("model_name")
        if first_model:
            # Update the default model setting
            agents = config.setdefault("agents", {})
            defaults = agents.setdefault("defaults", {})
            model_section = defaults.setdefault("model", {})
            model_section["id"] = first_model
            print(f"📝 [Config] Updated current model to {first_model}")


def prepare_for_planning():
    """Prepare configuration before planning by verifying TokenRouter setup and updating models."""
    print("🔄 [Setup] Verifying TokenRouter configuration...")

    # Load current config
    config = load_json_safe(CONFIG_FILE)

    # Step 1: Check if TokenRouter provider is configured — abort if not
    found, provider_key = check_tokenrouter_provider(config)
    if not found:
        print_no_provider_guidance()
        sys.exit(1)

    print(f"✅ [Setup] TokenRouter provider found: '{provider_key}'")

    # Step 2: Fetch current models from API
    models = fetch_models()
    if not models:
        print("⚠️ [Setup] Could not fetch models from API")
        return config  # Still return config even if models fetch failed

    # Step 3: Update TokenRouter models
    update_tokenrouter_models(config, models)

    # Step 4: Add all models to allow list
    add_models_to_allow_list(config, models)

    # Step 5: Update current model if not already set
    agents_model = config.get("agents", {}).get("defaults", {}).get("model", {})
    if not agents_model.get("id"):
        update_current_model(config, models)

    # Write the updated config back
    config_dir = os.path.dirname(CONFIG_FILE)
    if config_dir and not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)

    # Backup existing config
    if os.path.exists(CONFIG_FILE):
        backup_path = CONFIG_FILE + ".bak"
        try:
            shutil.copy2(CONFIG_FILE, backup_path)
        except Exception:
            pass

    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ [Setup] Configuration updated successfully")
    except Exception as e:
        print(f"❌ [Setup] Failed to write config: {e}")

    return config


def main():
    if len(sys.argv) < 2:
        print("Usage: manage_models.py <check|setup|sync|list|enable|plan> [options]")
        print("")
        print("Commands:")
        print(
            "  check                          Verify TokenRouter provider configuration"
        )
        print(
            "  setup --name N --base-url U --api-key K   Write TokenRouter provider config"
        )
        print(
            "  sync                           Fetch models and sync to provider & allow list"
        )
        print("  list                           Show all models with pricing")
        print("  enable <index|name>            Enable a model")
        print("  plan <task> [--execute]        Plan a task with smart routing")
        return

    # Argument parsing
    cmd_args = sys.argv[1:]
    action = cmd_args[0]

    # --- Commands that do NOT require pre-existing provider ---

    if action == "check":
        check_command()
        return

    if action == "setup":
        # Parse setup arguments
        parser = argparse.ArgumentParser(prog="manage_models.py setup")
        parser.add_argument("--name", default="tokenrouter", help="Provider name")
        parser.add_argument("--base-url", required=True, help="TokenRouter base URL")
        parser.add_argument("--api-key", required=True, help="API key from PBD")
        try:
            args = parser.parse_args(cmd_args[1:])
        except SystemExit:
            return
        success = setup_provider(args.name, args.base_url, args.api_key)
        if success:
            print("")
            print(
                "Next step: run `check` to verify, then `sync` to fetch and add all models."
            )
        return

    # --- Commands that REQUIRE provider to exist ---

    found, provider_key = check_tokenrouter_provider()
    if not found:
        print_no_provider_guidance()
        return

    if action == "sync":
        sync_models()
        return

    if action == "plan":
        # Prepare configuration before planning (auto-syncs models)
        prepare_for_planning()

        execute = "--execute" in cmd_args or "-x" in cmd_args
        # Extract task description safely
        task_words = [arg for arg in cmd_args[1:] if not arg.startswith("-")]
        if not task_words:
            print("Error: Please provide a task description.")
            return
        task = " ".join(task_words)

        planner = TaskPlanner()
        planner.plan(task, execute=execute)
        return

    if action == "enable":
        if len(cmd_args) < 2:
            print("Error: Please specify a model index or name to enable.")
            return

        target = cmd_args[1]

        if target.isdigit():
            # Need to fetch models to resolve index
            models = fetch_models()
            if not models:
                print(
                    "❌ Cannot fetch model list. Try enabling by name instead: enable <model_name>"
                )
                return
            sorted_models = filter_and_rank(models)
            idx = int(target) - 1
            if 0 <= idx < len(sorted_models):
                selected_model_name = sorted_models[idx]["model_name"]
            else:
                print(f"Error: Index {target} out of range (1-{len(sorted_models)}).")
                return
        else:
            # Direct name, no need to fetch
            selected_model_name = target

        enable_model(selected_model_name, CONFIG_FILE)
        return

    if action == "list":
        # Fetch models
        models = fetch_models()
        if not models:
            return
        sorted_models = filter_and_rank(models)
        display_models(sorted_models)
        return

    print(
        f"Error: Unknown action '{action}'. Use: check, setup, sync, list, enable, plan"
    )


def enhanced_task_classification(task_description):
    """Enhanced task classification with Chinese + English keyword scoring."""
    task_lower = task_description.lower()

    patterns = {
        "coding": [
            "code",
            "program",
            "script",
            "debug",
            "function",
            "algorithm",
            "api",
            "database",
            "app",
            "test",
            "bug",
            "compile",
            "deploy",
            "refactor",
            "代码",
            "编程",
            "脚本",
            "程序",
            "调试",
            "测试",
            "开发",
            "编码",
            "接口",
            "部署",
            "重构",
            "修复",
            "函数",
            "算法",
            "数据库",
            "前端",
            "后端",
            "全栈",
            "爬虫",
            "框架",
            "模块",
        ],
        "writing": [
            "write",
            "article",
            "blog",
            "content",
            "story",
            "email",
            "letter",
            "essay",
            "copywriting",
            "documentation",
            "draft",
            "写作",
            "文章",
            "博客",
            "内容",
            "故事",
            "邮件",
            "信件",
            "文案",
            "文档",
            "稿件",
            "撰写",
            "起草",
        ],
        "analysis": [
            "analyze",
            "compare",
            "evaluate",
            "research",
            "study",
            "report",
            "data",
            "statistics",
            "insight",
            "metrics",
            "分析",
            "对比",
            "评估",
            "研究",
            "调研",
            "报告",
            "数据",
            "统计",
            "洞察",
            "指标",
            "复盘",
        ],
        "translation": [
            "translate",
            "convert language",
            "interpretation",
            "localize",
            "翻译",
            "转换语言",
            "本地化",
            "国际化",
            "多语言",
            "中译英",
            "英译中",
        ],
        "creative": [
            "creative",
            "brainstorm",
            "idea",
            "design",
            "artistic",
            "logo",
            "illustration",
            "prototype",
            "wireframe",
            "创意",
            "头脑风暴",
            "点子",
            "设计",
            "艺术",
            "原型",
            "线框图",
            "灵感",
            "构思",
        ],
        "simple": [
            "simple",
            "quick",
            "basic",
            "summarize",
            "list",
            "count",
            "lookup",
            "define",
            "explain",
            "简单",
            "快速",
            "基础",
            "总结",
            "列出",
            "计数",
            "查询",
            "定义",
            "解释",
            "概括",
        ],
    }

    scores = {}
    for category, keywords in patterns.items():
        score = sum(1 for kw in keywords if kw in task_lower)
        if score > 0:
            scores[category] = score

    if scores:
        return max(scores, key=scores.get)
    return "simple"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: manage_models.py <check|setup|sync|list|enable|plan> [options]")
    main()
