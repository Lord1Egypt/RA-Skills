# Changelog

## 1.1.2 (2026-03-25)

- **Retrieval:** Updated instructions to explicitly sequence `zettel-link` semantic retrieval as the first step, falling back gracefully to local scripts with a warning if the skill is not installed.
- **Delivery:** Added an explicit Stage 5 requiring the agent to always list the cited references in the chat response.


## 2026-03-02

- Refactored workflow into 4 explicit stages: Retrieval, Preprocess, Draft, Publish.
- Updated skill instructions to require relevance filtering before draft synthesis.
- Added `scripts/compile_preprocess.py` to build a relevance-filtered draft packet and citation list.
- Updated retrieval guidance to:
  - read note count from config,
  - prioritize `zettel-link` semantic retrieval when available,
  - then use local wikilink/tag retrieval.
- Updated agent prompts in `agents/` to align with the stage boundaries and citation requirements.
- Expanded publisher guidance for more natural blog structure, stronger title style guidance, and cleaner section naming.
- Converted strict heading limits into soft style guidance.
- Added draft-level "argument spine" requirements to improve end-to-end coherence.
- Updated preprocess guidance to retain main ideas, high-signal quotes, and key references (links/tags/citations).
- Clarified draft synthesis can center on the full relevant corpus, not only the seed note.
- Added publish rules that the `Argument Spine` is internal scaffolding only and must not appear in final output.
- Added publish output property requirements: valid YAML frontmatter with required `tags`.
- Added `agent_models.retriever` and `agent_models.preprocess` config support for fast/deep tier selection.
- Removed deprecated `scripts/draft_prompt.py` and stale cache artifacts.
- Removed redundant sample file `examples/sample-seed-note.md`.
