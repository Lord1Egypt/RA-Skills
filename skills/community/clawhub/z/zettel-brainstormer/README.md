# Zettel Brainstormer

An AI-powered skill for expanding a seed zettel into a referenced, publishable post.

This works best when paired with the `zettel-link` skill from the same repo for semantic retrieval before local link/tag retrieval.

- Local path: `../zettel-link`
- Skill doc: [`../zettel-link/SKILL.md`](../zettel-link/SKILL.md)

## Overview

This skill uses a **4-stage pipeline**:
1. **Retrieval**: pick retrieval count from config, prefer semantic candidates from `zettel-link` when available, then use local wikilink/tag retrieval.
2. **Preprocess**: run one subagent per candidate note to extract relevance and key evidence.
3. **Draft**: synthesize only relevant notes into a structured draft with citations.
4. **Publish**: rewrite into natural language and keep a final `## References` section.

## Core Docs

- Full workflow: `SKILL.md`
- Agent prompts: `agents/`
- Scripts: `scripts/`

## Quick Start

1. Configure the skill once:
```bash
python zettel-brainstormer/scripts/setup.py
```
2. (Recommended) Prepare semantic retrieval with `zettel-link`:
```bash
uv run zettel-link/scripts/embed.py --input <your-zettel-dir>
uv run zettel-link/scripts/search.py --input <your-zettel-dir> --query "<seed topic>"
```
3. Retrieve local linked/tag notes for the seed:
```bash
python zettel-brainstormer/scripts/find_links.py \
  --input "/abs/path/Seed Note.md" \
  --output /tmp/zettel_candidates.json
```
4. Preprocess candidates with subagents and save outputs into `/tmp/zettel_preprocess/*.md`.
5. Compile the draft packet from relevant preprocess results:
```bash
python zettel-brainstormer/scripts/compile_preprocess.py \
  --seed "/abs/path/Seed Note.md" \
  --preprocess-dir /tmp/zettel_preprocess \
  --output /tmp/zettel_draft_packet.json
```
6. Draft with `agents/draft.md`, then publish with `agents/publisher.md` and include `## References`.
