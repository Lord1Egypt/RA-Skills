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


def _detect_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    lower = text.lower()
    for label, keywords in rules.items():
        if any(keyword in lower for keyword in keywords):
            return label
    return default


def _detect_many(text: str, rules: Dict[str, Sequence[str]], default: List[str], limit: int = 4) -> List[str]:
    lower = text.lower()
    found = [label for label, keywords in rules.items() if any(keyword in lower for keyword in keywords)]
    ordered: List[str] = []
    for item in found + default:
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _join(items: Sequence[str]) -> str:
    return ", ".join(items) if items else "Not specified"


REVIEW_MODE_RULES = {
    "Daily payout check": ["daily", "yesterday", "daily settlement", "payout run"],
    "Weekly exception sweep": ["weekly", "exception sweep", "weekly review"],
    "Month-end close support": ["month-end", "month end", "close", "quarter close"],
    "Discrepancy investigation": ["discrepancy", "mismatch", "missing payout", "short paid", "unreconciled", "investigate"],
    "New channel setup review": ["new channel", "new psp", "new marketplace", "launch", "onboarding"],
}

CHANNEL_RULES = {
    "Marketplace settlement": ["amazon", "tiktok", "jd", "taobao", "marketplace"],
    "PSP / card acquiring": ["psp", "stripe", "adyen", "paypal", "card", "acquirer"],
    "Bank payout / remittance": ["bank", "statement", "remittance", "payout file"],
    "ERP / finance ledger": ["erp", "general ledger", "gl", "finance ledger", "journal"],
}

EVIDENCE_RULES = {
    "Order ledger": ["order ledger", "orders", "merchant ledger", "order report"],
    "Payout report": ["payout", "settlement report", "remittance advice", "provider report"],
    "Bank statement": ["bank statement", "statement", "bank file"],
    "Fee schedule": ["fee schedule", "mdr", "commission", "fee table", "pricing schedule"],
    "Refund log": ["refund", "refund log", "refund report"],
    "Chargeback or reserve log": ["chargeback", "reserve", "holdback", "dispute"],
    "Tax or invoice file": ["tax", "vat", "invoice", "fapiao"],
}

DISCREPANCY_RULES = {
    "Missing payout or delayed remittance": {
        "keywords": ["missing payout", "delayed payout", "remittance", "not received", "bank delay"],
        "why": "Cash expected from the channel has not landed when finance expects it to clear.",
        "check": "Compare payout schedule, processor release rules, and the bank statement timing before escalating a shortage claim.",
        "action": "Tag the batch, prove the expected amount, and separate timing delay from actual loss.",
    },
    "Fee mismatch": {
        "keywords": ["fee mismatch", "commission", "mdr", "higher fee", "rate error", "fee"],
        "why": "Incorrect fee application distorts margin and makes every downstream settlement look off.",
        "check": "Reconcile contracted rates, fee tiers, promotions, and tax treatment against the payout detail.",
        "action": "Build a fee-variance file and isolate systemic pricing-rule errors from one-off manual adjustments.",
    },
    "Refund timing mismatch": {
        "keywords": ["refund", "refund timing", "returned", "reversal", "refund delay"],
        "why": "Refunds often hit a different cycle than sales and can make a clean period look broken.",
        "check": "Match refund authorization date, customer completion date, and settlement-cycle impact separately.",
        "action": "Keep a cross-period refund schedule so finance does not double-count or chase normal timing differences.",
    },
    "Chargeback or reserve leakage": {
        "keywords": ["chargeback", "reserve", "holdback", "dispute", "rolling reserve"],
        "why": "Dispute and reserve mechanisms quietly withhold cash outside the core sales-versus-payout view.",
        "check": "Review reserve policy, release timing, and dispute workflow before calling it a settlement shortfall.",
        "action": "Split reserves and chargebacks into dedicated reconciliation buckets with named owners.",
    },
    "Order-to-payout mapping gap": {
        "keywords": ["mapping", "unmatched", "order missing", "sku missing", "join key", "reconcile"],
        "why": "When identifiers do not join cleanly, finance teams can neither explain the gap nor prove the true balance.",
        "check": "Validate order ID, payout batch, currency, and merchant reference keys across every source file.",
        "action": "Repair the join logic first, then investigate residual true discrepancies.",
    },
    "Tax or invoice variance": {
        "keywords": ["tax", "vat", "invoice", "fapiao", "withholding"],
        "why": "Tax treatment can legitimately change settlement math, but it is often misclassified as fee error or short payment.",
        "check": "Confirm invoice rules, withholding logic, and whether tax is grossed up or netted in the report.",
        "action": "Move tax review into the reconciliation checklist instead of handling it as an afterthought.",
    },
}


