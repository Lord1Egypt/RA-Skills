---
name: session-atlas
description: Build a source-indexed navigation layer over a private Claude JSONL session, preserving evidence locations and uncertainty without reproducing private reasoning.
---
# Session Atlas
Use scripts/index_claude_session.py with explicit --source and --out-dir paths. Output includes private prompt/assistant text and tool previews: it is NOT anonymized or publication-safe. Choose a private directory outside public repositories. Raw reasoning blocks are represented by hashes and counts only.
Validate with scripts/validate_atlas.py --index-dir DIR --source SOURCE. Add --require-complete-tools when a complete tool trail is required. Without --source, validation is structural only. A valid index does not establish factual or semantic accuracy.
For a human-authored map, use references/methodology.md and templates/atlas.md. Keep source observations, interpretations, decisions, outstanding work and evidence gaps distinct. Link claims to snapshot hashes and line spans. Preserve the difference between requested, prepared, executed and verified.
Do not publish source transcripts, generated indexes or personal paths without separate review and authorization. No external service or private companion skill is required.
