#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Sequence, Union

QaInput = Union[str, Dict[str, Any]]

REVIEW_MODE_RULES = {
    'Escalation Reduction': ['escalation', 'refund', 'angry customer', 'complaint'],
    'CSAT Recovery': ['csat', 'satisfaction', 'low score', 'bad feedback'],
    'Marketplace Support Audit': ['marketplace', 'amazon buyer message', 'shopify inbox'],
    'New Hire Ramp': ['new hire', 'onboarding', 'ramp'],
    'Calibration Sprint': ['calibration', 'scorecard', 'rubric'],
}

CHANNEL_RULES = {
    'Live chat': ['chat', 'live chat'],
    'Email support': ['email'],
    'Phone support': ['phone', 'call'],
    'Social DM': ['dm', 'social', 'instagram', 'facebook', 'wechat'],
    'Marketplace tickets': ['marketplace', 'amazon', 'ticket'],
}

FOCUS_RULES = {
    'Policy compliance': ['policy', 'compliance', 'refund policy'],
    'Empathy and tone': ['empathy', 'tone', 'rude', 'robotic'],
    'Resolution quality': ['resolve', 'resolution', 'solved', 'fix'],
    'Response speed': ['slow', 'sla', 'response time', 'delay'],
    'Documentation accuracy': ['notes', 'documentation', 'case note', 'logging'],
}

ISSUE_RULES = {
    'Slow first response': ['slow', 'delay', 'waiting'],
    'Low empathy / robotic tone': ['robotic', 'cold', 'rude', 'empathy'],
    'Policy misquote': ['wrong policy', 'policy', 'incorrect refund'],
    'Incomplete troubleshooting': ['did not solve', 'not solved', 'troubleshoot', 'incomplete'],
    'Excessive escalation or transfer': ['escalation', 'transfer', 'handoff'],
    'Weak case notes': ['notes', 'logging', 'documentation'],
}


def _normalize_input(user_input: QaInput) -> str:
    if isinstance(user_input, dict):
        chunks: List[str] = []
        for key in ['channel', 'goal', 'issues', 'team_context', 'sample', 'notes']:
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


class ServiceQaCoach:
    def __init__(self, user_input: QaInput):
        self.raw = user_input
        self.text = _normalize_input(user_input)
        self.lower = self.text.lower()
        self.review_mode = _match_one(self.lower, REVIEW_MODE_RULES, 'Calibration Sprint')
        self.channels = _match_many(self.lower, CHANNEL_RULES, ['Live chat', 'Email support'], limit=4)
        self.focus_areas = _match_many(self.lower, FOCUS_RULES, ['Empathy and tone', 'Resolution quality'], limit=4)
        self.issue_flags = _match_many(self.lower, ISSUE_RULES, ['Slow first response', 'Low empathy / robotic tone'], limit=4)

    def _rubric_rows(self) -> List[List[str]]:
        rows = {
            'Policy compliance': ['Policy compliance', 'Was the answer accurate, safe, and aligned to policy?', 'Incorrect policy guidance creates risk fast.'],
            'Empathy and tone': ['Empathy and tone', 'Did the customer feel understood without losing clarity?', 'Cold or robotic tone can escalate frustration even when the answer is technically correct.'],
            'Resolution quality': ['Resolution quality', 'Did the interaction move the case materially closer to a solution?', 'Fast replies that do not solve the problem still create repeat contact.'],
            'Response speed': ['Response speed', 'Was the timing appropriate for the channel and case severity?', 'Speed matters, but not more than accuracy and clarity.'],
            'Documentation accuracy': ['Documentation accuracy', 'Could another agent pick up the case cleanly from the notes?', 'Weak notes drive repeat work and messy escalations.'],
        }
        return [rows[item] for item in self.focus_areas if item in rows]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Service QA Coaching Brief')
        lines.append('')
        lines.append(f'**Review mode:** {self.review_mode}')
        lines.append(f'**Support channels:** {_join(self.channels)}')
        lines.append(f'**Focus areas:** {_join(self.focus_areas)}')
        lines.append(f'**Issue flags:** {_join(self.issue_flags)}')
        lines.append('**Method note:** This is a heuristic QA brief. No live ticketing, CRM, call, or chat system was accessed.')
        lines.append('')
        lines.append('## QA Summary')
        lines.append('- Separate whether the team has a knowledge problem, a behavior problem, or an operating-rhythm problem.')
        lines.append('- Score quality on what helps the customer move forward, not on script compliance alone.')
        lines.append(f'- Because the main review mode is **{self.review_mode.lower()}**, the plan should focus on repeatable coaching rather than one-off criticism.')
        lines.append('')
        lines.append('## Scorecard Rubric')
        lines.append('| Dimension | Core question | Coaching angle |')
        lines.append('|---|---|---|')
        for row in self._rubric_rows():
            lines.append(f'| {row[0]} | {row[1]} | {row[2]} |')
        lines.append('')
        lines.append('## Failure Mode Review')
        for item in self.issue_flags:
            lines.append(f'- **{item}:** isolate where the workflow, training, or judgment broke instead of blaming the agent generically.')
        lines.append('')
        lines.append('## Coaching Plan')
        lines.append('1. Review a small but representative sample and tag every miss by failure mode, not by gut feel alone.')
        lines.append('2. Turn the top two recurring misses into short coaching moments with examples of what good looks like.')
        lines.append('3. Recheck the same agent or queue quickly after coaching so improvement is measured, not assumed.')
        lines.append('4. Escalate process or policy gaps separately from individual coaching needs.')
        lines.append('')
        lines.append('## Calibration and Sampling Plan')
        lines.append('- Use the same sample definition across reviewers so scores are comparable.')
        lines.append('- Calibrate on edge cases first, especially refunds, angry customers, or unclear policy situations.')
        lines.append('- Keep one running list of rubric disagreements and resolve them before changing score weights.')
        lines.append('')
        lines.append('## Assumptions and Limits')
        lines.append('- This brief is heuristic and depends on the notes, excerpts, and issue framing supplied by the user.')
        lines.append('- Privacy, compliance, HR, refund, and disciplinary decisions remain human-approved.')
        lines.append('- Tiny or anecdotal samples should be treated as signals to inspect further, not as proof of team-wide performance.')
        return "\n".join(lines)


def handle(user_input: QaInput) -> str:
    return ServiceQaCoach(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
