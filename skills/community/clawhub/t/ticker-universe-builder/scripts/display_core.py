"""Explicit presentation groups; never infer economic identity from small counts."""

from collections import defaultdict


def display_groups(plan, profile):
    return plan.get("display_groups", {}).get(profile, [])


def theme_groups(plan, profile="heavy"):
    return {theme: row["id"] for row in display_groups(plan, profile)
            for theme in row["themes"]}


def display_view(universe):
    """Return group labels and rows without rewriting any researched member facts."""
    plan = universe.get("coverage_plan", {})
    mapping = theme_groups(plan, universe["profile"])
    taxonomy = {t["theme_code"]: t for t in universe["taxonomy"]}
    labels = {k: t["theme_name"] for k, t in taxonomy.items()}
    labels.update({g["id"]: g["name"] for g in display_groups(plan, universe["profile"])})
    grouped = defaultdict(list)
    for row in universe["members"] + plan.get("references", []):
        grouped[mapping.get(row["theme_code"], row["theme_code"])].append(row)
    return labels, grouped
