#!/usr/bin/env python3
import re
import sys
from typing import Dict, List, Optional

CATEGORY_KEYWORDS = {
    'beauty': ['beauty', 'skincare', 'makeup', 'cosmetic', 'self-care', 'self care'],
    'snack': ['snack', 'food', 'tea', 'coffee', 'treat', 'drink'],
    'pet': ['pet', 'dog', 'cat', 'puppy', 'kitten'],
    'book': ['book', 'reading', 'novel', 'fiction', 'nonfiction'],
    'wellness': ['wellness', 'fitness', 'mindfulness', 'supplement', 'recovery'],
    'hobby': ['hobby', 'craft', 'kit', 'diy', 'creative'],
}

DEFAULT_BUDGET = {
    'beauty': 28,
    'snack': 22,
    'pet': 26,
    'book': 24,
    'wellness': 30,
    'hobby': 32,
}

THEME_LIBRARY = {
    'beauty': [
        {
            'name': 'Reset Ritual',
            'angle': 'Blend one hero treatment with easy-repeat staples for a calm self-care story.',
            'structure': ['hero treatment', 'routine staple', 'surprise comfort extra'],
            'replenishment': 'Watch any fast-moving serum, cleanser, or mask with less than 6 weeks of cover.',
        },
        {
            'name': 'Desk-to-Dinner Glow',
            'angle': 'Position the box around quick routine upgrades for busy weekdays.',
            'structure': ['prep item', 'on-the-go enhancer', 'sensory delight'],
            'replenishment': 'Keep compact SKUs and leak-prone items in buffer stock for packing reliability.',
        },
        {
            'name': 'Seasonal Calm Kit',
            'angle': 'Use a seasonal ritual narrative to create freshness without changing every core SKU.',
            'structure': ['seasonal hero', 'habit anchor', 'theme accessory'],
            'replenishment': 'Reserve flexible accessory substitutions in case seasonal packaging slips.',
        },
    ],
    'snack': [
        {
            'name': 'Better Break Box',
            'angle': 'Mix familiar comfort with one discovery flavor to keep repeat boxes exciting.',
            'structure': ['anchor snack', 'functional treat', 'surprise flavor'],
            'replenishment': 'Track shelf-life windows and avoid overcommitting to novelty SKUs with low repeatability.',
        },
        {
            'name': 'Workday Energy Drop',
            'angle': 'Support midday productivity with portion-controlled, portable items.',
            'structure': ['focus snack', 'hydration companion', 'reward bite'],
            'replenishment': 'Secure replacements for fragile or melt-sensitive items before peak heat periods.',
        },
        {
            'name': 'Seasonal Discovery Flight',
            'angle': 'Rotate regional or limited flavors while preserving one recognizable favorite.',
            'structure': ['seasonal headline item', 'safe favorite', 'conversation starter'],
            'replenishment': 'Build alternates for imported or seasonal SKUs that may sell out early.',
        },
    ],
    'pet': [
        {
            'name': 'Play + Treat + Care',
            'angle': 'Balance fun, reward, and wellness so the box feels complete instead of random.',
            'structure': ['play item', 'treat item', 'care item'],
            'replenishment': 'Monitor treat inventory and size-variant coverage to avoid last-minute substitutions.',
        },
        {
            'name': 'Enrichment Refresh',
            'angle': 'Use rotating enrichment themes to fight subscription fatigue.',
            'structure': ['challenge toy', 'reward snack', 'owner convenience extra'],
            'replenishment': 'Keep a substitution list for oversized toys or region-restricted treat ingredients.',
        },
        {
            'name': 'Seasonal Bonding Box',
            'angle': 'Center the box on owner-pet rituals that create emotional retention value.',
            'structure': ['shared activity item', 'comfort item', 'photo-worthy bonus'],
            'replenishment': 'Protect packaging timelines for photo-led seasonal extras and soft goods.',
        },
    ],
    'book': [
        {
            'name': 'Anchor Read + Companion Gift',
            'angle': 'Pair one clear reading promise with a small companion item that amplifies the theme.',
            'structure': ['headline title', 'theme companion', 'community prompt'],
            'replenishment': 'Confirm title availability and keep one approved alternate title in the same mood lane.',
        },
        {
            'name': 'Genre Journey Box',
            'angle': 'Rotate genre-led curation while preserving a familiar community experience.',
            'structure': ['genre lead title', 'immersion accessory', 'discussion insert'],
            'replenishment': 'Protect against publisher delays and keep printable inserts flexible.',
        },
        {
            'name': 'Quarterly Reflection Edition',
            'angle': 'Use slower seasonal rhythms to justify a premium-feeling box with reflection tools.',
            'structure': ['main read', 'annotation tool', 'ritual extra'],
            'replenishment': 'Leave room to swap stationery or gift extras if print or import lead times drift.',
        },
    ],
    'wellness': [
        {
            'name': 'Reset and Recover',
            'angle': 'Lead with low-friction habits that feel useful from day one.',
            'structure': ['habit anchor', 'recovery helper', 'motivation nudge'],
            'replenishment': 'Backstop any consumable or compliance-sensitive item with a non-consumable alternative.',
        },
        {
            'name': 'Morning Momentum',
            'angle': 'Frame the box around routine consistency and easy wins.',
            'structure': ['daily starter', 'supporting tool', 'surprise delight'],
            'replenishment': 'Keep a fallback for glass, liquid, or temperature-sensitive items.',
        },
        {
            'name': 'Seasonal Reset Circuit',
            'angle': 'Refresh the subscription through seasonal behavior cues rather than SKU chaos.',
            'structure': ['seasonal focus item', 'core staple', 'reflection prompt'],
            'replenishment': 'Limit bespoke inserts that are hard to reprint late in the cycle.',
        },
    ],
    'hobby': [
        {
            'name': 'Starter Win Kit',
            'angle': 'Make the box feel achievable, rewarding, and easy to begin immediately.',
            'structure': ['headline project item', 'support tool', 'bonus extra'],
            'replenishment': 'Protect specialty components and keep one simpler substitute for scarce parts.',
        },
        {
            'name': 'Skill-Building Series',
            'angle': 'Sequence the box so each month advances one visible capability.',
            'structure': ['core project piece', 'practice aid', 'showcase add-on'],
            'replenishment': 'Avoid single-source materials without backup options.',
        },
        {
            'name': 'Seasonal Inspiration Drop',
            'angle': 'Use calendar themes to create freshness while preserving a repeatable assembly process.',
            'structure': ['seasonal craft lead', 'color or texture set', 'shareable bonus'],
            'replenishment': 'Reserve swappable colorways or motifs if a seasonal design asset slips.',
        },
    ],
}

