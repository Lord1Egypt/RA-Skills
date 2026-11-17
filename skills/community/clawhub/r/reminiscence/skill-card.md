## Description:

Reminiscence-追忆 provides local semantic memory search over OpenClaw memory files using BM25 and multi-signal reranking without external APIs or model dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indivisible2025](https://clawhub.ai/user/indivisible2025)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to search local workspace memory records, including MEMORY.md and daily memory markdown files, for prior decisions, configurations, and historical notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local OpenClaw memory files that may contain secrets, private conversations, client data, or credentials.

Mitigation: Install and invoke it only when local memory search is intended, and keep the ~/.openclaw directory private to the user account.

Risk: The skill creates persistent plaintext search indexes and token caches from memory content.

Mitigation: Inspect or delete ~/.openclaw/memory_bm25_index.json and ~/.openclaw/memory_bm25_token_cache.json when retention is not desired.

Risk: Loose activation wording may cause memory search to run in broad recall scenarios.

Mitigation: Review search requests before execution when the workspace memory may contain sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indivisible2025/skills/reminiscence)
- [Publisher profile](https://clawhub.ai/user/indivisible2025)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown and terminal-style search results with file paths, line ranges, scores, and excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output is ranked and deduplicated, with up to eight results by default.]

## Skill Version(s):

7.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
