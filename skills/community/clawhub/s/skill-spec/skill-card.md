## Description:

Use when identifying skill candidates from repeated work, managing skill change proposals, reviewing candidates, or chaining skills into workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chamberz40](https://clawhub.ai/user/chamberz40)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-skill maintainers use this skill to identify repeatable Claude Code work, review skill candidates, scaffold new skills, manage change proposals, and suggest downstream skill chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on hooks can record session IDs, tool counts, and tool names across Claude Code sessions.

Mitigation: Review hook configuration before installation, narrow hook matchers where practical, and provide an explicit way to inspect, purge, or disable candidate logging.

Risk: Hook state is stored in shared /tmp paths derived from the session ID.

Mitigation: Move hook state to a scoped user-owned directory and sanitize hook input before using it in file paths.

Risk: The skill can guide creation or modification of skill files and change proposals.

Mitigation: Review generated scaffolds and proposals before use, and run the included hook validation script after changes to hook behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chamberz40/skills/skill-spec)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, and skill file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update skill files, candidate logs, change proposals, and hook configuration when the agent follows the skill.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
