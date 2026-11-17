## Description:

A living knowledge base of strategy lessons and banned code patterns that helps agents avoid repeating past strategy mistakes by scanning code and generating decision context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tltby12341](https://clawhub.ai/user/tltby12341)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and strategy researchers use this skill to record lessons from strategy iterations, maintain banned code patterns, scan new strategy code for known violations, and produce concise LLM decision context before generating new strategy code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary lesson text can become persistent prompt influence when reused as LLM decision context.

Mitigation: Review stored lessons before use, avoid importing unreviewed text directly into system prompts, and inspect lessons.json regularly.

Risk: Automation or users with write access to the memory directory can add misleading lessons or bans.

Mitigation: Limit write access to trusted users and automation, keep the memory directory scoped to the project, and audit bans.json before relying on scan results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tltby12341/skills/strategy-constitutional-memory)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text guidance with Python snippets, shell commands, scan results, and JSON-backed memory records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates human-readable lessons.json and bans.json files in the configured memory directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
