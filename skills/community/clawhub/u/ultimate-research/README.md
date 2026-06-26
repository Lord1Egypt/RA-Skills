# Ultimate Research

[![ClawHub](https://img.shields.io/badge/ClawHub-Published-111827?style=flat-square)](https://clawhub.ai/nemesis0017/ultimate-research)

A clean, opinionated meta-skill for turning broad questions into one structured, evidence-backed answer.

This repository is intentionally small and easy to maintain: one skill, one deterministic routing helper, and one short routing guide.

## Release status

- Latest published version: **1.0.2**
- No further version bumps planned unless the skill meaningfully changes

## What it does

- Clarifies vague questions before research starts
- Pulls prior context from memory before making assumptions
- Uses a mandatory core of routing skills for every query
- Adds only the specialist skills that materially improve the answer
- Merges everything into one structured response
- Includes citations only when the query is research-heavy

## Repository layout

```text
SKILL.md
scripts/ultimate_research.py
references/routing.md
CHANGELOG.md
```

## Design principles

- **Speed**: keep routing deterministic and minimal
- **Quality**: use the smallest useful skill set, then synthesise once
- **Reliability**: never invent facts; ask a clarifying question when needed
- **Consistency**: return answers in the same five-part structure every time

## Output format

1. Question breakdown
2. Skills used
3. Evidence
4. Recommendation
5. Next steps

## Usage

The skill is designed for research, strategy, comparison, market, SEO, pricing, launch, analytics, and other multi-step questions.

For a quick deterministic routing draft, run:

```bash
python3 scripts/ultimate_research.py "your query"
```

## Release notes

See `CHANGELOG.md` for the latest repository updates and published skill versions.

## ClawHub listing

Published skill: https://clawhub.ai/nemesis0017/ultimate-research

## Notes

- The skill file is the source of truth for behaviour.
- The router script is a deterministic aid, not a replacement for judgement.
- The repository is designed to be easy to review, easy to extend, and easy to publish.