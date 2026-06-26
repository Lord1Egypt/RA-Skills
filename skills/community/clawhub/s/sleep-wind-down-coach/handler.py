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


TIME_PATTERN = r'(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)'


class SleepWindDownCoach:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.desired_bedtime = self._desired_bedtime()
        self.current_pattern = self._current_pattern()
        self.ladder_minutes = self._ladder_minutes()
        self.timeline = self._timeline()
        self.environment = self._environment()
        self.fallback = self._fallback()

    def _desired_bedtime(self) -> str:
        patterns = [
            rf'(?:bed by|asleep by|bedtime\s*(?:is|:)?|target bedtime\s*(?:is|:)?|want to be asleep by)\s*{TIME_PATTERN}',
            rf'(?:go to bed by)\s*{TIME_PATTERN}',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.lower)
            if match:
                return match.group(1).strip()
        return '10:30 pm'

    def _current_pattern(self) -> str:
        patterns = [
            rf'(?:usually|currently|actual bedtime is|but usually)\s+(?:around\s+)?{TIME_PATTERN}',
            rf'(?:stay up until|scroll until|work until|awake until)\s*{TIME_PATTERN}',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.lower)
            if match:
                return f'Usually closer to {match.group(1).strip()}'
        if any(word in self.lower for word in ['late', 'drift', 'too late']):
            return 'Bedtime drifts later than intended.'
        return 'Current pattern not clearly specified.'

    def _ladder_minutes(self) -> int:
        explicit = re.search(r'\b(30|60|90)\s*(minutes|minute|min)\b', self.lower)
        if explicit:
            return int(explicit.group(1))
        if any(word in self.lower for word in ['email', 'scroll', 'screens', 'doomscroll', 'mentally on', 'work until']):
            return 60
        if any(word in self.lower for word in ['very late', 'chaotic', 'kids', 'short version']):
            return 30
        return 60

    def _boundary(self) -> str:
        boundary_label = 'T-60' if self.ladder_minutes >= 60 else 'T-30'
        if any(word in self.lower for word in ['email', 'work', 'slack', 'message']):
            return f'No work email or work chat after {boundary_label}.'
        if any(word in self.lower for word in ['scroll', 'social', 'phone', 'screens']):
            return f'No scrolling or high-stimulation screens after {boundary_label}.'
        return f'No new stimulating input after {boundary_label}.'

    def _timeline(self) -> Dict[str, str]:
        top_label = 'T-90' if self.ladder_minutes == 90 else ('T-60' if self.ladder_minutes >= 60 else 'T-30')
        top_step = 'Dim lights, close work loops, and make tomorrow capture notes short and final.'
        if self.ladder_minutes == 30:
            top_step = 'End stimulating inputs, dim lights, and start the shortest calming sequence available.'
        middle_step = 'Do hygiene, light stretching, or quiet reading instead of productivity tasks.'
        final_step = 'Put the phone away, lower sensory input, and use 3 slow breaths or one page of reading as the final bridge into bed.'
        return {
            top_label: top_step,
            'T-30': middle_step,
            'T-10': final_step,
        }

    def _environment(self) -> Dict[str, str]:
        light = 'Lights get noticeably dimmer once the wind-down starts.'
        screens = self._boundary()
        temperature = 'Cool the room slightly or remove one layer of heat if the room runs warm.'
        noise = 'Use the quietest setup available, such as a fan, earplugs, or a closed-door buffer.'
        if 'noise' in self.lower or 'kids' in self.lower or 'child' in self.lower:
            noise = 'Use a realistic noise buffer, such as a fan, earplugs, or the calmest room available.'
        return {
            'light': light,
            'screens': screens,
            'temperature': temperature,
            'noise': noise,
        }

    def _fallback(self) -> str:
        return 'If the night is already late, stop new inputs now, do the shortest wash-up possible, dim lights, take 3 slow breaths, and get into bed without trying to perfect the routine.'

    def render(self) -> str:
        top_label = next(key for key in self.timeline.keys() if key in ['T-90', 'T-60', 'T-30'])
        lines: List[str] = []
        lines.append('# Wind-Down Plan')
        lines.append('')
        lines.append('## Sleep Target')
        lines.append(f'- Desired bedtime: {self.desired_bedtime}')
        lines.append(f'- Current pattern: {self.current_pattern}')
        lines.append('')
        lines.append('## Ramp-Down Timeline')
        lines.append(f"- {top_label}: {self.timeline[top_label]}")
        lines.append(f"- T-30: {self.timeline['T-30']}")
        lines.append(f"- T-10: {self.timeline['T-10']}")
        lines.append('')
        lines.append('## Environment Checklist')
        lines.append(f"- Light: {self.environment['light']}")
        lines.append(f"- Screens: {self.environment['screens']}")
        lines.append(f"- Temperature: {self.environment['temperature']}")
        lines.append(f"- Noise: {self.environment['noise']}")
        lines.append('')
        lines.append('## Fallback Version')
        lines.append(f'- If the night is already late, I will: {self.fallback}')
        lines.append('')
        lines.append('## Morning Feedback')
        lines.append('- How fast did I settle?')
        lines.append('- How did I feel on wake-up?')
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('sleep-wind-down-coach')
    coach = SleepWindDownCoach(inputs)
    return coach.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
