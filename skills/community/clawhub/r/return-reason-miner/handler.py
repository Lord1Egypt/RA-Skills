#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Sequence, Union

ReturnInput = Union[str, Dict[str, Any]]

REVIEW_MODE_RULES = {
    'Weekly Return Review': ['weekly', 'week', 'recurring'],
    'Launch Issue Triage': ['launch', 'new product', 'debut'],
    'Seasonal Trend Scan': ['seasonal', 'holiday', 'promo period', 'campaign'],
    'Vendor Quality Escalation': ['vendor', 'supplier', 'factory', 'quality issue'],
}

PRODUCT_CONTEXT_RULES = {
    'Apparel': ['apparel', 'size', 'fit', 'clothing'],
    'Beauty / Personal Care': ['beauty', 'skincare', 'cosmetic'],
    'Electronics': ['electronic', 'device', 'charger', 'battery'],
    'Home goods': ['home', 'kitchen', 'furniture', 'decor'],
    'Food / Perishable': ['food', 'perishable', 'fresh', 'frozen'],
}

REASON_RULES = {
    'Quality defect': ['defect', 'broken', 'faulty', 'quality issue'],
    'Size or fit mismatch': ['size', 'fit', 'too small', 'too big'],
    'Expectation mismatch': ['not as described', 'different than expected', 'color mismatch', 'expectation'],
    'Shipping damage': ['damaged', 'crushed', 'leaked', 'shipping damage'],
    'Wrong item or fulfillment error': ['wrong item', 'wrong color', 'wrong size', 'missing item', 'fulfillment'],
    'Late delivery or timing miss': ['late', 'delay', 'missed', 'too slow'],
}

SIGNAL_RULES = {
    'Return notes and free text': ['return note', 'refund note', 'feedback', 'reason'],
    'SKU or variant clues': ['sku', 'variant', 'size', 'color'],
    'Packaging or warehouse clues': ['warehouse', 'packaging', 'shipment', 'box'],
    'Review or rating clues': ['review', 'rating', 'star'],
    'Season or promo timing': ['holiday', 'launch', 'promo', 'campaign'],
}


def _normalize_input(user_input: ReturnInput) -> str:
    if isinstance(user_input, dict):
        chunks: List[str] = []
        for key in ['product_context', 'review_mode', 'signals', 'reasons', 'notes', 'constraints']:
            value = user_input.get(key)
            if not value:
                continue
            if isinstance(value, list):
                value = ', '.join(str(item) for item in value)
            chunks.append(f'{key}: {value}')
        return ' | '.join(chunks)
    return str(user_input or '').strip()


def _match_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    for label, keywords in rules.items():
        if any(keyword in text for keyword in keywords):
            return label
    return default


def _match_many(text: str, rules: Dict[str, Sequence[str]], default: List[str], limit: int = 4) -> List[str]:
    found = [label for label, keywords in rules.items() if any(keyword in text for keyword in keywords)]
    ordered: List[str] = []
    for item in found + default:
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _join(items: List[str]) -> str:
    return ', '.join(items) if items else 'None explicitly provided'


