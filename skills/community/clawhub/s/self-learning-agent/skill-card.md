## Description:

Knowledge card memory system with semantic search. Agents wake up fresh each session but remember everything through atomic ~350-token cards with YAML frontmatter, daily logs, and a slim master index. Captures lessons, corrections, preferences, and facts automatically. Built for agents that need persistent memory across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent local memory across fresh agent sessions. It structures memory as a small master index, atomic knowledge cards, and daily logs that can be searched, reviewed, and distilled over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages agents to write durable local memory that may include personal, infrastructure, credential-adjacent, or project-confidential information.

Mitigation: Require user confirmation before saving sensitive information, keep memory files out of source control, and maintain review and deletion practices.

Risk: The skill can promote repeated learned content into permanent agent instructions.

Mitigation: Disable AGENTS.md promotion or require manual approval before permanent instruction changes are made.

## Reference(s):

- [Knowledge Card Examples](references/card-examples.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML frontmatter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-organization guidance for local memory cards, daily logs, and a slim master index.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
