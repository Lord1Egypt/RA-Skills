#!/usr/bin/env python3
import json
import os
import re
import sys
from typing import Any, Dict, List


def _load_skill_meta(slug):
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    meta = re.search(r'^---$(.*?)^---$', content, re.DOTALL | re.MULTILINE)
    return meta.group(1).strip() if meta else ''


def _normalize_inputs(inputs: Any) -> str:
    if inputs is None:
        return ''
    if isinstance(inputs, str):
        return inputs.strip()
    try:
        return json.dumps(inputs, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(inputs)


DIMENSION_KEYWORDS = {
    'Work': ['work', 'project', 'client', 'meeting', 'deadline', 'task', 'email', 'draft', 'study', 'school'],
    'Health': ['sleep', 'walk', 'workout', 'exercise', 'meal', 'food', 'water', 'rest', 'run', 'tired', 'energy'],
    'Relationships': ['family', 'friend', 'partner', 'child', 'kids', 'parent', 'call', 'conversation', 'date'],
    'Growth': ['read', 'book', 'learn', 'learning', 'course', 'journal', 'reflect', 'practice', 'skill'],
}

POSITIVE_WORDS = ['good', 'great', 'win', 'finished', 'progress', 'proud', 'steady', 'strong', 'connected', 'consistent', 'better']
NEGATIVE_WORDS = ['hard', 'late', 'stuck', 'avoid', 'avoided', 'missed', 'tired', 'poor', 'friction', 'stress', 'overwhelmed']

DEFAULT_WINS = {
    'Work': 'Name one concrete thing that moved, even if the week felt messy.',
    'Health': 'Name one behavior that supported your body, even briefly.',
    'Relationships': 'Name one moment of contact, care, or patience.',
    'Growth': 'Name one thing you learned, noticed, or practiced.',
}

DEFAULT_FRICTIONS = {
    'Work': 'Notice one unfinished loop or recurring distraction.',
    'Health': 'Notice one pattern around sleep, food, movement, or energy that made the week harder.',
    'Relationships': 'Notice one relationship that got less attention than it needed.',
    'Growth': 'Notice where learning or reflection got crowded out.',
}

DEFAULT_EVIDENCE = {
    'Work': 'No work note was provided, so pull one concrete example from memory.',
    'Health': 'No health note was provided, so pull one real body or energy example from memory.',
    'Relationships': 'No relationship note was provided, so pull one interaction from memory.',
    'Growth': 'No growth note was provided, so pull one reading, learning, or reflection example from memory.',
}


class WeeklyReflector:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.snippets = self._split_snippets()
        self.dimensions = self._build_dimensions()
        self.pattern = self._detect_pattern()
        self.theme = self._detect_theme()
        self.overall_feeling = self._overall_feeling()
        self.adjustments = self._build_adjustments()

    def _split_snippets(self) -> List[str]:
        parts = re.split(r'[\n.;!?]+', self.raw)
        return [part.strip(' -•') for part in parts if part.strip(' -•')]

    def _matched_snippets(self, dimension: str) -> List[str]:
        keywords = DIMENSION_KEYWORDS[dimension]
        matched = [snippet for snippet in self.snippets if any(keyword in snippet.lower() for keyword in keywords)]
        return matched

    def _positive_snippets(self, snippets: List[str]) -> List[str]:
        return [snippet for snippet in snippets if any(word in snippet.lower() for word in POSITIVE_WORDS)]

    def _negative_snippets(self, snippets: List[str]) -> List[str]:
        return [snippet for snippet in snippets if any(word in snippet.lower() for word in NEGATIVE_WORDS)]

    def _build_dimensions(self) -> Dict[str, Dict[str, str]]:
        result: Dict[str, Dict[str, str]] = {}
        for dimension in DIMENSION_KEYWORDS:
            matched = self._matched_snippets(dimension)
            positives = self._positive_snippets(matched)
            negatives = self._negative_snippets(matched)
            if positives and not negatives:
                status = 'strong'
            elif negatives and not positives:
                status = 'needs attention'
            elif matched:
                status = 'mixed'
            else:
                status = 'mixed'
            wins = '; '.join(positives[:2]) if positives else DEFAULT_WINS[dimension]
            friction = '; '.join(negatives[:2]) if negatives else DEFAULT_FRICTIONS[dimension]
            evidence = '; '.join(matched[:3]) if matched else DEFAULT_EVIDENCE[dimension]
            result[dimension] = {
                'status': status,
                'wins': wins,
                'friction': friction,
                'evidence': evidence,
            }
        return result

    def _detect_pattern(self) -> str:
        if any(word in self.lower for word in ['sleep', 'slept poorly', 'late night', 'tired', 'exhausted']):
            return 'Sleep and recovery shaped multiple areas of the week more than willpower alone.'
        if any(word in self.lower for word in ['avoid', 'avoided', 'procrast', 'stuck', 'delay']):
            return 'Avoidance and delayed starts created drag across more than one area.'
        strong_count = sum(1 for info in self.dimensions.values() if info['status'] == 'strong')
        if strong_count >= 3 or any(word in self.lower for word in ['consistent', 'routine', 'showed up', 'kept going']):
            return 'Small consistency created momentum across the week.'
        if self.dimensions['Relationships']['status'] == 'needs attention':
            return 'Relationships needed more intentional space instead of being squeezed between tasks.'
        return 'The week looked mixed, so one stabilizing adjustment will likely help more than a full reset.'

    def _detect_theme(self) -> str:
        if self.pattern.startswith('Sleep'):
            return 'Recovery'
        if self.pattern.startswith('Small consistency'):
            return 'Momentum'
        if self.pattern.startswith('Avoidance'):
            return 'Re-entry'
        return 'Rebalance'

    def _overall_feeling(self) -> str:
        positives = sum(1 for snippet in self.snippets if any(word in snippet.lower() for word in POSITIVE_WORDS))
        negatives = sum(1 for snippet in self.snippets if any(word in snippet.lower() for word in NEGATIVE_WORDS))
        if positives > negatives:
            return 'Mostly positive, with usable momentum.'
        if negatives > positives:
            return 'Tired or stretched, but still informative.'
        return 'Mixed, honest, and still useful.'

    def _build_adjustments(self) -> Dict[str, str]:
        if self.pattern.startswith('Sleep'):
            return {
                'stop': 'Stop borrowing from sleep to rescue the next day.',
                'start': 'Start one earlier shutdown cue on the two most demanding nights.',
                'continue': 'Continue the smallest health behavior that already helped, even if it was brief.',
                'experiment': 'Try a two-night wind-down experiment and note whether work focus and patience improve.',
            }
        if self.pattern.startswith('Avoidance'):
            return {
                'stop': 'Stop carrying vague open loops in your head.',
                'start': 'Start the day with one 15 minute entry task on the hardest item.',
                'continue': 'Continue anything that made starting easier, even if the block was short.',
                'experiment': 'Test a visible first-task card for three days and see if resistance drops.',
            }
        if self.pattern.startswith('Small consistency'):
            return {
                'stop': 'Stop overloading next week with too many new goals.',
                'start': 'Start protecting the routines that already produced momentum.',
                'continue': 'Continue the habits and environments that made follow-through easier.',
                'experiment': 'Repeat your strongest block from this week on purpose once more next week.',
            }
        return {
            'stop': 'Stop keeping the weekly review only in your head.',
            'start': 'Start a 10 minute weekly evidence capture before judging the week.',
            'continue': 'Continue one supportive behavior that already feels realistic.',
            'experiment': 'Run one small change in the area with the most friction and review it next week.',
        }

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Weekly Reflection')
        lines.append('')
        lines.append('## Snapshot')
        lines.append(f'- Week theme: {self.theme}')
        lines.append(f'- Overall feeling: {self.overall_feeling}')
        lines.append('')
        lines.append('## Four-Dimension Review')
        for dimension in ['Work', 'Health', 'Relationships', 'Growth']:
            info = self.dimensions[dimension]
            lines.append(f'### {dimension}')
            lines.append(f"- Status: {info['status']}")
            lines.append(f"- Wins: {info['wins']}")
            lines.append(f"- Friction: {info['friction']}")
            lines.append(f"- Evidence: {info['evidence']}")
            lines.append('')
        lines.append('## Pattern Noticed')
        lines.append(f'- {self.pattern}')
        lines.append('')
        lines.append('## Next Week Adjustments')
        lines.append(f"- Stop: {self.adjustments['stop']}")
        lines.append(f"- Start: {self.adjustments['start']}")
        lines.append(f"- Continue: {self.adjustments['continue']}")
        lines.append(f"- One experiment: {self.adjustments['experiment']}")
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('weekly-reflectron')
    reflector = WeeklyReflector(inputs)
    return reflector.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
