"""
Token Cost Calculator
Input conversation scale and model pricing, output cost comparison before and after optimization and savings percentage.
"""
import sys

MODELS = {
    "gpt-4o": {"input": 2.5, "output": 10.0, "unit": "M tokens"},
    "gpt-4-turbo": {"input": 10.0, "output": 30.0, "unit": "M tokens"},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "unit": "M tokens"},
    "claude-sonnet-4": {"input": 3.0, "output": 15.0, "unit": "M tokens"},
    "claude-haiku-3": {"input": 0.25, "output": 1.25, "unit": "M tokens"},
}

OPTIMIZATION_SAVINGS = {
    "none": 0,
    "L1_only": 0.20,       # Prompt compression
    "L1_L2": 0.40,         # L1 + Summary caching
    "L1_L2_L3": 0.60,      # All three tiers
}

def prompt_model_choice():
    print("\n=== Available Models ===")
    for i, name in enumerate(MODELS.keys(), 1):
        d = MODELS[name]
        print(f"  {i}. {name}")
        print(f"     Input: ${d['input']}/{d['unit']} | Output: ${d['output']}/{d['unit']}")
    print()
    while True:
        try:
            choice = int(input("Select model number: ").strip())
            if 1 <= choice <= len(MODELS):
                return list(MODELS.keys())[choice - 1]
        except ValueError:
            pass
        print("Please enter a valid number.")

def prompt_optimizer_level():
    print("\n=== Optimization Level ===")
    levels = [
        ("0 - No optimization", "none"),
        ("1 - L1: Prompt compression", "L1_only"),
        ("2 - L1+L2: Compression + Cache", "L1_L2"),
        ("3 - L1+L2+L3: All three tiers", "L1_L2_L3"),
    ]
    for label, key in levels:
        saving = int(OPTIMIZATION_SAVINGS[key] * 100)
        print(f"  {label}  (Estimated savings {saving}%)")

    while True:
        try:
            choice = int(input("Select optimization level: ").strip())
            if 0 <= choice <= 3:
                return list(OPTIMIZATION_SAVINGS.keys())[choice]
        except ValueError:
            pass
        print("Please enter 0-3.")

def main():
    print("=" * 48)
    print("  Token Cost Calculator")
    print("=" * 48)

    model = prompt_model_choice()
    rounds = int(input("\nDaily conversation rounds (e.g., 20): ").strip() or "20")
    days = int(input("Working days per month (e.g., 22): ").strip() or "22")
    avg_input = int(input("Average input tokens per turn (e.g., 500): ").strip() or "500")
    avg_output = int(input("Average output tokens per turn (e.g., 800): ").strip() or "800")

    opt_level = prompt_optimizer_level()

    m = MODELS[model]
    input_cost = (avg_input / 1_000_000) * m["input"]
    output_cost = (avg_output / 1_000_000) * m["output"]
    per_turn = input_cost + output_cost

    monthly_before = per_turn * rounds * days
    saving = OPTIMIZATION_SAVINGS[opt_level]
    monthly_after = monthly_before * (1 - saving)
    monthly_saved = monthly_before - monthly_after

    print("\n" + "=" * 48)
    print("  Cost Analysis Results")
    print("=" * 48)
    print(f"  Model: {model}")
    print(f"  Cost per turn: ${per_turn:.4f}")
    print(f"  Total monthly calls: {rounds * days}")
    print()
    print(f"  Monthly cost before optimization: ${monthly_before:.2f}")
    print(f"  Monthly cost after optimization:  ${monthly_after:.2f}")
    print(f"  Monthly savings:                  ${monthly_saved:.2f}  ({int(saving*100)}%)")
    print("=" * 48)

if __name__ == "__main__":
    main()