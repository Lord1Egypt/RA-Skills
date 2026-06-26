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


OBJECTIVE_RULES = {
    "Inventory synchronization": ["inventory", "stock", "availability", "qty", "quantity", "on-hand", "on hand"],
    "Catalog and pricing alignment": ["catalog", "attribute", "title", "spec", "sku", "price", "cost"],
    "Order and fulfillment handoff": ["order", "shipment", "tracking", "fulfillment", "asn", "po"],
    "Supplier onboarding and master-data setup": ["onboarding", "new supplier", "template", "master data", "mapping", "integration"],
    "Exception and discrepancy review": ["exception", "mismatch", "failed sync", "error", "duplicate", "conflict"],
}

CADENCE_RULES = {
    "Real-time or intraday control": ["real-time", "realtime", "hourly", "intraday", "live"],
    "Daily control cycle": ["daily", "overnight", "every day", "morning", "day-end"],
    "Weekly operating review": ["weekly", "this week", "weekly review"],
    "Launch or cutover preparation": ["launch", "go-live", "cutover", "first sync", "onboarding"],
}

SYSTEM_RULES = {
    "ERP": ["erp", "sap", "netsuite", "kingdee", "u8"],
    "WMS": ["wms", "warehouse"],
    "OMS": ["oms", "order management"],
    "PIM / Catalog": ["pim", "catalog", "product info"],
    "Marketplace / Storefront": ["amazon", "shopify", "tiktok", "jd", "taobao", "marketplace", "storefront"],
    "Supplier portal / spreadsheet": ["supplier portal", "portal", "spreadsheet", "excel", "csv", "template"],
}

RISK_RULES = {
    "SKU mapping mismatch": {
        "keywords": ["mapping", "sku mismatch", "wrong sku", "attribute mismatch", "id mismatch"],
        "why": "Broken identifiers make every downstream sync look unstable even when the transport layer is working.",
        "check": "Confirm internal SKU, supplier SKU, barcode, variant, and unit definitions resolve to one source of truth.",
        "action": "Freeze risky changes, repair the mapping table, and re-run only the affected records.",
    },
    "Inventory latency": {
        "keywords": ["inventory lag", "stock lag", "latency", "oversell", "availability", "qty"],
        "why": "Late inventory updates turn healthy demand into oversells, cancellations, or false replenishment signals.",
        "check": "Measure how long supplier, warehouse, and storefront stock snapshots remain inconsistent.",
        "action": "Shorten the sync loop, isolate the slow system, and define a fallback availability policy.",
    },
    "Price or cost mismatch": {
        "keywords": ["price", "cost", "margin", "currency", "discount"],
        "why": "Pricing drift can create channel conflict, margin leakage, or supplier disputes very quickly.",
        "check": "Review which system owns sell price, buy cost, tax, and currency conversion logic.",
        "action": "Lock the price source of truth and reconcile only approved price updates across channels.",
    },
    "Pack size or MOQ mismatch": {
        "keywords": ["pack size", "moq", "case pack", "carton", "uom", "unit"],
        "why": "Unit-of-measure confusion makes purchasing, receiving, and sellable stock numbers disagree.",
        "check": "Inspect whether pack, carton, MOQ, and sellable unit definitions are being converted consistently.",
        "action": "Document the conversion rules and test edge cases before expanding the integration scope.",
    },
    "Duplicate or missing order events": {
        "keywords": ["duplicate order", "missing order", "retry", "resend", "tracking", "shipment"],
        "why": "Order-event drift creates fulfillment noise and corrupts downstream operational reporting.",
        "check": "Review event idempotency, retry logic, and whether acknowledgements are persisted correctly.",
        "action": "Quarantine duplicate flows, reissue the missing events, and tighten event-state logging.",
    },
    "Supplier SLA drift": {
        "keywords": ["sla", "delay", "lead time", "supplier delay", "late"],
        "why": "Supplier timing drift can make a technically correct sync operationally unreliable.",
        "check": "Compare promised lead time, confirmation time, and exception response time against reality.",
        "action": "Escalate the supplier operating review and separate data issues from true supply issues.",
    },
}


