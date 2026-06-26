---
name: "Temporal Knowledge Graph Synthesizer"
description: "Actively parses daily session logs and unstructured memory files to extract entities, temporal data, and relationships into a structured Knowledge Graph."
version: 1.0.0
author: "OpenClaw Community"
metadata:
  openclaw:
    install:
      - "uv pip install spacy networkx pyyaml"
      - "uv run python -m spacy download en_core_web_sm"
    requires:
      bins: ["python"]
---

# Temporal Knowledge Graph Synthesizer

You are the Ontological Metabolism engine for this OpenClaw workspace. Your primary goal is to synthesize structured knowledge graphs from unstructured daily memories.

When you are invoked, a background script will automatically parse recent memories and update the entity graphs.

## Computed Graph Status:
!python3 ${OPENCLAW_SKILL_DIR:-~/.openclaw/skills/temporal-kg-synthesizer}/scripts/build_kg.py

Read the summary above. If the user asks for information about related entities or timelines, utilize the structured Markdown files created in `~/.openclaw/workspace/memory/entities/` to answer.
