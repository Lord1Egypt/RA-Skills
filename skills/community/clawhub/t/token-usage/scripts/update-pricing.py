#!/usr/bin/env python3
"""
Multi-source model pricing updater.
Fetches current rates from multiple APIs and merges into pricing.json + registry.json
"""

import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Where the token-usage skill lives
SKILL_DIR = Path(__file__).parent
PRICING_FILE = SKILL_DIR / "pricing.json"
REGISTRY_FILE = SKILL_DIR / "registry.json"

# Sources to query
SOURCES = {
    "openrouter": "https://openrouter.ai/api/v1/models",
    # Moonshot doesn't have a public pricing endpoint; we fall back to known rates
}

# Known Moonshot direct pricing (CNY, converted to USD at ~7.2 rate)
# Source: https://platform.kimi.com/docs/pricing/
CNY_TO_USD = 7.2
MOONSHOT_RATES = {
    "kimi/k2.6": {
        "input": round(6.50 / CNY_TO_USD, 2),      # ¥6.50 per 1M
        "output": round(27.00 / CNY_TO_USD, 2),     # ¥27.00 per 1M
        "cache_read": round(1.10 / CNY_TO_USD, 2),  # ¥1.10 per 1M (cache hit)
        "cache_write": None,
    },
    "kimi/k2.7": {
        "input": round(6.50 / CNY_TO_USD, 2),      # ¥6.50 per 1M (assuming same as k2.6)
        "output": round(27.00 / CNY_TO_USD, 2),     # ¥27.00 per 1M
        "cache_read": round(1.10 / CNY_TO_USD, 2),
        "cache_write": None,
    },
    "kimi/k2.7-code": {
        "input": round(6.50 / CNY_TO_USD, 2),      # ¥6.50 per 1M
        "output": round(27.00 / CNY_TO_USD, 2),     # ¥27.00 per 1M
        "cache_read": round(1.30 / CNY_TO_USD, 2),  # ¥1.30 per 1M
        "cache_write": None,
    },
    "kimi/k3": {
        "input": round(20.00 / CNY_TO_USD, 2),     # ¥20.00 per 1M (cache miss)
        "output": round(100.00 / CNY_TO_USD, 2),    # ¥100.00 per 1M
        "cache_read": round(2.00 / CNY_TO_USD, 2),  # ¥2.00 per 1M (cache hit)
        "cache_write": None,
    },
}


def fetch_openrouter():
    """Fetch pricing from OpenRouter API."""
    try:
        req = urllib.request.Request(
            SOURCES["openrouter"],
            headers={"Accept": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        rates = {}
        for model in data.get("data", []):
            id = model.get("id", "")
            pricing = model.get("pricing", {})
            if not pricing:
                continue
            # OpenRouter prices are per-token; convert to per-million for consistency
            inp = pricing.get("prompt", 0)
            out = pricing.get("completion", 0)
            if inp or out:
                rates[id] = {
                    "input": round(float(inp) * 1_000_000, 4),
                    "output": round(float(out) * 1_000_000, 4),
                    "cache_read": None,
                    "cache_write": None,
                    "source": "openrouter",
                    "updated": datetime.now().isoformat(),
                }
        return rates
    except Exception as e:
        print(f"OpenRouter fetch failed: {e}")
        return {}


def merge_pricing(openrouter_rates):
    """Merge all sources into final pricing dict. Moonshot direct rates take priority."""
    pricing = {}
    
    # Start with Moonshot direct rates as baseline (most accurate for Kimi models)
    for model, rates in MOONSHOT_RATES.items():
        pricing[model] = {
            **rates,
            "source": "moonshot-direct",
            "updated": datetime.now().isoformat(),
        }
    
    # Add other known rates ONLY if OpenRouter doesn't have them
    known_fallbacks = {
        "anthropic/claude-sonnet-4-5": {
            "input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75,
        },
        "openai/gpt-4o": {
            "input": 2.50, "output": 10.00, "cache_read": 1.25, "cache_write": 0,
        },
        "openai/gpt-4o-mini": {
            "input": 0.15, "output": 0.60, "cache_read": 0.075, "cache_write": 0,
        },
    }
    
    for model, rates in known_fallbacks.items():
        if model not in openrouter_rates:
            pricing[model] = {
                **rates,
                "source": "fallback",
                "updated": datetime.now().isoformat(),
            }
    
    # Overlay OpenRouter rates for comparison (stored separately)
    for model, rates in openrouter_rates.items():
        # Normalize OpenRouter model IDs to our format
        normalized = model
        if model.startswith("moonshotai/kimi-"):
            # Map moonshotai/kimi-k2.6 → kimi/k2.6
            normalized = "kimi/" + model.replace("moonshotai/kimi-", "")
        elif model.startswith("anthropic/"):
            normalized = model
        elif model.startswith("openai/"):
            normalized = model
        
        # Only add OpenRouter rate if we don't have a better direct source
        if normalized not in pricing:
            pricing[normalized] = {
                "input": rates["input"],
                "output": rates["output"],
                "cache_read": rates.get("cache_read"),
                "cache_write": rates.get("cache_write"),
                "source": "openrouter",
                "updated": rates["updated"],
            }
        else:
            # Store OpenRouter as alternative pricing for comparison
            pricing[normalized]["openrouter_input"] = rates["input"]
            pricing[normalized]["openrouter_output"] = rates["output"]
    
    return pricing


def build_registry(pricing):
    """Build a model registry with metadata."""
    registry = {
        "updated": datetime.now().isoformat(),
        "models": {},
    }
    
    for model_id, rates in pricing.items():
        registry["models"][model_id] = {
            "pricing": {
                "input_per_million": rates["input"],
                "output_per_million": rates["output"],
                "cache_read_per_million": rates.get("cache_read"),
                "cache_write_per_million": rates.get("cache_write"),
            },
            "alternative_pricing": {},
            "availability": "available",
            "provider": model_id.split("/")[0] if "/" in model_id else "unknown",
            "last_pricing_update": rates.get("updated", datetime.now().isoformat()),
            "pricing_source": rates.get("source", "unknown"),
        }
        # Add OpenRouter comparison if available
        if "openrouter_input" in rates:
            registry["models"][model_id]["alternative_pricing"]["openrouter"] = {
                "input_per_million": rates["openrouter_input"],
                "output_per_million": rates["openrouter_output"],
            }
    
    return registry


def main():
    print("Fetching model pricing from multiple sources...")
    
    # Fetch from sources
    openrouter_rates = fetch_openrouter()
    print(f"OpenRouter: {len(openrouter_rates)} models found")
    
    # Merge
    pricing = merge_pricing(openrouter_rates)
    print(f"Total models in pricing: {len(pricing)}")
    
    # Write pricing.json
    with open(PRICING_FILE, "w") as f:
        json.dump(pricing, f, indent=2)
    print(f"Wrote {PRICING_FILE}")
    
    # Build and write registry
    registry = build_registry(pricing)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"Wrote {REGISTRY_FILE}")
    
    # Print summary
    print("\n--- Pricing Summary ---")
    for model in sorted(pricing.keys()):
        p = pricing[model]
        or_in = p.get('openrouter_input')
        or_out = p.get('openrouter_output')
        comparison = ""
        if or_in:
            markup = ((or_in - p['input']) / p['input'] * 100) if p['input'] > 0 else 0
            comparison = f" | OpenRouter: ${or_in}/M in (+{markup:.0f}%)"
        print(f"{model}: ${p['input']}/M in, ${p['output']}/M out (source: {p.get('source', '?')}){comparison}")


if __name__ == "__main__":
    main()
