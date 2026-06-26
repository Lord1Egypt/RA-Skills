#!/usr/bin/env python3
import sys
from typing import Dict, List

SCENARIO_LIBRARY: Dict[str, Dict[str, object]] = {
    'Refund Request': {
        'keywords': ['refund', 'money back', 'refund request'],
        'summary': 'Customers want a refund decision, timeline clarity, and confidence that the policy is applied consistently.',
        'checks': ['order ID', 'purchase date', 'refund reason', 'item condition', 'payment method'],
        'approval': ['high-value refunds', 'manual compensation', 'fraud or abuse suspicion'],
    },
    'Return / Exchange': {
        'keywords': ['return', 'exchange', 'swap', 'replace'],
        'summary': 'Customers need eligibility guidance, logistics instructions, and a clear next step for return or exchange handling.',
        'checks': ['order ID', 'purchase date', 'product category', 'opened or used status', 'preferred outcome'],
        'approval': ['out-of-policy exceptions', 'damaged-item disputes', 'inventory override'],
    },
    'Delivery Delay': {
        'keywords': ['delivery delay', 'delay', 'late', 'tracking', 'shipment', 'not arrived'],
        'summary': 'Customers need status clarity, reassurance, and consistent escalation when the shipment is late or unclear.',
        'checks': ['order ID', 'tracking status', 'carrier milestone', 'promised date', 'customer urgency'],
        'approval': ['reshipment', 'compensation offer', 'warehouse escalation'],
    },
    'Payment Failure': {
        'keywords': ['payment failure', 'payment failed', 'declined', 'card issue', 'checkout payment'],
        'summary': 'Customers need a fast diagnosis path that separates payment-method issues from merchant-side outages or policy blocks.',
        'checks': ['order ID if created', 'payment method', 'error message', 'attempt timestamp', 'device or channel'],
        'approval': ['suspected fraud', 'manual order creation', 'billing exception'],
    },
    'VIP Escalation': {
        'keywords': ['vip', 'priority customer', 'high value customer', 'executive complaint'],
        'summary': 'The team needs a high-touch path with tighter response time, ownership, and approval visibility.',
        'checks': ['customer tier', 'recent order value', 'issue severity', 'promised SLA', 'assigned owner'],
        'approval': ['non-standard compensation', 'public relations risk', 'founder or leadership review'],
    },
    'Bot Handoff': {
        'keywords': ['bot handoff', 'human handoff', 'handoff', 'agent handoff'],
        'summary': 'The flow must collect the right fields early and transfer context cleanly to a human agent.',
        'checks': ['contact reason', 'order ID if available', 'customer language', 'uploaded proof', 'bot summary'],
        'approval': ['policy conflict', 'sensitive complaint', 'repeat unresolved issue'],
    },
}

CHANNEL_RULES = {
    'Email': ['email'],
    'Live Chat': ['chat', 'live chat', 'intercom', 'chatbot'],
    'Marketplace IM': ['marketplace', 'im', 'amazon message', 'shop message'],
    'Call Notes': ['call', 'phone'],
}


