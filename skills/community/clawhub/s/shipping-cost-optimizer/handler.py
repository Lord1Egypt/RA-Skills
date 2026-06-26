#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence


def _load_skill_meta() -> Dict[str, str]:
    skill_path = Path(__file__).with_name("SKILL.md")
    text = skill_path.read_text(encoding="utf-8")
    frontmatter = ""
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            frontmatter = parts[1]
            body = parts[2]

    data: Dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")

    title = data.get("name", Path(__file__).resolve().parent.name.replace("-", " ").title())
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    return {
        "name": data.get("name", title),
        "title": title,
        "description": data.get("description", title),
    }


def _normalize_inputs(inputs: Any) -> str:
    if inputs is None:
        return ""
    if isinstance(inputs, str):
        return inputs.strip()
    if isinstance(inputs, dict):
        parts: List[str] = []
        for key, value in inputs.items():
            if value in (None, "", [], {}, ()):  # type: ignore[comparison-overlap]
                continue
            if isinstance(value, (list, tuple, set)):
                rendered = ", ".join(str(item) for item in value)
            else:
                rendered = str(value)
            parts.append(f"{key}: {rendered}")
        return " | ".join(parts)
    if isinstance(inputs, (list, tuple, set)):
        return " | ".join(str(item) for item in inputs)
    try:
        return json.dumps(inputs, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(inputs)


def _detect_many(text: str, rules: Dict[str, Sequence[str]], default: List[str], limit: int = 4) -> List[str]:
    lower = text.lower()
    found = [label for label, keywords in rules.items() if any(keyword in lower for keyword in keywords)]
    ordered: List[str] = []
    for item in found + default:
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _detect_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    lower = text.lower()
    for label, keywords in rules.items():
        if any(keyword in lower for keyword in keywords):
            return label
    return default


def _join(items: Sequence[str]) -> str:
    return ", ".join(items) if items else "Not specified"


OBJECTIVE_RULES = {
    "Packaging rationalization": ["packaging", "box", "carton", "overpack", "包材", "包装"],
    "Carrier routing review": ["carrier", "courier", "routing", "快递", "承运商", "route"],
    "Free-shipping policy reset": ["free shipping", "threshold", "免邮", "shipping promo"],
    "Regional profitability control": ["region", "zone", "偏远", "remote", "loss-making", "区域"],
    "Cross-border caution": ["cross-border", "customs", "duty", "international", "跨境"],
}

SIGNAL_RULES = {
    "Order weight / volume": ["weight", "volume", "dimensional", "kg", "尺寸", "体积", "重量"],
    "Packaging specs": ["packaging", "box", "carton", "包材", "包装"],
    "Carrier pricing": ["carrier", "courier", "rate", "quote", "承运商", "报价", "运费"],
    "Region mix / surcharge": ["region", "zone", "remote", "偏远", "区域", "surcharge"],
    "Free-shipping rule": ["free shipping", "threshold", "免邮", "shipping promo"],
    "Experience guardrail": ["premium", "luxury", "unboxing", "fragile", "fast delivery", "高端", "易碎", "时效"],
}

OPPORTUNITY_LIBRARY = {
    "Packaging rationalization": {
        "pain": "The parcel is likely paying for excess cube, filler, or unnecessary material complexity.",
        "recommendation": "Standardize pack tiers, remove over-boxing where safe, and match packaging to actual order profiles instead of habit.",
        "difficulty": "Low to medium",
        "impact": "Reduces freight, packaging cost, and handling waste if damage risk remains controlled.",
    },
    "Carrier routing review": {
        "pain": "The current carrier split may reflect legacy habit rather than the best current lane economics.",
        "recommendation": "Re-benchmark route logic by zone, order type, and SLA so the cheapest acceptable carrier wins more often.",
        "difficulty": "Medium",
        "impact": "Can lower unit freight cost while protecting service-level targets when lane logic is clean.",
    },
    "Free-shipping policy reset": {
        "pain": "The threshold may be converting orders at the cost of avoidable margin erosion.",
        "recommendation": "Test a higher threshold, bundle encouragement, or member-only rule instead of subsidizing every order equally.",
        "difficulty": "Medium",
        "impact": "Improves order economics if conversion loss stays within an acceptable range.",
    },
    "Regional profitability control": {
        "pain": "Some zones may look healthy on revenue but become negative after remote or low-density shipping costs.",
        "recommendation": "Create region-specific rules, exclusions, or slower-service defaults where profitability repeatedly breaks.",
        "difficulty": "Medium to high",
        "impact": "Protects contribution margin and reveals where geographic demand is expensive to serve.",
    },
    "Cross-border caution": {
        "pain": "Cross-border cost layers can distort shipping economics far beyond domestic assumptions.",
        "recommendation": "Model duties, customs variance, and exception handling separately before rolling out any broad shipping-cost promise.",
        "difficulty": "High",
        "impact": "Prevents underpricing and protects against operational surprises in international lanes.",
    },
}

EXPERIENCE_RULES = {
    "Premium brand or unboxing sensitivity": ["premium", "luxury", "unboxing", "高端"],
    "Speed-sensitive delivery promise": ["fast delivery", "same day", "next day", "时效"],
    "Fragile-product protection": ["fragile", "breakable", "易碎"],
}


class ShippingCostOptimizer:
    def __init__(self, user_input: Any):
        self.raw = user_input
        self.text = _normalize_inputs(user_input)
        self.lower = self.text.lower()
        self.primary_objective = _detect_one(self.text, OBJECTIVE_RULES, "Packaging rationalization")
        self.signals = _detect_many(
            self.text,
            SIGNAL_RULES,
            ["Order weight / volume", "Carrier pricing", "Packaging specs"],
            limit=6,
        )
        self.opportunities = _detect_many(
            self.text,
            OBJECTIVE_RULES,
            ["Packaging rationalization", "Carrier routing review", "Free-shipping policy reset"],
            limit=4,
        )
        self.guardrail = _detect_one(self.text, EXPERIENCE_RULES, "Balanced shipping cost versus service level")

    def _pilot_plan(self) -> List[str]:
        items = [
            "Weeks 1-2: measure the current waste source with one clean baseline instead of changing packaging, routing, and thresholds all at once.",
            "Weeks 2-4: run the lowest-friction pilot first in one lane, region, or order profile where the economics are most obviously weak.",
            "Month 2: decide whether the result is strong enough for rollout after reviewing profit, damage, speed, and customer-experience effects together.",
        ]
        if self.primary_objective == "Free-shipping policy reset":
            items[1] = "Weeks 2-4: test the revised threshold or offer rule in one traffic cohort so conversion and margin quality can be read together."
        if self.primary_objective == "Carrier routing review":
            items[1] = "Weeks 2-4: pilot a cleaner carrier split in one stable lane before rewriting the whole routing policy."
        return items

    def _risk_notes(self) -> List[str]:
        notes = [
            "Cost reduction is only good if delivery speed, damage rate, and service quality remain inside acceptable guardrails.",
            "Keep carrier contract changes, routing rules, and shipping-policy updates human-approved.",
        ]
        if self.guardrail != "Balanced shipping cost versus service level":
            notes.append(f"Special watchout: {self.guardrail} should be protected during any pilot.")
        if "Cross-border caution" in self.opportunities:
            notes.append("International shipping assumptions often drift quickly, so broad cross-border promises should be treated carefully.")
        return notes

    def render(self) -> str:
        meta = _load_skill_meta()
        lines: List[str] = []
        lines.append("# Shipping Cost Optimization Report")
        lines.append("")
        lines.append(f"**Skill description:** {meta['description']}")
        lines.append(f"**Primary objective:** {self.primary_objective}")
        lines.append(f"**Signals referenced:** {_join(self.signals)}")
        lines.append(f"**Experience guardrail:** {self.guardrail}")
        lines.append(f"**Input snapshot:** {self.text or 'No structured logistics brief was provided, so this report uses default ecommerce fulfillment assumptions.'}")
        lines.append("")
        lines.append("## Cost Snapshot")
        lines.append("- Start with the largest repeatable waste source before chasing every marginal shipping-cost hypothesis at once.")
        lines.append(f"- Because the main job is **{self.primary_objective.lower()}**, the first pilot should isolate that lever and avoid mixing too many policy changes together.")
        lines.append("- Treat shipping cost as a combined packaging, carrier, policy, and customer-experience problem, not just a freight invoice line.")
        lines.append("")
        lines.append("## Optimization Opportunities")
        lines.append("| Opportunity | Current pain pattern | Recommendation | Difficulty | Business impact |")
        lines.append("|---|---|---|---|---|")
        for opportunity in self.opportunities:
            details = OPPORTUNITY_LIBRARY[opportunity]
            lines.append(
                f"| {opportunity} | {details['pain']} | {details['recommendation']} | {details['difficulty']} | {details['impact']} |"
            )
        lines.append("")
        lines.append("## Pilot Recommendations")
        for idx, item in enumerate(self._pilot_plan(), 1):
            lines.append(f"{idx}. {item}")
        lines.append("")
        lines.append("## Experience and Risk Notes")
        for note in self._risk_notes():
            lines.append(f"- {note}")
        lines.append("")
        lines.append("## Assumptions and Limits")
        lines.append("- This is a heuristic cost-reduction brief, not a live TMS or carrier-routing engine.")
        lines.append("- Incomplete rate cards or regional data will reduce confidence in the projected savings range.")
        lines.append("- Final policy, routing, packaging, and customer-facing promise changes should stay human-approved.")
        return "\n".join(lines)


def handle(user_input: Any) -> str:
    return ShippingCostOptimizer(user_input).render()


if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
