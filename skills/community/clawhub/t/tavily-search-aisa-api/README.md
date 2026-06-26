# Tavily Search

Release-ready ClawHub skill package generated from `targetSkills/tavily-search`.

- Skill name: `tavily-search`
- Entry point: `SKILL.md`
- Runtime assets: `scripts/`, `references/`, `assets/` when present

## Notes

- Advanced web search via Tavily through AIsa API. Supports search depth, topic filtering (general/news/finance), time ranges, domain inclusion/exclusion, and LLM-generated answers. Use when: the user needs web search, research, source discovery, or content extraction.
- This README is release-specific and replaces source READMEs that were written for other runtimes.
- If the underlying instructions mention OpenClaw, treat that as source-context or compatibility guidance unless the skill is specifically about OpenClaw setup.

## Quick Start

1. Open `SKILL.md` to review invocation guidance and runtime requirements.
2. Set any required environment variables before running bundled scripts.
3. Use repo-relative paths like `python3 scripts/...` when following command examples.
