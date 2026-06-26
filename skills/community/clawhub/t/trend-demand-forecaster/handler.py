#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

ActionInput = Union[str, Dict[str, Any]]

MODE_RULES = {
    'Promo Lift Planning': ['promo', 'promotion', 'campaign', 'holiday', 'launch', 'event', 'sale'],
    'Replenishment Planning': ['inventory', 'replenish', 'stock', 'buy', 'inbound', 'purchase order', 'coverage'],
    'Recovery / Slowdown Read': ['recover', 'recovery', 'rebound', 'drop', 'decline', 'slowdown', 'softness'],
    'Baseline Forecast': ['forecast', 'baseline', 'plan', 'next month', 'next quarter', 'demand'],
}

SIGNAL_RULES = {
    'Traffic / Order Volume': ['traffic', 'sessions', 'orders', 'volume', 'demand', 'gmv', 'sales'],
    'Conversion / Funnel': ['conversion', 'cvr', 'checkout', 'cart', 'funnel'],
    'Price / Promotion': ['price', 'pricing', 'discount', 'promo', 'coupon', 'markdown'],
    'Inventory / Availability': ['inventory', 'stock', 'stockout', 'oos', 'coverage', 'inbound'],
    'Returns / Service': ['return', 'refund', 'rating', 'review', 'service', 'complaint'],
    'External Trend Context': ['seasonal', 'holiday', 'trend', 'weather', 'competitor', 'market'],
}

RISK_RULES = {
    'Promo distortion': ['promo', 'discount', 'campaign', 'sale'],
    'Stockout distortion': ['stockout', 'oos', 'out of stock', 'inventory'],
    'Seasonality shift': ['seasonal', 'holiday', 'weather'],
    'Assortment change': ['launch', 'new sku', 'new product', 'bundle', 'assortment'],
    'Weak data quality': ['rough notes', 'estimate', 'limited data', 'partial'],
}


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for keyword in keywords if keyword in text) for name, keywords in rules.items()}


def _join_list(items: List[str]) -> str:
    return ', '.join(items) if items else 'None explicitly provided'


