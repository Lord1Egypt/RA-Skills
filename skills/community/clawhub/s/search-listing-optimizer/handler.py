#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

PLATFORM_RULES = {
    'Amazon': ['amazon', 'a9', 'seller central', 'asin'],
    'Taobao / 1688': ['taobao', '1688'],
    'JD': ['jd', 'jingdong'],
    'TikTok Shop': ['tiktok', 'tik tok'],
    'Xiaohongshu': ['xiaohongshu', 'rednote', 'xhs'],
    'Shopify': ['shopify', 'storefront'],
    'General': ['general', 'multi', 'all platform'],
}

ATTRIBUTE_WEIGHT = {
    'Title': {'amazon': 25, 'taobao': 20, 'jd': 20, 'tiktok': 15, 'xiaohongshu': 10, 'shopify': 20, 'general': 15},
    'Bullets / Key Features': {'amazon': 25, 'taobao': 20, 'jd': 15, 'tiktok': 15, 'xiaohongshu': 15, 'shopify': 20, 'general': 15},
    'Description / Body': {'amazon': 15, 'taobao': 20, 'jd': 20, 'tiktok': 20, 'xiaohongshu': 20, 'shopify': 20, 'general': 20},
    'Backend Keywords': {'amazon': 20, 'taobao': 15, 'jd': 15, 'tiktok': 10, 'xiaohongshu': 5, 'shopify': 10, 'general': 10},
    'Images': {'amazon': 10, 'taobao': 15, 'jd': 15, 'tiktok': 20, 'xiaohongshu': 25, 'shopify': 15, 'general': 20},
    'Reviews / Rating': {'amazon': 5, 'taobao': 5, 'jd': 10, 'tiktok': 15, 'xiaohongshu': 20, 'shopify': 15, 'general': 10},
    'Price': {'amazon': 0, 'taobao': 5, 'jd': 5, 'tiktok': 5, 'xiaohongshu': 5, 'shopify': 5, 'general': 5},
}

CONVERSION_TRAPS = {
    'Pricing': ['price too high', 'price mismatch', 'not competitive', 'expensive'],
    'Images': ['no main image', 'blurry', 'no lifestyle', 'no infographic', 'missing alt text'],
    'Reviews': ['no reviews', 'low rating', 'negative reviews', 'review count low'],
    'Description': ['vague', 'missing spec', 'no benefit', 'hard to read', 'no proof points'],
    'Trust Signals': ['no guarantee', 'no return policy visible', 'no FAQ', 'no brand story'],
}

ListingInput = Union[str, Dict[str, Any]]


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for kw in kws if kw in text) for name, kws in rules.items()}


def _join(items: List[str]) -> str:
    return ', '.join(items) if items else 'Not specified'


