## Description:

Unified web search skill. Fallback order: web_search (Brave), DuckDuckGo, then claude.ai, with search results saved to memory/research/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run web research through a three-tier search fallback and preserve search outputs for later review. It supports fast searches, current-news queries, Korean/regional search, and complex research workflows that may require browser-based Claude search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to Brave, DuckDuckGo, and a logged-in claude.ai browser session.

Mitigation: Use the skill only for queries that may be shared with those services, and avoid confidential, regulated, personal, or secret-bearing content.

Risk: Search history and results may be persistently saved under memory/research/ without clear retention controls.

Mitigation: Review, disable, or manually manage the cache before use in sensitive environments.

Risk: Browser-based fallback depends on an authenticated claude.ai session and may be slow or subject to usage limits.

Mitigation: Prefer Brave or DuckDuckGo paths when available and reserve browser fallback for cases where those methods fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/web-claude)
- [Claude new chat](https://claude.ai/new)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and saved research notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save queries, timestamps, methods, links, summaries, and extracted insights under memory/research/.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