class TrendDemandForecaster:
    def __init__(self, user_input: ActionInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.mode = self._detect_mode()
        self.horizon = self._detect_horizon()
        self.signals = self._detect_signals()
        self.risks = self._detect_risks()

    def _normalize_input(self, user_input: ActionInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['objective', 'horizon', 'signals', 'constraints', 'notes']:
                value = user_input.get(key)
                if not value:
                    continue
                if isinstance(value, list):
                    value = ', '.join(str(item) for item in value)
                chunks.append(f'{key}: {value}')
            return ' | '.join(chunks)
        return str(user_input or '').strip()

    def _detect_mode(self) -> str:
        scores = _score_rules(self.lower, MODE_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'Baseline Forecast'

    def _detect_horizon(self) -> str:
        if any(keyword in self.lower for keyword in ['quarter', 'q1', 'q2', 'q3', 'q4']):
            return 'Next quarter'
        if any(keyword in self.lower for keyword in ['holiday', 'seasonal', 'summer', 'winter', 'festival']):
            return 'Seasonal window'
        if any(keyword in self.lower for keyword in ['week', '4 week', '8 week', 'month']):
            return 'Next 4 to 8 weeks'
        return 'Next 4 to 8 weeks'

    def _detect_signals(self) -> List[str]:
        matched = [name for name, keywords in SIGNAL_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return matched or ['Traffic / Order Volume', 'Conversion / Funnel', 'Inventory / Availability']

    def _detect_risks(self) -> List[str]:
        matched = [name for name, keywords in RISK_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        if not matched:
            matched = ['Weak data quality']
        if 'Weak data quality' not in matched:
            matched.append('Weak data quality')
        return matched[:4]

    def _scenario_rows(self) -> List[Dict[str, str]]:
        if self.mode == 'Promo Lift Planning':
            return [
                {'scenario': 'Base', 'implication': 'Promo creates a temporary lift, then demand normalizes toward the recent underlying run rate.', 'cue': 'Buy enough to protect hero SKUs, but avoid assuming the full event lift persists.'},
                {'scenario': 'Upside', 'implication': 'Campaign resonance and clean inventory availability sustain higher-than-expected sell-through.', 'cue': 'Prepare a fast reorder or transfer path for top products instead of broad overbuying.'},
                {'scenario': 'Downside', 'implication': 'Lift is shallow or highly discount-dependent, so demand falls back quickly after the event.', 'cue': 'Keep markdown exposure and tail inventory tightly controlled.'},
            ]
        if self.mode == 'Replenishment Planning':
            return [
                {'scenario': 'Base', 'implication': 'Demand stays close to the recent steady-state trend and the current inbound plan mostly fits.', 'cue': 'Replenish core SKUs first and defer speculative tail buys.'},
                {'scenario': 'Upside', 'implication': 'Availability improves and conversion holds, creating a cleaner sell-through path than recent history suggests.', 'cue': 'Secure supplier flexibility for the top-demand families.'},
                {'scenario': 'Downside', 'implication': 'Demand softens or lead-time risk rises, leaving slower inventory exposed.', 'cue': 'Reduce open-to-buy on low-confidence or low-margin items.'},
            ]
        if self.mode == 'Recovery / Slowdown Read':
            return [
                {'scenario': 'Base', 'implication': 'Demand is stabilizing, but the recovery is still fragile and uneven by channel or SKU.', 'cue': 'Monitor leading indicators for two more cycles before making aggressive commitments.'},
                {'scenario': 'Upside', 'implication': 'Improving traffic, conversion, and service quality point to a real recovery rather than noise.', 'cue': 'Lean into the strongest channels and products with controlled inventory expansion.'},
                {'scenario': 'Downside', 'implication': 'The apparent rebound is mostly explained by promo timing, stock normalization, or one-off factors.', 'cue': 'Preserve cash and resist extrapolating a short-term bounce.'},
            ]
        return [
            {'scenario': 'Base', 'implication': 'Demand tracks the recent underlying trend after adjusting for major one-off distortions.', 'cue': 'Plan around the dependable core rather than headline spikes.'},
            {'scenario': 'Upside', 'implication': 'Traffic quality, conversion, or mix improves enough to support a stronger demand curve.', 'cue': 'Use reorder triggers, not blanket optimism, to capture the upside.'},
            {'scenario': 'Downside', 'implication': 'Soft traffic, weaker conversion, or operational friction drags demand below the current baseline.', 'cue': 'Protect margin and cash by slowing low-conviction buys.'},
        ]

    def _leading_indicators(self) -> List[str]:
        indicators = {
            'Traffic / Order Volume': 'Track weekly sessions, order count, and top-SKU daily demand pace against a recent baseline.',
            'Conversion / Funnel': 'Watch conversion rate, add-to-cart quality, and checkout completion for sign changes before revenue fully moves.',
            'Price / Promotion': 'Separate true baseline demand from discount-driven lift and measure normalization after the offer ends.',
            'Inventory / Availability': 'Check stockout hours, in-stock rate, and inbound timing so availability issues are not mistaken for weak demand.',
            'Returns / Service': 'Use return reasons, complaint spikes, and rating changes as early warning signals for demand quality erosion.',
            'External Trend Context': 'Confirm whether seasonality, holiday timing, or market trend changes are amplifying or suppressing demand.',
        }
        return [indicators[name] for name in self.signals][:4]

    def _implications(self) -> List[str]:
        actions = [
            'Protect the core demand signal first, then layer scenario-specific inventory or budget actions on top.',
            'Keep hero SKU availability cleaner than the long tail, because forecasting error matters most where demand concentrates.',
            'Use scenario triggers to decide when to accelerate, pause, or defer incremental buys.',
        ]
        if self.mode == 'Promo Lift Planning':
            actions.append('Treat event demand as a pulse unless repeat-order quality or post-event conversion proves otherwise.')
        elif self.mode == 'Replenishment Planning':
            actions.append('Bias open-to-buy toward fast, flexible replenishment rather than broad speculative depth.')
        else:
            actions.append('Document what would count as evidence of a true recovery, not just a good week.')
        return actions

    def _assumptions(self) -> List[str]:
        notes = [
            'This brief is heuristic and depends on the quality of the user-supplied history and planning notes.',
            'No live system, marketplace, ad platform, or external trend source was accessed.',
            'Scenario ranges are decision aids, not statistical confidence intervals.',
        ]
        if 'Inventory / Availability' not in self.signals:
            notes.append('Availability details were limited, so lost-demand and true-baseline separation may be weak.')
        return notes

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Trend Demand Forecast Brief')
        lines.append('')
        lines.append(f'**Primary mode:** {self.mode}')
        lines.append(f'**Planning horizon:** {self.horizon}')
        lines.append(f'**Signals referenced:** {_join_list(self.signals)}')
        lines.append(f'**Main risks:** {_join_list(self.risks)}')
        lines.append('**Method note:** This is a heuristic demand-planning brief. No live ERP, BI, ads, or marketplace data was accessed.')
        lines.append('')
        lines.append('## Demand Narrative')
        lines.append('- Start from the likely underlying trend, then adjust for promo noise, stock distortions, and seasonality.')
        lines.append('- Treat the forecast as a planning range, not a single precise number.')
        lines.append('- Focus on what would change the next buy, budget, or availability decision.')
        lines.append('')
        lines.append('## Scenario View')
        lines.append('| Scenario | What it implies | Action cue |')
        lines.append('|---|---|---|')
        for row in self._scenario_rows():
            lines.append(f'| {row["scenario"]} | {row["implication"]} | {row["cue"]} |')
        lines.append('')
        lines.append('## Leading Indicators')
        for idx, item in enumerate(self._leading_indicators(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## Inventory and Commercial Implications')
        for bullet in self._implications():
            lines.append(f'- {bullet}')
        lines.append('')
        lines.append('## Risk Watchlist')
        for risk in self.risks:
            lines.append(f'- {risk}: validate whether this is distorting the recent signal before scaling any commitment.')
        lines.append('')
        lines.append('## Assumptions and Limits')
        for note in self._assumptions():
            lines.append(f'- {note}')
        return '\n'.join(lines)


def handle(user_input: ActionInput) -> str:
    return TrendDemandForecaster(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