class SupportFlowBuilder:
    def __init__(self, text: str):
        self.text = (text or '').strip()
        self.lower = self.text.lower()
        self.scenario = self._detect_scenario()
        self.channels = self._detect_channels()

    def _detect_scenario(self) -> str:
        for scenario in ['Return / Exchange', 'Refund Request', 'Delivery Delay', 'Payment Failure', 'VIP Escalation', 'Bot Handoff']:
            if any(keyword in self.lower for keyword in SCENARIO_LIBRARY[scenario]['keywords']):
                return scenario
        return 'Refund Request'

    def _detect_channels(self) -> List[str]:
        channels = [name for name, keywords in CHANNEL_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return channels or ['Email', 'Live Chat']

    def _flow_steps(self) -> List[str]:
        details = SCENARIO_LIBRARY[self.scenario]
        checks = details['checks']
        return [
            f'Intake: collect {", ".join(checks[:3])} before promising an outcome.',
            f'Qualification: verify policy fit across {", ".join(checks[3:])}.',
            'Decision: approve, deny, route to another team, or request missing information with a clear reason.',
            'Closure: confirm timeline, owner, and the next customer-visible update.',
        ]

    def _agent_playbook(self) -> List[str]:
        details = SCENARIO_LIBRARY[self.scenario]
        checks = details['checks']
        return [
            f'Ask only the minimum required questions first: {", ".join(checks)}.',
            'State the policy or rule in plain language before giving the resolution.',
            'If the case is outside policy, explain the exception path instead of improvising a promise.',
            'Leave an internal note that captures evidence, decision, and next owner.',
        ]

    def _macro_for_channel(self, channel: str) -> str:
        scenario_phrase = self.scenario.lower()
        if channel == 'Email':
            return f'Subject: Update on your {scenario_phrase} request\n\nHi there, thanks for contacting us. I am reviewing your case and will confirm the next step as soon as I verify the required details.'
        if channel == 'Live Chat':
            return f'Thanks for reaching out. I can help with this {scenario_phrase} request. First, please share your order ID and the key detail that best describes the issue.'
        if channel == 'Marketplace IM':
            return f'Thanks for your message. Please send your order number and a short note about the {scenario_phrase} issue so we can review the correct policy path.'
        return f'Call-note template: Confirm the customer goal, restate the {scenario_phrase} policy path, and log the next promised update.'

    def _knowledge_gaps(self) -> List[str]:
        base = ['Document the exact approval owner for edge cases so frontline agents do not guess.']
        if self.scenario in ('Refund Request', 'Return / Exchange'):
            base.append('Clarify any category exclusions, opened-item rules, and refund timing promises.')
        if self.scenario == 'Delivery Delay':
            base.append('Document compensation thresholds and warehouse-escalation criteria by delay severity.')
        if self.scenario == 'Payment Failure':
            base.append('Document what agents may suggest safely versus what must be escalated to payments or fraud review.')
        if self.scenario == 'Bot Handoff':
            base.append('Define the required structured fields so the bot does not hand off empty context.')
        return base

    def render(self) -> str:
        details = SCENARIO_LIBRARY[self.scenario]
        lines: List[str] = []
        lines.append('# Support Flow Design Pack')
        lines.append('')
        lines.append(f'**Primary scenario:** {self.scenario}')
        lines.append(f'**Channels:** {", ".join(self.channels)}')
        lines.append('**Method note:** This is a policy-grounded support design pack. No live helpdesk, bot builder, or ticket analytics system was accessed.')
        lines.append('')
        lines.append('## Intent Summary')
        lines.append(f'- {details["summary"]}')
        lines.append('- Design the flow so frontline agents know what to collect, what to decide, and when to escalate.')
        lines.append('')
        lines.append('## Support Flow Map')
        for idx, step in enumerate(self._flow_steps(), 1):
            lines.append(f'{idx}. {step}')
        lines.append('')
        lines.append('## Agent Playbook')
        for bullet in self._agent_playbook():
            lines.append(f'- {bullet}')
        lines.append('')
        lines.append('## Macros / Canned Responses')
        for channel in self.channels:
            lines.append(f'### {channel}')
            lines.append(self._macro_for_channel(channel))
            lines.append('')
        lines.append('## Bot Handoff Fields')
        lines.append('- Customer name or handle')
        lines.append(f'- Required scenario checks: {", ".join(details["checks"])}')
        lines.append('- Existing transcript summary and any uploaded proof')
        lines.append('- Urgency, sentiment, and requested outcome')
        lines.append('')
        lines.append('## Governance and QA')
        lines.append(f'- Human review required for: {", ".join(details["approval"])}.')
        lines.append('- Review macro tone, legal wording, and compensation promises before rollout.')
        lines.append('- Version the flow when policy changes so new agents are not trained on stale guidance.')
        lines.append('')
        lines.append('## Knowledge Gaps to Close Next')
        for bullet in self._knowledge_gaps():
            lines.append(f'- {bullet}')
        return '\n'.join(lines)


def handle(user_input: str) -> str:
    return SupportFlowBuilder(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
