#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

ActionInput = Union[str, Dict[str, Any]]

FOCUS_RULES = {
    'Receiving / Dock Flow': ['receiving', 'dock', 'unload', 'carrier', 'cutoff'],
    'Slotting / Putaway': ['slotting', 'putaway', 'bin', 'layout', 'travel time'],
    'Picking / Packing': ['picking', 'pick', 'packing', 'pack', 'wave', 'congestion'],
    'Replenishment Control': ['replenishment', 'stockout', 'top-off', 'forward pick', 'refill'],
    'Labor Balancing': ['labor', 'shift', 'headcount', 'cross-train', 'productivity'],
}

SIGNAL_RULES = {
    'Queue / Congestion': ['queue', 'congestion', 'wave', 'jam', 'backlog'],
    'Travel Time Waste': ['travel time', 'walking', 'distance', 'layout', 'slotting'],
    'Pick / Pack Accuracy': ['accuracy', 'mispick', 'error', 'rework', 'wrong item'],
    'Inventory Accuracy / Replenishment': ['inventory', 'stockout', 'replenishment', 'count', 'forward pick'],
    'Space Utilization': ['space', 'cube', 'slot', 'staging', 'overflow'],
    'Labor Imbalance': ['labor', 'shift', 'staffing', 'cross-train', 'headcount'],
    'Cutoff / Service Risk': ['cutoff', 'sla', 'carrier', 'late', 'same day'],
}

CONSTRAINT_RULES = {
    'Fixed layout': ['fixed layout', 'cannot move', 'layout constraint'],
    'Headcount cap': ['headcount', 'labor cap', 'hiring freeze'],
    'Peak pressure': ['peak', 'holiday', 'surge'],
    'Service-level commitment': ['sla', 'cutoff', 'same day', 'next day'],
    'Low automation flexibility': ['manual', 'no automation', 'limited automation'],
}


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for keyword in keywords if keyword in text) for name, keywords in rules.items()}


def _join_list(items: List[str]) -> str:
    return ', '.join(items) if items else 'None explicitly provided'


class WarehouseFlowOptimizer:
    def __init__(self, user_input: ActionInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.focus = self._detect_focus()
        self.signals = self._detect_signals()
        self.constraints = self._detect_constraints()

    def _normalize_input(self, user_input: ActionInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['objective', 'zones', 'signals', 'constraints', 'notes']:
                value = user_input.get(key)
                if not value:
                    continue
                if isinstance(value, list):
                    value = ', '.join(str(item) for item in value)
                chunks.append(f'{key}: {value}')
            return ' | '.join(chunks)
        return str(user_input or '').strip()

    def _detect_focus(self) -> str:
        scores = _score_rules(self.lower, FOCUS_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'Picking / Packing'

    def _detect_signals(self) -> List[str]:
        matched = [name for name, keywords in SIGNAL_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return matched or ['Queue / Congestion', 'Travel Time Waste', 'Labor Imbalance']

    def _detect_constraints(self) -> List[str]:
        matched = [name for name, keywords in CONSTRAINT_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        base = matched or ['Service-level commitment', 'Headcount cap']
        if 'Service-level commitment' not in base:
            base.append('Service-level commitment')
        return base[:4]

    def _root_causes(self) -> List[str]:
        causes = [
            'The visible bottleneck may be downstream of poor replenishment timing, weak slotting, or handoff friction rather than raw labor effort alone.',
            'Throughput pain often compounds when the same people absorb queue clearing, exception handling, and normal flow work at the same time.',
            'If staging and forward-pick locations are unstable, the team pays twice through search time and rework.',
        ]
        if self.focus == 'Receiving / Dock Flow':
            causes.append('Dock congestion usually reflects arrival clustering, unload sequencing, or delayed putaway capacity, not just carrier volume.')
        elif self.focus == 'Slotting / Putaway':
            causes.append('Travel waste often points to slotting drift where demand velocity changed faster than location logic.')
        elif self.focus == 'Replenishment Control':
            causes.append('Forward-pick starvation can make otherwise healthy picking teams look slow and inconsistent.')
        return causes[:4]

    def _quick_wins(self) -> List[str]:
        return [
            'Stabilize one high-volume zone first instead of redesigning the entire building at once.',
            'Create a simple exception lane so abnormal orders stop stealing capacity from normal flow.',
            'Tighten the replenishment trigger for the fastest movers before the next heavy shift window.',
            'Use one visual control for queue status, aged backlog, and near-cutoff risk so supervisors react earlier.',
        ]

    def _pilot_plan(self) -> List[str]:
        return [
            'Week 1: baseline one zone or process with a small set of comparable shift metrics.',
            'Week 2: trial one slotting, replenishment, or labor-balance change without adding multiple new variables.',
            'Week 3: compare throughput, errors, backlog age, and cutoff hit rate against the baseline.',
            'Week 4: expand only if the pilot improved both speed and operational stability, not just short bursts of output.',
        ]

    def _assumptions(self) -> List[str]:
        notes = [
            'This brief is heuristic and depends on the quality of the user-supplied KPI and process notes.',
            'No live WMS, OMS, labor, or automation telemetry was accessed.',
            'Bottlenecks are inferred from described symptoms and should be confirmed with floor observation or measurement.',
        ]
        if 'Inventory Accuracy / Replenishment' not in self.signals:
            notes.append('Replenishment detail appears limited, so some root-cause attribution may be incomplete.')
        return notes

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Warehouse Flow Optimizer Brief')
        lines.append('')
        lines.append(f'**Primary focus:** {self.focus}')
        lines.append(f'**Flow signals referenced:** {_join_list(self.signals)}')
        lines.append(f'**Operating constraints:** {_join_list(self.constraints)}')
        lines.append('**Method note:** This is a heuristic warehouse optimization brief. No live WMS, labor, or automation data was accessed.')
        lines.append('')
        lines.append('## Flow Summary')
        lines.append('- Start with the narrowest bottleneck that most strongly affects throughput or service risk.')
        lines.append('- Separate structural flow waste from temporary peak pressure or one-off disruptions.')
        lines.append('- Prefer local pilots that are measurable and reversible before scaling changes across the building.')
        lines.append('')
        lines.append('## Root-Cause Hypotheses')
        for bullet in self._root_causes():
            lines.append(f'- {bullet}')
        lines.append('')
        lines.append('## Quick Wins')
        for idx, item in enumerate(self._quick_wins(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## 30-Day Pilot Plan')
        for idx, item in enumerate(self._pilot_plan(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## Guardrails and Monitoring')
        for constraint in self.constraints:
            lines.append(f'- {constraint}: check that any improvement move respects this operational boundary.')
        lines.append('')
        lines.append('## Assumptions and Limits')
        for note in self._assumptions():
            lines.append(f'- {note}')
        return '\n'.join(lines)


def handle(user_input: ActionInput) -> str:
    return WarehouseFlowOptimizer(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