class ReturnReasonMiner:
    def __init__(self, user_input: ReturnInput):
        self.raw = user_input
        self.text = _normalize_input(user_input)
        self.lower = self.text.lower()
        self.review_mode = _match_one(self.lower, REVIEW_MODE_RULES, 'Weekly Return Review')
        self.product_context = _match_one(self.lower, PRODUCT_CONTEXT_RULES, 'Apparel')
        self.reason_clusters = _match_many(self.lower, REASON_RULES, ['Expectation mismatch', 'Quality defect'], limit=4)
        self.signals = _match_many(self.lower, SIGNAL_RULES, ['Return notes and free text', 'SKU or variant clues'], limit=4)

    def _taxonomy_rows(self) -> List[List[str]]:
        notes = {
            'Quality defect': ['Quality defect', 'Product or material issue', 'Review production quality, QC escapes, and vendor consistency.'],
            'Size or fit mismatch': ['Size or fit mismatch', 'Merchandising, spec, or expectation issue', 'Inspect size chart clarity, fit guidance, and variant labeling.'],
            'Expectation mismatch': ['Expectation mismatch', 'Listing, imagery, or messaging issue', 'Check whether claims, imagery, or use-case framing are overselling the product.'],
            'Shipping damage': ['Shipping damage', 'Packaging or carrier issue', 'Inspect packaging protection, handoff points, and damage concentration by route.'],
            'Wrong item or fulfillment error': ['Wrong item or fulfillment error', 'Warehouse or pick-pack issue', 'Audit SKU mapping, labeling, and process controls.'],
            'Late delivery or timing miss': ['Late delivery or timing miss', 'Carrier, planning, or promise-setting issue', 'Compare promised delivery windows with real operational capability.'],
        }
        return [notes[item] for item in self.reason_clusters if item in notes]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Return Reason Mining Brief')
        lines.append('')
        lines.append(f'**Review mode:** {self.review_mode}')
        lines.append(f'**Product context:** {self.product_context}')
        lines.append(f'**Priority reason clusters:** {_join(self.reason_clusters)}')
        lines.append(f'**Signals referenced:** {_join(self.signals)}')
        lines.append('**Method note:** This is a heuristic return-analysis brief. No live OMS, WMS, ERP, or return portal was accessed.')
        lines.append('')
        lines.append('## Return Pattern Summary')
        lines.append('- Separate product truth problems from fulfillment and expectation-management problems before choosing a fix.')
        lines.append('- Recurring returns matter more than memorable one-off anecdotes.')
        lines.append(f'- Because the main review mode is **{self.review_mode.lower()}**, the team should prioritize fixes that reduce preventable repeat returns.')
        lines.append('')
        lines.append('## Reason Taxonomy')
        lines.append('| Reason cluster | Likely owner lane | First inspection path |')
        lines.append('|---|---|---|')
        for row in self._taxonomy_rows():
            lines.append(f'| {row[0]} | {row[1]} | {row[2]} |')
        lines.append('')
        lines.append('## Root Cause Hypotheses')
        lines.append('- If quality defect signals are rising, inspect whether the issue is concentrated by batch, vendor, or recent process change.')
        lines.append('- If expectation mismatch dominates, inspect imagery, claims, and what the customer thought they were buying.')
        lines.append('- If fulfillment or delivery reasons are rising, isolate whether the issue began with warehouse accuracy, packaging, or promise-setting.')
        lines.append('')
        lines.append('## Fix Priorities')
        lines.append('1. Fix the preventable causes with the clearest recurrence and the simplest controllable owner.')
        lines.append('2. Improve listing clarity before redesigning the product when the problem is mostly expectation mismatch.')
        lines.append('3. Escalate vendor or packaging issues only after confirming the return notes point to the same pattern repeatedly.')
        lines.append('4. Track whether the same reason cluster returns after the first remediation cycle.')
        lines.append('')
        lines.append('## Cross-Functional Action Plan')
        lines.append('- **Product:** inspect spec, quality, and packaging assumptions.')
        lines.append('- **Merchandising / content:** tighten imagery, size guidance, claims, and comparison framing.')
        lines.append('- **Operations:** review pick-pack accuracy, shipping protection, and delivery promise discipline.')
        lines.append('- **CX:** standardize how return reasons are captured so future analysis is cleaner.')
        lines.append('')
        lines.append('## Assumptions and Limits')
        lines.append('- This brief is heuristic and depends on the return notes and context supplied by the user.')
        lines.append('- Root causes are hypotheses until validated by repeated evidence or operational review.')
        lines.append('- Final product, vendor, inventory, refund, and policy decisions remain human-approved.')
        return "\n".join(lines)


def handle(user_input: ReturnInput) -> str:
    return ReturnReasonMiner(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