class SupplierSyncManager:
    def __init__(self, inputs: Any):
        self.meta = _load_skill_meta()
        self.raw = inputs
        self.text = _normalize_inputs(inputs)
        self.lower = self.text.lower()
        self.objective = _detect_one(self.lower, OBJECTIVE_RULES, "Inventory synchronization")
        self.cadence = _detect_one(self.lower, CADENCE_RULES, "Daily control cycle")
        self.systems = _detect_many(self.lower, SYSTEM_RULES, ["ERP", "Supplier portal / spreadsheet"], limit=5)
        self.risks = self._detect_risks()

    def _detect_risks(self) -> List[str]:
        matched = [name for name, data in RISK_RULES.items() if any(keyword in self.lower for keyword in data["keywords"])]
        defaults = {
            "Inventory synchronization": ["Inventory latency", "SKU mapping mismatch", "Supplier SLA drift"],
            "Catalog and pricing alignment": ["Price or cost mismatch", "SKU mapping mismatch", "Pack size or MOQ mismatch"],
            "Order and fulfillment handoff": ["Duplicate or missing order events", "Supplier SLA drift", "SKU mapping mismatch"],
            "Supplier onboarding and master-data setup": ["SKU mapping mismatch", "Pack size or MOQ mismatch", "Supplier SLA drift"],
            "Exception and discrepancy review": ["SKU mapping mismatch", "Inventory latency", "Price or cost mismatch"],
        }[self.objective]
        ordered: List[str] = []
        for item in matched + defaults:
            if item not in ordered:
                ordered.append(item)
        return ordered[:4]

    def _control_rows(self) -> List[List[str]]:
        rows: List[List[str]] = []
        for risk in self.risks:
            info = RISK_RULES[risk]
            rows.append([risk, info["why"], info["check"], info["action"]])
        return rows

    def _field_watchlist(self) -> List[str]:
        items = [
            "Confirm one canonical key path for internal SKU, supplier SKU, barcode, and variant identifiers.",
            "Review owner rules for price, cost, available quantity, lead time, and pack-size fields before automation expands.",
            "Check whether nulls, blanks, and zero values have different meanings across supplier files and internal systems.",
        ]
        if "Marketplace / Storefront" in self.systems:
            items.append("Verify storefront-ready fields, publish flags, and channel-specific attribute requirements are mapped deliberately.")
        if self.objective == "Order and fulfillment handoff":
            items.append("Map acknowledgment, shipment, cancellation, and return statuses to one shared event language.")
        return items[:4]

    def _cadence_notes(self) -> List[str]:
        notes = {
            "Real-time or intraday control": [
                "Use lightweight exception thresholds, because real-time sync work fails when every tiny delta becomes an alarm.",
                "Track lag between source update and downstream visibility so teams can tell data delay from true stock risk.",
                "Keep a manual fallback path for high-value SKUs when the automation is degraded.",
            ],
            "Daily control cycle": [
                "Start each cycle with the previous day's failed or partial sync queue, not just the fresh file drop.",
                "Separate structural issues from one-off supplier file mistakes so the team does not overreact to noise.",
                "Close the day with an owner-confirmed exception list and a re-run decision.",
            ],
            "Weekly operating review": [
                "Use the week to spot repeat breaks by supplier, field, or system rather than treating every incident as unique.",
                "Review whether manual fixes are quietly replacing a missing productized control.",
                "Escalate only the patterns that create real commercial or operational risk.",
            ],
            "Launch or cutover preparation": [
                "Run a pre-launch file rehearsal with edge cases, not just a happy-path sample.",
                "Confirm ownership for rollback, freeze windows, and master-data approval before the first live sync.",
                "Limit initial scope so the first live cycle teaches the team something controllable.",
            ],
        }
        return notes[self.cadence]

    def _exception_queue(self) -> List[str]:
        return [
            "Critical: records that would cause oversell, wrong price, or broken order routing if left unresolved.",
            "High: supplier rows missing identifiers, unit definitions, or mandatory commercial fields.",
            "Medium: stale confirmations, repeated retries, or low-volume mismatches that still need root-cause ownership.",
            "Owner rule: one person owns supplier follow-up and one person owns internal-system correction when the issue crosses both sides.",
        ]

    def _assumptions(self) -> List[str]:
        notes = [
            "This brief is heuristic and uses only the user's context plus the local skill description.",
            "No live ERP, OMS, WMS, supplier portal, or marketplace API was queried.",
            "Master-data changes, supplier SLAs, and sync reruns should remain human-approved.",
        ]
        missing = [system for system in ["WMS", "Marketplace / Storefront", "OMS"] if system not in self.systems]
        if missing:
            notes.append(f"Lightly referenced systems in the prompt: {_join(missing)}.")
        return notes

    def render(self) -> str:
        lines: List[str] = []
        lines.append("# Supplier Sync Management Brief")
        lines.append("")
        lines.append(f"**Skill description:** {self.meta['description']}")
        lines.append(f"**Primary sync objective:** {self.objective}")
        lines.append(f"**Operating cadence:** {self.cadence}")
        lines.append(f"**Systems referenced:** {_join(self.systems)}")
        lines.append(f"**Priority risk themes:** {_join(self.risks)}")
        lines.append(f"**Input snapshot:** {self.text or 'No structured supplier-sync context was provided, so this brief uses default operational-control assumptions.'}")
        lines.append("")
        lines.append("## Sync Scope Summary")
        lines.append("- Treat supplier sync as an operating-control problem, not just a file-transfer problem.")
        lines.append("- Decide which system is authoritative for each commercial and operational field before scaling automation.")
        lines.append(f"- Because the main objective is **{self.objective.lower()}**, the first controls should reduce repeat exceptions rather than just clean up today's queue.")
        lines.append("")
        lines.append("## Recommended Control Table")
        lines.append("| Risk area | Why it matters | First control question | Default response |")
        lines.append("|---|---|---|---|")
        for row in self._control_rows():
            lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")
        lines.append("")
        lines.append("## Field Mapping Watchlist")
        for item in self._field_watchlist():
            lines.append(f"- {item}")
        lines.append("")
        lines.append("## Operating Cadence")
        for idx, item in enumerate(self._cadence_notes(), 1):
            lines.append(f"{idx}. {item}")
        lines.append("")
        lines.append("## Exception Queue Design")
        for item in self._exception_queue():
            lines.append(f"- {item}")
        lines.append("")
        lines.append("## Assumptions and Limits")
        for note in self._assumptions():
            lines.append(f"- {note}")
        return "\n".join(lines)


def handle(inputs: Any) -> str:
    return SupplierSyncManager(inputs).render()


if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