ADD_ONS = {
    'beauty': ['mini refill add-on', 'premium tool upgrade', 'giftable duo pack'],
    'snack': ['office share pack', 'limited-edition flavor booster', 'sampler refill'],
    'pet': ['extra treat pouch', 'premium chew upgrade', 'birthday add-on'],
    'book': ['annotator bundle', 'premium bookmark set', 'author note insert'],
    'wellness': ['habit tracker card', 'premium recovery extra', 'refill pouch'],
    'hobby': ['advanced material pack', 'community challenge insert', 'premium finishing tool'],
}

PERSONA_RULES = {
    'students': ['student', 'campus', 'college'],
    'busy professionals': ['busy', 'professional', 'office', 'workday'],
    'premium enthusiasts': ['premium', 'luxury', 'high-end', 'enthusiast'],
    'families': ['family', 'kids', 'parent'],
    'gift buyers': ['gift', 'present', 'holiday'],
}

SEASON_RULES = {
    'spring': ['spring', 'march', 'april', 'may'],
    'summer': ['summer', 'june', 'july', 'august'],
    'autumn': ['autumn', 'fall', 'september', 'october', 'november'],
    'winter': ['winter', 'december', 'january', 'february'],
}

GOAL_RULES = {
    'retention': ['retention', 'churn', 'keep subscribers', 'renewal'],
    'margin': ['margin', 'profit', 'gross margin'],
    'launch': ['launch', 'new box', 'new subscription', 'acquisition'],
}


