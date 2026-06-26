"""
yumnb notification dispatcher — post a small payload to a webhook after
`publish`. Supports Slack, Discord, Teams (Power Automate Workflow), or
generic JSON. No org-specific defaults.
"""
from __future__ import annotations

from typing import Dict, Optional

import requests


def _slack_payload(title: str, summary: str, links: Dict[str, str]) -> dict:
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"📓 {title}"}},
    ]
    if summary:
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": summary}})
    if links:
        link_md = " · ".join(f"<{url}|{label}>" for label, url in links.items() if url)
        if link_md:
            blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": link_md}]})
    return {"text": title, "blocks": blocks}


def _discord_payload(title: str, summary: str, links: Dict[str, str]) -> dict:
    desc_parts = []
    if summary:
        desc_parts.append(summary)
    if links:
        desc_parts.append("\n".join(f"[{label}]({url})" for label, url in links.items() if url))
    return {
        "embeds": [{
            "title": f"📓 {title}"[:256],
            "description": "\n\n".join(desc_parts)[:4000],
            "color": 0x1F4E79,
        }]
    }


def _teams_workflow_payload(title: str, summary: str, links: Dict[str, str]) -> dict:
    """For Teams 'Post to a channel when a webhook request is received' Workflow."""
    body = [
        {"type": "TextBlock", "text": f"📓 {title}", "size": "Large",
         "weight": "Bolder", "wrap": True},
    ]
    if summary:
        body.append({"type": "TextBlock", "text": summary, "wrap": True})
    actions = [{"type": "Action.OpenUrl", "title": label, "url": url}
               for label, url in links.items() if url]
    return {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.4",
                "body": body,
                "actions": actions,
            },
        }],
    }


def _generic_payload(title: str, summary: str, links: Dict[str, str]) -> dict:
    return {"title": title, "summary": summary, "links": links}


_STYLES = {
    "slack": _slack_payload,
    "discord": _discord_payload,
    "teams_workflow": _teams_workflow_payload,
    "generic": _generic_payload,
}


def post(webhook_url: Optional[str], style: str,
         title: str, summary: str, links: Dict[str, str]) -> Optional[int]:
    if not webhook_url:
        return None
    builder = _STYLES.get((style or "generic").lower(), _generic_payload)
    payload = builder(title, summary, links)
    r = requests.post(webhook_url, json=payload, timeout=20)
    print(f"webhook [{style}] -> {r.status_code}")
    return r.status_code
