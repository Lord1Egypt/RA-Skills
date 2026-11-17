## Description:

Skill Inventory Expert helps AI agents discover, catalog, and report installed skills in structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saqierma-cyber](https://clawhub.ai/user/saqierma-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to inventory local agent skills, summarize their capabilities, and produce a compact structured report for assessment or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to inspect local skill directories and skill configuration metadata, which may expose sensitive local setup details if shared broadly.

Mitigation: Review generated inventories before sharing, avoid dumping full SKILL.md contents, and inspect ~/.claude/skills.json only when exposing local skill configuration metadata is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/saqierma-cyber/skills/skill-inventory-expert)
- [Publisher Profile](https://clawhub.ai/user/saqierma-cyber)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON examples and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local skill inventory guidance and sample structured inventory output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