class SubscriptionBoxPlanner:
    def __init__(self, text: str):
        self.text = (text or '').strip()
        self.lower = self.text.lower()
        self.category = self._detect_category()
        self.budget = self._extract_budget()
        self.goal = self._detect_goal()
        self.season = self._detect_season()
        self.personas = self._detect_personas()
        self.constraints = self._detect_constraints()

    def _detect_category(self) -> str:
        scored = []
        for category, keywords in CATEGORY_KEYWORDS.items():
            hits = sum(1 for word in keywords if word in self.lower)
            scored.append((hits, category))
        best_hits, best_category = max(scored)
        return best_category if best_hits > 0 else 'wellness'

    def _extract_budget(self) -> int:
        matches = re.findall(r'\$\s?(\d{1,3})|under\s?\$?(\d{1,3})|(\d{1,3})\s?(?:usd|dollars)', self.lower)
        for match in matches:
            for part in match:
                if part:
                    return int(part)
        return DEFAULT_BUDGET[self.category]

    def _detect_goal(self) -> str:
        for goal, keywords in GOAL_RULES.items():
            if any(word in self.lower for word in keywords):
                return goal
        return 'balanced'

    def _detect_season(self) -> str:
        for season, keywords in SEASON_RULES.items():
            if any(word in self.lower for word in keywords):
                return season
        return 'always-on'

    def _detect_personas(self) -> List[str]:
        personas = [name for name, keywords in PERSONA_RULES.items() if any(word in self.lower for word in keywords)]
        return personas or ['core subscribers', 'value seekers', 'loyal fans']

    def _detect_constraints(self) -> List[str]:
        flags = []
        if any(word in self.lower for word in ['inventory', 'stock', 'restock', 'supply']):
            flags.append('Inventory depth matters for at least one key SKU.')
        if any(word in self.lower for word in ['ship', 'shipping', 'fragile', 'cold', 'liquid']):
            flags.append('Fulfillment simplicity and parcel reliability should influence the final mix.')
        if any(word in self.lower for word in ['budget', 'margin', 'cost', 'under $', 'under$']):
            flags.append('Cost discipline is an explicit decision filter.')
        if any(word in self.lower for word in ['feedback', 'review', 'complaint']):
            flags.append('Past customer feedback should shape what stays familiar versus what rotates.')
        return flags or ['Inputs were limited, so the plan uses a general subscription-box baseline.']

    def _price_band(self, landed_cost: int) -> str:
        low = round(landed_cost * 2.1)
        high = round(landed_cost * 2.6)
        return f'${low}-${high}'

    def _cost_for_concept(self, index: int) -> int:
        base = self.budget
        if self.goal == 'margin':
            return max(12, base - 3 + index)
        if self.goal == 'retention':
            return base + index
        return base - 1 + index

    def _theme_notes(self, concept: Dict[str, str], index: int) -> str:
        persona = self.personas[index % len(self.personas)]
        if self.goal == 'retention':
            emphasis = 'Keep one dependable repeatable item and one rotating surprise to reduce box fatigue.'
        elif self.goal == 'margin':
            emphasis = 'Let the hero item carry the story while support items stay operationally simple.'
        elif self.goal == 'launch':
            emphasis = 'Use a clearer headline theme so first-time subscribers instantly understand the promise.'
        else:
            emphasis = 'Balance discovery, practicality, and merchandising freshness across the mix.'
        return f'Best fit for **{persona}**. {emphasis}'

    def render(self) -> str:
        concepts = THEME_LIBRARY[self.category][:3]
        lines: List[str] = []
        lines.append('# Subscription Box Curation Plan')
        lines.append('')
        lines.append(f'**Category:** {self.category.title()}')
        lines.append(f'**Primary objective:** {self.goal}')
        lines.append(f'**Seasonal context:** {self.season}')
        lines.append(f'**Budget anchor:** ${self.budget} landed-cost target')
        lines.append('**Method note:** This plan is heuristic and template-based. No live catalog, inventory, or pricing API was used.')
        lines.append('')
        lines.append('## Input Snapshot')
        lines.append(f'- Suggested audience lanes: {", ".join(self.personas[:3])}')
        for flag in self.constraints:
            lines.append(f'- Constraint signal: {flag}')
        lines.append('')
        lines.append('## Recommended Box Concepts')
        for idx, concept in enumerate(concepts, 1):
            landed_cost = self._cost_for_concept(idx)
            lines.append(f'### Concept {idx}: {concept["name"]}')
            lines.append(f'- Theme angle: {concept["angle"]}')
            lines.append(f'- Suggested item architecture: {", ".join(concept["structure"])}')
            lines.append(f'- Indicative landed cost: ~${landed_cost}')
            lines.append(f'- Indicative sell-price band: {self._price_band(landed_cost)}')
            lines.append(f'- Why it works: {self._theme_notes(concept, idx - 1)}')
            lines.append(f'- Add-on idea: {ADD_ONS[self.category][(idx - 1) % len(ADD_ONS[self.category])]}')
            lines.append(f'- Replenishment watchout: {concept["replenishment"]}')
            lines.append('')
        lines.append('## Merchandising Matrix')
        lines.append('| Concept | Novelty level | Margin discipline | Fulfillment ease | Retention value |')
        lines.append('|---|---|---|---|---|')
        for idx, concept in enumerate(concepts, 1):
            novelty = 'High' if idx == 2 else 'Medium'
            margin = 'High' if self.goal == 'margin' and idx == 1 else 'Medium'
            fulfillment = 'High' if idx != 2 else 'Medium'
            retention = 'High' if self.goal == 'retention' or idx == 1 else 'Medium'
            lines.append(f'| {concept["name"]} | {novelty} | {margin} | {fulfillment} | {retention} |')
        lines.append('')
        lines.append('## Risks and Assumptions')
        lines.append('- Theme quality improves if the user later provides SKU margin, inventory cover, and subscriber feedback by segment.')
        lines.append('- Pricing guidance is directional and should be reconciled with shipping, packaging, and discount rules.')
        lines.append('- Final assortment choices should be checked against procurement timing and substitution tolerance.')
        lines.append('')
        lines.append('## Next Moves')
        lines.append('1. Pick one concept as the control box and one as the challenger concept.')
        lines.append('2. Map real SKUs into the hero / staple / surprise architecture.')
        lines.append('3. Validate landed cost, pack-out complexity, and replenishment coverage before launch lock.')
        return '\n'.join(lines)


def handle(user_input: str) -> str:
    return SubscriptionBoxPlanner(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
