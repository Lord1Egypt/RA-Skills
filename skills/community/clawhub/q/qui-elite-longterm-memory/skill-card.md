## Description:

Provides an AI agent memory workflow and CLI for maintaining session state, long-term Markdown archives, semantic recall, git-notes guidance, and optional cloud backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to initialize and maintain persistent memory for AI coding agents. It helps create session state, curated Markdown memory, daily logs, semantic recall practices, git-notes guidance, and optional SkillBoss backup or extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages long-term retention of conversation facts, preferences, decisions, and workspace context.

Mitigation: Review what is written to memory files, keep sensitive projects local-only where possible, and regularly inspect or prune stored memories.

Risk: The documented optional SkillBoss auto-extraction flow can send conversation content to a third-party service.

Mitigation: Avoid enabling SkillBoss auto-extraction for sensitive, private, regulated, or secret-bearing conversations unless the user has approved that processing.

Risk: The guidance describes silently persisting decisions and facts, which can record information the user did not intend to preserve.

Mitigation: Require explicit user approval before silently storing facts or decisions, especially when the content includes personal data, credentials, private code, or business-sensitive context.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/quincygunter/skills/qui-elite-longterm-memory)
- [npm package](https://www.npmjs.com/package/elite-longterm-memory)
- [ClawdHub source skill page](https://clawdhub.com/skills/elite-longterm-memory)
- [Bulletproof Memory reference](https://clawdhub.com/skills/bulletproof-memory)
- [LanceDB Memory reference](https://clawdhub.com/skills/lancedb-memory)
- [Git Notes Memory reference](https://clawdhub.com/skills/git-notes-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, JavaScript examples, and generated Markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can create SESSION-STATE.md, MEMORY.md, and daily files under memory/; optional cloud and extraction flows require SKILLBOSS_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package.json report 1.2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
