---
name: verifier
description: Trust and evidence verification engine for claims, sources, screenshots, profiles, offers, and suspicious messages. Use whenever the user asks whether something is true, credible, safe, trustworthy, manipulated, misleading, or worth believing. Evaluates evidence quality, source reliability, internal consistency, and obvious red flags. Produces a clear verdict, confidence level, risk notes, missing evidence, and a recommended next verification step. Local-only storage.
---

# Verifier: Trust the evidence, not the vibe.

## Core Philosophy
1. Verify claims, not feelings.
2. Distinguish evidence from presentation.
3. Confidence should reflect proof quality, not tone or certainty.
4. When proof is weak, say what is missing.

## Runtime Requirements
- Python 3 must be available as `python3`
- No external packages required

## Agent vs Script Responsibilities
- The LLM must extract text from screenshots, summarize external links, and convert outside content into structured evidence before passing it into verifier scripts.
- Verifier scripts do not browse the web, inspect images directly, or fetch remote content.
- Verifier scripts score only the claim and evidence that have already been provided.

## Storage
All data is stored locally only under:
- `~/.openclaw/workspace/memory/verifier/cases.json`

No external sync. No cloud storage. No third-party APIs.

## Case Types
- `claim`: A statement that needs verification
- `source`: A source whose credibility needs assessment
- `screenshot`: An image or claimed visual proof
- `profile`: A person or identity claim
- `offer`: A proposal, deal, or opportunity
- `message`: A suspicious or questionable message
- `website`: A site or page that needs trust evaluation

## Evidence Schema
Each evidence item should be structured with:
- `id`
- `type`
- `content`
- `support_level` (`supports`, `contradicts`, `neutral`)
- `source_label`
- `added_at`

## Core Outputs
Each verification case should aim to produce:
- a verdict
- a confidence level
- risk notes
- missing evidence
- a recommended next step

## Key Workflows
- **Capture a case**: `add_case.py --title "..." --type claim --claim "..."`
- **Score a case**: `score_case.py --id VER-XXXX`
- **Review a case**: `show_case.py --id VER-XXXX`
- **Update evidence**: `update_case.py --id VER-XXXX --notes "..."`
- **Close a case**: `close_case.py --id VER-XXXX --verdict inconclusive`
- **List open cases**: `list_cases.py`

## Scripts
| Script | Purpose |
|---|---|
| `add_case.py` | Capture a new verification case |
| `score_case.py` | Score credibility, risk, and evidence quality |
| `show_case.py` | Show one case in detail |
| `list_cases.py` | List stored cases |
| `update_case.py` | Update notes, status, and evidence |
| `close_case.py` | Close a case with final verdict |
| `init_storage.py` | Initialize local storage |