class SearchListingOptimizer:
    def __init__(self, user_input: ListingInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.platform = self._detect_platform()
        self.goal = self._detect_goal()
        self.traps = self._detect_traps()
        self.attributes = self._attribute_order()

    def _normalize_input(self, user_input: ListingInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['platform', 'product', 'listing', 'goal', 'notes']:
                value = user_input.get(key)
                if not value:
                    continue
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value)
                chunks.append(f'{key}: {value}')
            return ' | '.join(chunks)
        return str(user_input or '').strip()

    def _detect_platform(self) -> str:
        scores = _score_rules(self.lower, PLATFORM_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'Amazon'

    def _detect_goal(self) -> str:
        if any(kw in self.lower for kw in ['new', 'launch', 'first', 'create', 'build']):
            return 'New Listing'
        if any(kw in self.lower for kw in ['convert', 'conversion', 'sales', 'order']):
            return 'Conversion Improvement'
        return 'Visibility Boost'

    def _detect_traps(self) -> List[str]:
        matched = [name for name, kws in CONVERSION_TRAPS.items() if any(kw in self.lower for kw in kws)]
        defaults = ['Pricing', 'Description', 'Trust Signals']
        return list(dict.fromkeys(matched + [d for d in defaults if d not in matched]))[:4]

    def _attribute_order(self) -> List[str]:
        return list(ATTRIBUTE_WEIGHT.keys())

    def _scorecard_rows(self) -> List[Dict[str, str]]:
        p = self.platform
        rows = []
        for attr in self.attributes:
            weight = ATTRIBUTE_WEIGHT.get(attr, {}).get(p, ATTRIBUTE_WEIGHT.get(attr, {}).get('general', 10))
            guidance = {
                'Title': 'Front-load primary keyword; include brand, model, key benefit, and count/pack.',
                'Bullets / Key Features': 'Lead bullet 1 with the biggest benefit; use remaining bullets for specs, use case, and social proof.',
                'Description / Body': 'Open with the core benefit in one sentence; use the rest for proof points, scenarios, and trust.',
                'Backend Keywords': 'Fill all available character slots; avoid duplicates with title or bullets.',
                'Images': 'Main image on pure white background; add infographic, lifestyle, and comparison chart.',
                'Reviews': 'Prioritize review velocity over star rating; address negative review themes proactively.',
                'Price': 'Research the 3rd-party price comparison; price within 10% of the competitive range.',
            }
            rows.append({'attribute': attr, 'weight': f'{weight}%', 'guidance': guidance.get(attr, 'Optimize per platform guidelines.')})
        return rows

    def _keyword_angles(self) -> List[str]:
        return [
            'Identify the primary search intent: is it informational, navigational, or transactional?',
            'Target the top 3 competitor ASIN titles for structural inspiration without copying.',
            'Distribute primary keywords across Title, Bullet 1, and the first line of Description.',
            'Use backend search terms for secondary keywords, misspellings, and synonyms.',
        ]

    def _action_list(self) -> List[str]:
        actions = [
            'Rewrite the title with the primary keyword first, followed by a benefit and a spec.',
            'Audit bullets: each bullet should independently convey a compelling reason to buy.',
            'Add or refresh the main image; ensure it passes the platform main-image standard.',
            'Build the description with a benefit-led opening, proof points, and a clear CTA.',
            'Populate all backend search term fields with relevant secondary keywords and variants.',
        ]
        if self.goal == 'New Listing':
            actions.insert(0, 'Start with competitor research: find the top 3 ASINs and map their keyword structure.')
        if self.goal == 'Conversion Improvement':
            actions.insert(0, 'Run a conversion-trap audit: check pricing, trust signals, and review depth first.')
        return actions[:6]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Search Listing Optimization Brief')
        lines.append('')
        lines.append(f'**Platform:** {self.platform}')
        lines.append(f'**Optimization goal:** {self.goal}')
        lines.append(f'**Conversion traps detected:** {_join(self.traps)}')
        lines.append('**Method note:** This is a heuristic optimization brief. No live search analytics or platform API was accessed.')
        lines.append('')
        lines.append('## Platform Search Context')
        platform_notes = {
            'Amazon': 'A9 ranks by conversion rate,相关性, and customer satisfaction. Price and reviews also factor.',
            'Taobao / 1688': 'Relevance + sales history + DSR. Titles should match buyer search phrasing.',
            'JD': 'Similar to Amazon; logistics score (京东物流) also influences ranking.',
            'TikTok Shop': 'Discovery is feed-driven; tags, titles, and engagement signals drive visibility.',
            'Xiaohongshu': 'Keyword relevance + engagement + creator seeding;笔记 copy is critical.',
            'Shopify': 'Search is storefront-driven; product metafields and tags influence search relevance.',
        }
        lines.append(f'- {platform_notes.get(self.platform, "Review platform-specific ranking factors before finalizing optimization.")}')
        lines.append('')
        lines.append('## Listing Attribute Scorecard')
        lines.append('| Attribute | Est. Weight | Optimization Guidance |')
        lines.append('|---|---|---|')
        for row in self._scorecard_rows():
            lines.append(f'| {row["attribute"]} | {row["weight"]} | {row["guidance"]} |')
        lines.append('')
        lines.append('## Keyword Strategy Angles')
        for item in self._keyword_angles():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Conversion Trap Detection')
        trap_notes = {
            'Pricing': 'Compare against top 3 competitors and the platform median; price within 10–15% if possible.',
            'Images': 'Require a compliant main image, at least 4 supplemental images, and 1 infographic.',
            'Reviews': 'Aim for 10+ reviews with a 4.0+ average before expecting meaningful traffic.',
            'Description': 'Lead with benefits, support with specs, and end with a low-friction CTA.',
            'Trust Signals': 'Display return policy, warranty terms, and brand credibility above the fold.',
        }
        for trap in self.traps:
            lines.append(f'### {trap}')
            lines.append(f'- {trap_notes.get(trap, "Audit this area and address specific weaknesses.")}')
        lines.append('')
        lines.append('## Prioritized Action List')
        for idx, action in enumerate(self._action_list(), 1):
            lines.append(f'{idx}. {action}')
        lines.append('')
        lines.append('## Revised Title Template')
        title_templates = {
            'Amazon': '[Brand] [Product Name] [Key Feature 1] [Key Feature 2] [Count/Pack] — [Primary Benefit]',
            'Taobao / 1688': '[品牌] [产品名称] [规格/型号] [核心卖点] [件数/套餐]',
            'JD': '[品牌] [商品名称] [型号] [核心卖点] [件数]',
            'TikTok Shop': '[Product Name] | [Key Benefit] | [Trending Keyword] #[Hashtag1] #[Hashtag2]',
            'Xiaohongshu': '[产品名]测评 | [核心功效] | [适合人群] #[关键词1] #[关键词2]',
            'Shopify': '[Product Name] — [Short Benefit Description] | [Brand]',
        }
        lines.append(f'```\n{title_templates.get(self.platform, "[Brand] [Product Name] [Key Feature] [Count]")}\n```')
        return '\n'.join(lines)


def handle(user_input: ListingInput) -> str:
    return SearchListingOptimizer(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
