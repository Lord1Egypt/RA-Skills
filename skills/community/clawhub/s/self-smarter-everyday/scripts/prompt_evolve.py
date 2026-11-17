#!/usr/bin/env python3
"""
prompt_evolve.py — Prompt evolution and version control.

Reads current prompt variants, applies mutation strategies, evaluates
fitness based on historical performance, and selects the best variants
for the next cycle.

Mutation Strategies:
  - CLONE:       Copy the best-performing variant (baseline)
  - REPHRASE:    Shuffle instruction order
  - CONSTRAIN:   Add a constraint or guardrail
  - RELAX:       Remove a constraint (if fitness allows)
  - COMBINE:     Merge elements from two top variants

Fitness Evaluation:
  - Based on task success rate from reflection logs
  - Token efficiency from audit data
  - Error frequency from error logs

Usage:
  python3 prompt_evolve.py [--state-dir DIR] [--generations N] [--dry-run]
"""

import argparse
import copy
import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_STATE_DIR = os.path.expanduser("~/self-smarter/state")
PROMPTS_DIR_NAME = "prompts"
MAX_VARIANTS = 10
MUTATION_RATE = 0.3

# ---------------------------------------------------------------------------
# Prompt storage
# ---------------------------------------------------------------------------
def load_prompts(state_dir: Path) -> dict:
    """Load prompt variants from state directory."""
    prompts_dir = state_dir / PROMPTS_DIR_NAME
    if not prompts_dir.exists():
        return {"variants": [], "generation": 0, "best_variant_id": None}
    index_file = prompts_dir / "index.json"
    if index_file.exists():
        with open(index_file, "r") as f:
            return json.load(f)
    return {"variants": [], "generation": 0, "best_variant_id": None}

def save_prompts(state_dir: Path, prompts: dict):
    """Save prompt variants to state directory."""
    prompts_dir = state_dir / PROMPTS_DIR_NAME
    prompts_dir.mkdir(parents=True, exist_ok=True)
    index_file = prompts_dir / "index.json"
    with open(index_file, "w") as f:
        json.dump(prompts, f, indent=2)

def save_variant(state_dir: Path, variant: dict):
    """Save a single variant to disk."""
    prompts_dir = state_dir / PROMPTS_DIR_NAME
    variant_file = prompts_dir / f"variant_{variant['id']}.json"
    with open(variant_file, "w") as f:
        json.dump(variant, f, indent=2)

# ---------------------------------------------------------------------------
# Mutation strategies
# ---------------------------------------------------------------------------
def mutate_clone(variant: dict, new_id: str) -> dict:
    """Clone the best variant with a new ID."""
    new_variant = copy.deepcopy(variant)
    new_variant["id"] = new_id
    new_variant["parent_id"] = variant["id"]
    new_variant["generation"] = variant.get("generation", 0) + 1
    new_variant["created"] = datetime.now().isoformat()
    new_variant["mutation"] = "clone"
    new_variant["fitness"] = 0.0  # untested
    return new_variant

def mutate_rephrase(variant: dict, new_id: str) -> dict:
    """Reorder instruction blocks in the prompt."""
    new_variant = copy.deepcopy(variant)
    new_variant["id"] = new_id
    new_variant["parent_id"] = variant["id"]
    new_variant["generation"] = variant.get("generation", 0) + 1
    new_variant["created"] = datetime.now().isoformat()
    new_variant["mutation"] = "rephrase"
    # Shuffle instruction order if instructions is a list
    if isinstance(new_variant.get("instructions"), list):
        random.shuffle(new_variant["instructions"])
    new_variant["fitness"] = 0.0
    return new_variant

def mutate_constrain(variant: dict, new_id: str) -> dict:
    """Add a new constraint to the prompt."""
    new_variant = copy.deepcopy(variant)
    new_variant["id"] = new_id
    new_variant["parent_id"] = variant["id"]
    new_variant["generation"] = variant.get("generation", 0) + 1
    new_variant["created"] = datetime.now().isoformat()
    new_variant["mutation"] = "constrain"
    constraints = new_variant.get("constraints", [])
    new_constraints = [
        "Validate output before delivering",
        "Minimize token usage without losing clarity",
        "Check for edge cases before executing",
        "Prefer cached data over API calls",
    ]
    unused = [c for c in new_constraints if c not in constraints]
    if unused:
        constraints.append(random.choice(unused))
    new_variant["constraints"] = constraints
    new_variant["fitness"] = 0.0
    return new_variant

def mutate_relax(variant: dict, new_id: str) -> dict:
    """Remove a constraint from the prompt."""
    new_variant = copy.deepcopy(variant)
    new_variant["id"] = new_id
    new_variant["parent_id"] = variant["id"]
    new_variant["generation"] = variant.get("generation", 0) + 1
    new_variant["created"] = datetime.now().isoformat()
    new_variant["mutation"] = "relax"
    constraints = new_variant.get("constraints", [])
    if constraints:
        removed = constraints.pop(random.randrange(len(constraints)))
        new_variant["relaxed_constraint"] = removed
    new_variant["fitness"] = 0.0
    return new_variant

