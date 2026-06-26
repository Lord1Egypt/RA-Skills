"""Support ticket parser — parse tickets from various text formats."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class TicketInfo:
    """Parsed ticket metadata."""
    title: str = ""
    description: str = ""
    reporter: str = ""
    priority: str = ""
    labels: list[str] = field(default_factory=list)
    raw: str = ""
    sections: dict[str, str] = field(default_factory=dict)


def parse_markdown_ticket(text: str) -> TicketInfo:
    """Parse a markdown-formatted ticket."""
    ticket = TicketInfo(raw=text)

    lines = text.splitlines()

    # Extract title from first heading
    for line in lines:
        if line.startswith("# "):
            ticket.title = line[2:].strip()
            break

    # Extract sections by heading
    current_section = ""
    section_lines: list[str] = []

    for line in lines:
        heading_match = re.match(r"^#{1,3}\s+(.+)", line)
        if heading_match:
            if current_section and section_lines:
                ticket.sections[current_section] = "\n".join(section_lines).strip()
            current_section = heading_match.group(1).strip().lower()
            section_lines = []
        else:
            section_lines.append(line)

    if current_section and section_lines:
        ticket.sections[current_section] = "\n".join(section_lines).strip()

    # Try to extract common fields from sections
    for key in ("description", "summary", "details", "问题描述", "bug描述"):
        if key in ticket.sections:
            ticket.description = ticket.sections[key]
            break

    if not ticket.description:
        # Use everything after the title as description
        title_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("# "):
                title_idx = i
                break
        ticket.description = "\n".join(lines[title_idx + 1 :]).strip()

    # Extract priority/labels from metadata-style lines
    for line in lines:
        pri_match = re.match(r"(?:Priority|优先级|严重等级)[:\s]+(\S+)", line, re.IGNORECASE)
        if pri_match:
            ticket.priority = pri_match.group(1)
        reporter_match = re.match(r"(?:Reporter|报告人|提交人)[:\s]+(.+)", line, re.IGNORECASE)
        if reporter_match:
            ticket.reporter = reporter_match.group(1).strip()
        label_match = re.match(r"(?:Labels?|标签)[:\s]+(.+)", line, re.IGNORECASE)
        if label_match:
            ticket.labels = [l.strip() for l in label_match.group(1).split(",")]

    return ticket


def parse_plain_ticket(text: str) -> TicketInfo:
    """Parse a plain-text ticket (e.g., pasted from email or chat)."""
    ticket = TicketInfo(raw=text, description=text.strip())

    lines = text.splitlines()
    if lines:
        # Use first non-empty line as title
        for line in lines:
            if line.strip():
                ticket.title = line.strip()[:120]
                break
    return ticket


def parse_ticket(text: str) -> TicketInfo:
    """Auto-detect ticket format and parse."""
    # Check if it looks like markdown
    has_headings = bool(re.search(r"^#{1,3}\s+", text, re.MULTILINE))
    if has_headings:
        return parse_markdown_ticket(text)
    return parse_plain_ticket(text)