class SettlementReconciliationGuard:
    def __init__(self, inputs: Any):
        self.meta = _load_skill_meta()
        self.raw = inputs
        self.text = _normalize_inputs(inputs)
        self.lower = self.text.lower()
        self.review_mode = _detect_one(self.lower, REVIEW_MODE_RULES, "Daily payout check")
        self.channels = _detect_many(self.lower, CHANNEL_RULES, ["Marketplace settlement", "Bank payout / remittance"], limit=4)
        self.evidence = _detect_many(self.lower, EVIDENCE_RULES, ["Order ledger", "Payout report"], limit=5)
        self.discrepancies = self._detect_discrepancies()

    def _detect_discrepancies(self) -> List[str]:
        matched = [name for name, data in DISCREPANCY_RULES.items() if any(keyword in self.lower for keyword in data["keywords"])]
        defaults = {
            "Daily payout check": ["Missing payout or delayed remittance", "Order-to-payout mapping gap", "Fee mismatch"],
            "Weekly exception sweep": ["Order-to-payout mapping gap", "Fee mismatch", "Refund timing mismatch"],
            "Month-end close support": ["Refund timing mismatch", "Fee mismatch", "Tax or invoice variance"],
            "Discrepancy investigation": ["Missing payout or delayed remittance", "Fee mismatch", "Order-to-payout mapping gap"],
            "New channel setup review": ["Order-to-payout mapping gap", "Fee mismatch", "Tax or invoice variance"],
        }[self.review_mode]
        ordered: List[str] = []
        for item in matched + defaults:
            if item not in ordered:
                ordered.append(item)
        return ordered[:4]

    def _matching_logic_rows(self) -> List[List[str]]:
        return [
            ["Sales capture", "Order ledger to settlement detail", "Missing merchant references, currency drift, or split-order handling", "Make the join keys explicit before arguing about the money."],
            ["Fee application", "Contracted fee schedule to payout deductions", "Tier logic, promo rates, reserve deductions, or tax netting", "Prove expected fees separately from net cash movement."],
            ["Refund and reversal timing", "Refund log to payout cycle", "Cross-period timing and partial reversals", "Track timing buckets so expected reversals do not appear as unexplained loss."],
            ["Cash receipt", "Payout report to bank statement", "Bank delay, remittance timing, or reference mismatch", "Escalate to the provider only after the expected bank landing date is evidenced."],
        ]

    def _priorities(self) -> List[str]:
        items = [
            "Confirm the batch scope first, which channel, currency, date range, and settlement cycle are actually under review.",
            "Reconcile identifiers before reviewing commercial logic, because broken joins create fake fee and payout problems.",
            "Escalate only the residual exceptions that remain after timing, reserve, and refund mechanics are separated.",
        ]
        if "Bank statement" not in self.evidence:
            items.append("Request bank evidence before declaring a cash shortfall, because many payout disputes are really timing disputes.")
        return items[:4]

    def _close_controls(self) -> List[str]:
        return [
            "Keep one owner for source-file completeness and one owner for reconciliation logic when finance and operations both touch the workflow.",
            "Version the fee schedule and payout logic used for the reconciliation so month-end restatements are explainable later.",
            "Store exception decisions with evidence links so the next review cycle starts from confirmed facts instead of memory.",
            "Treat manual write-offs, reserve releases, and tax adjustments as separate approvals rather than hiding them in one balancing line.",
        ]

    def _assumptions(self) -> List[str]:
        notes = [
            "This brief is heuristic and uses only the user-supplied context plus the local skill description.",
            "No live settlement portal, bank feed, ERP, or PSP dashboard was queried.",
            "Final accounting treatment, dispute escalation, and journal posting remain human-approved.",
        ]
        missing = [item for item in ["Fee schedule", "Bank statement", "Refund log"] if item not in self.evidence]
        if missing:
            notes.append(f"Lightly referenced evidence sources: {_join(missing)}.")
        return notes

    def render(self) -> str:
        lines: List[str] = []
        lines.append("# Settlement Reconciliation Guard")
        lines.append("")
        lines.append(f"**Skill description:** {self.meta['description']}")
        lines.append(f"**Review mode:** {self.review_mode}")
        lines.append(f"**Channels in scope:** {_join(self.channels)}")
        lines.append(f"**Primary discrepancy themes:** {_join(self.discrepancies)}")
        lines.append(f"**Evidence referenced:** {_join(self.evidence)}")
        lines.append(f"**Input snapshot:** {self.text or 'No structured settlement context was provided, so this brief uses default reconciliation-control assumptions.'}")
        lines.append("")
        lines.append("## Reconciliation Summary")
        lines.append("- Separate timing differences from true settlement errors before escalating a financial discrepancy.")
        lines.append("- Reconciliation works best when order, fee, refund, reserve, and cash-receipt logic are reviewed as distinct layers.")
        lines.append(f"- Because the main review mode is **{self.review_mode.lower()}**, the output emphasizes exception containment and evidence quality over premature root-cause certainty.")
        lines.append("")
        lines.append("## Matching Logic Table")
        lines.append("| Match stage | What to align | Common breakpoints | Control note |")
        lines.append("|---|---|---|---|")
        for row in self._matching_logic_rows():
            lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")
        lines.append("")
        lines.append("## Discrepancy Queue")
        lines.append("| Discrepancy theme | Why it matters | First check | Default response |")
        lines.append("|---|---|---|---|")
        for name in self.discrepancies:
            info = DISCREPANCY_RULES[name]
            lines.append(f"| {name} | {info['why']} | {info['check']} | {info['action']} |")
        lines.append("")
        lines.append("## Investigation Priorities")
        for idx, item in enumerate(self._priorities(), 1):
            lines.append(f"{idx}. {item}")
        lines.append("")
        lines.append("## Close Controls")
        for item in self._close_controls():
            lines.append(f"- {item}")
        lines.append("")
        lines.append("## Assumptions and Limits")
        for note in self._assumptions():
            lines.append(f"- {note}")
        return "\n".join(lines)


def handle(inputs: Any) -> str:
    return SettlementReconciliationGuard(inputs).render()


if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
