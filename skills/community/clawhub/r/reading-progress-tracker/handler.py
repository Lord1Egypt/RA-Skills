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


WHY_RULES = [
    ('learning', ['learn', 'study', 'skill', 'understand', 'research']),
    ('enjoyment', ['enjoy', 'fun', 'fiction', 'novel', 'pleasure']),
    ('reference', ['reference', 'lookup', 'consult', 'manual']),
    ('parenting', ['parent', 'child', 'kid', 'family']),
]

FORMAT_RULES = [
    ('audiobook', ['audio', 'audiobook', 'listening']),
    ('ebook', ['ebook', 'kindle', 'pdf', 'epub']),
    ('print', ['print', 'paperback', 'hardcover', 'physical book']),
]


class ReadingProgressTracker:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.snippets = self._snippets()
        self.current_reads = self._current_reads()
        self.session_note = self._session_note()
        self.queue = self._queue()

    def _snippets(self) -> List[str]:
        parts = re.split(r'[\n;]+', self.raw)
        return [part.strip(' -•') for part in parts if part.strip(' -•')]

    def _extract_titles(self) -> List[str]:
        patterns = [
            r'(?:reading|read|working through|currently reading)\s+["“]?(.+?)(?=(?:\s+on\s+|\s+for\s+|,|\.|$))',
            r'(?:listening to)\s+["“]?(.+?)(?=(?:\s+on\s+|\s+for\s+|,|\.|$))',
            r'now\s*:\s*(.+?)(?=(?:\n|;|$))',
        ]
        titles: List[str] = []
        for pattern in patterns:
            for match in re.finditer(pattern, self.raw, flags=re.IGNORECASE):
                title = match.group(1).strip(' "”')
                if title and title not in titles:
                    titles.append(title)
        return titles[:3]

    def _purpose(self, snippet: str) -> str:
        lower = snippet.lower()
        for purpose, words in WHY_RULES:
            if any(word in lower for word in words):
                return purpose
        return 'learning'

    def _format(self, snippet: str) -> str:
        lower = snippet.lower()
        for format_name, words in FORMAT_RULES:
            if any(word in lower for word in words):
                return format_name
        return 'Not specified'

    def _progress(self, snippet: str) -> str:
        patterns = [
            r'(\d{1,4}\s*%)',
            r'(page\s+\d+(?:-\d+)?)',
            r'(pages\s+\d+(?:-\d+)?)',
            r'(chapter\s+\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, snippet, flags=re.IGNORECASE)
            if match:
                return match.group(1)
        return 'Not specified yet'

    def _next_stop(self, progress: str) -> str:
        match = re.search(r'page\s+(\d+)', progress, flags=re.IGNORECASE)
        if match:
            page = int(match.group(1))
            return f'Page {page + 15}'
        match = re.search(r'pages\s+(\d+)-(\d+)', progress, flags=re.IGNORECASE)
        if match:
            page = int(match.group(2))
            return f'Page {page + 10}'
        match = re.search(r'chapter\s+(\d+)', progress, flags=re.IGNORECASE)
        if match:
            chapter = int(match.group(1))
            return f'End of chapter {chapter + 1}'
        match = re.search(r'(\d{1,3})\s*%', progress)
        if match:
            pct = int(match.group(1))
            return f'{min(pct + 10, 100)}%'
        return 'Choose a small stopping point before the next context switch.'

    def _snippet_for_title(self, title: str) -> str:
        for snippet in self.snippets:
            if title.lower() in snippet.lower():
                return snippet
        return self.raw

    def _current_reads(self) -> List[Dict[str, str]]:
        titles = self._extract_titles()
        if not titles:
            titles = ['Current book not named']
        books: List[Dict[str, str]] = []
        for title in titles:
            snippet = self._snippet_for_title(title)
            progress = self._progress(snippet)
            books.append({
                'title': title,
                'why': self._purpose(snippet),
                'format': self._format(snippet),
                'progress': progress,
                'next_stop': self._next_stop(progress),
            })
        return books

    def _find_field(self, label: str, default: str) -> str:
        match = re.search(rf'{label}\s*[:\-]\s*(.+?)(?:\n|;|$)', self.raw, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return default

    def _session_note(self) -> Dict[str, str]:
        date_match = re.search(r'(20\d{2}-\d{2}-\d{2}|today|yesterday)', self.lower)
        date_value = date_match.group(1) if date_match else 'Today'
        progress = self.current_reads[0]['progress'] if self.current_reads else 'Not specified'
        return {
            'date': date_value.capitalize() if isinstance(date_value, str) else 'Today',
            'pages_or_chapter': progress,
            'idea': self._find_field('idea', 'One idea worth keeping from this session.'),
            'quote': self._find_field('quote', 'Capture one line, scene, or example that stayed with you.'),
            'question': self._find_field('question', 'What do I want to notice or test in the next reading session?'),
        }

    def _queue(self) -> Dict[str, str]:
        next_item = self._find_field('next', 'Choose one book that feels timely and genuinely readable next.')
        later_item = self._find_field('later', 'Everything interesting but not urgent belongs here.')
        drop_item = self._find_field('drop', 'Any book that feels like obligation only can be paused or dropped.')
        return {
            'next': next_item,
            'later': later_item,
            'drop': drop_item,
        }

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Reading Dashboard')
        lines.append('')
        lines.append('## Current Reads')
        for book in self.current_reads:
            lines.append(f"- Title: {book['title']}")
            lines.append(f"- Why I am reading it: {book['why']}")
            lines.append(f"- Format: {book['format']}")
            lines.append(f"- Current progress: {book['progress']}")
            lines.append(f"- Next stopping point: {book['next_stop']}")
            lines.append('')
        lines.append('## Session Note')
        lines.append(f"- Date: {self.session_note['date']}")
        lines.append(f"- Pages or chapter: {self.session_note['pages_or_chapter']}")
        lines.append(f"- One idea: {self.session_note['idea']}")
        lines.append(f"- One quote or example: {self.session_note['quote']}")
        lines.append(f"- One question: {self.session_note['question']}")
        lines.append('')
        lines.append('## Queue')
        lines.append(f"- Next: {self.queue['next']}")
        lines.append(f"- Later: {self.queue['later']}")
        lines.append(f"- Drop or pause: {self.queue['drop']}")
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('reading-progress-tracker')
    tracker = ReadingProgressTracker(inputs)
    return tracker.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
