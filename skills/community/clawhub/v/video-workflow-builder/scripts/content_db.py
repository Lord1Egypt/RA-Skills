#!/usr/bin/env python3
"""Shared helpers for the content asset DB scripts (stdlib only)."""
import json
import os
import re


def resolve_data_root():
    """Return the content-db root for this account.

    Priority: CONTENT_DB_ROOT env override, else derive from this file's
    location. scripts/ lives under <slug>-workflow, which lives under
    ~/.claude/skills (or ~/.codex/skills). Data root is a sibling of skills/:
    ~/.claude/content-db/<slug>/.
    """
    override = os.environ.get("CONTENT_DB_ROOT")
    if override:
        return override
    script_dir = os.path.dirname(os.path.realpath(__file__))
    skill_dir = os.path.dirname(script_dir)          # <slug>-workflow
    skill_name = os.path.basename(skill_dir)
    slug = skill_name[:-len("-workflow")] if skill_name.endswith("-workflow") else skill_name
    skills_root = os.path.dirname(skill_dir)          # .../skills
    base = os.path.dirname(skills_root)               # ~/.claude or ~/.codex
    return os.path.join(base, "content-db", slug)


def slugify(text):
    """Keep CJK + alnum, collapse everything else to single dashes."""
    text = text.strip()
    text = re.sub(r"[^\w一-鿿]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:40]


def _dump_value(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    s = str(value)
    if s == "" or ":" in s or s.strip() != s:
        return json.dumps(s, ensure_ascii=False)
    return s


def dump_frontmatter(meta):
    lines = ["---"]
    for key, value in meta.items():
        lines.append("%s: %s" % (key, _dump_value(value)))
    lines.append("---")
    return "\n".join(lines) + "\n"


def _parse_value(raw):
    raw = raw.strip()
    if raw == "":
        return ""
    if raw[0] in "[{\"":
        try:
            return json.loads(raw)
        except ValueError:
            pass
    return raw


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end].strip("\n")
    body = text[end + len("\n---"):].lstrip("\n")
    meta = {}
    for line in block.splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        meta[key.strip()] = _parse_value(raw)
    return meta, body