def mutate_combine(variant_a: dict, variant_b: dict, new_id: str) -> dict:
    """Combine elements from two variants."""
    new_variant = copy.deepcopy(variant_a)
    new_variant["id"] = new_id
    new_variant["parent_id"] = f"{variant_a['id']}+{variant_b['id']}"
    new_variant["generation"] = max(variant_a.get("generation", 0), variant_b.get("generation", 0)) + 1
    new_variant["created"] = datetime.now().isoformat()
    new_variant["mutation"] = "combine"
    # Merge constraints (union)
    constraints_a = set(variant_a.get("constraints", []))
    constraints_b = set(variant_b.get("constraints", []))
    new_variant["constraints"] = list(constraints_a | constraints_b)
    new_variant["fitness"] = 0.0
    return new_variant

MUTATIONS = {
    "clone": lambda v, nid: mutate_clone(v, nid),
    "rephrase": lambda v, nid: mutate_rephrase(v, nid),
    "constrain": lambda v, nid: mutate_constrain(v, nid),
    "relax": lambda v, nid: mutate_relax(v, nid),
}

# ---------------------------------------------------------------------------
# Fitness evaluation
# ---------------------------------------------------------------------------
def evaluate_fitness(state_dir: Path, variant: dict) -> float:
    """Evaluate variant fitness from historical data."""
    # Check audit data for success rate
    audit_file = state_dir / "audit_latest.json"
    success_rate = 0.5  # default neutral
    if audit_file.exists():
        with open(audit_file, "r") as f:
            audit = json.load(f)
        success_rate = audit.get("performance", {}).get("success_rate", 0.5)

    # Base fitness from success rate
    fitness = success_rate * 0.6

    # Bonus for having constraints (structure = better)
    constraint_bonus = min(len(variant.get("constraints", [])) * 0.05, 0.2)
    fitness += constraint_bonus

    # Bonus for higher generation (survived evolution)
    gen_bonus = min(variant.get("generation", 0) * 0.02, 0.2)
    fitness += gen_bonus

    return round(min(fitness, 1.0), 4)

# ---------------------------------------------------------------------------
# Evolution cycle
# ---------------------------------------------------------------------------
def evolve(state_dir: Path, generations: int, dry_run: bool) -> dict:
    """Run evolution cycle."""
    prompts = load_prompts(state_dir)
    variants = prompts.get("variants", [])
    current_gen = prompts.get("generation", 0)

    print(f"Starting evolution from generation {current_gen}")
    print(f"Current variants: {len(variants)}")

    for gen in range(generations):
        current_gen += 1
        print(f"\n--- Generation {current_gen} ---")

        # Evaluate all existing variants
        for v in variants:
            v["fitness"] = evaluate_fitness(state_dir, v)

        # Sort by fitness (descending)
        variants.sort(key=lambda x: x["fitness"], reverse=True)

        # Select top performers
        elite_count = max(2, len(variants) // 3)
        elite = variants[:elite_count]
        best = elite[0] if elite else None

        if best:
            print(f"  Best variant: {best['id']} (fitness={best['fitness']:.4f}, mutation={best.get('mutation', 'original')})")

        # Generate new variants through mutation
        new_variants = list(elite)  # keep elite
        variant_counter = len(variants) + 1

        for _ in range(min(4, MAX_VARIANTS - len(elite))):
            if not elite:
                break
            parent = random.choice(elite)
            mutation_type = random.choice(list(MUTATIONS.keys()))
            new_id = f"v{current_gen}_{variant_counter}"
            mutation_fn = MUTATIONS[mutation_type]
            new_v = mutation_fn(parent, new_id)
            new_variants.append(new_v)
            variant_counter += 1
            print(f"  Created: {new_id} via {mutation_type} (parent: {parent['id']})")

        # Occasionally combine two elites
        if len(elite) >= 2 and random.random() < MUTATION_RATE:
            new_id = f"v{current_gen}_{variant_counter}"
            combined = mutate_combine(elite[0], elite[1], new_id)
            new_variants.append(combined)
            variant_counter += 1
            print(f"  Created: {new_id} via combine (parents: {elite[0]['id']}+{elite[1]['id']})")

        # Cap at MAX_VARIANTS
        variants = new_variants[:MAX_VARIANTS]

        if not dry_run:
            prompts["variants"] = variants
            prompts["generation"] = current_gen
            prompts["best_variant_id"] = variants[0]["id"] if variants else None
            save_prompts(state_dir, prompts)
            for v in variants:
                save_variant(state_dir, v)

    print(f"\nEvolution complete. {len(variants)} variants in generation {current_gen}")
    return {"generation": current_gen, "variant_count": len(variants),
            "best_id": variants[0]["id"] if variants else None}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Prompt evolution")
    parser.add_argument("--state-dir", type=str, default=DEFAULT_STATE_DIR)
    parser.add_argument("--generations", type=int, default=1, help="Number of generations to evolve")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    state_dir = Path(args.state_dir)
    result = evolve(state_dir, args.generations, args.dry_run)
    print(f"\nResult: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
