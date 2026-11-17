## Description:

Skill Polisher helps agents track skill quality by collecting feedback, generating health reports, checking specification compliance, and producing read-only improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luciuscao](https://clawhub.ai/user/luciuscao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor OpenClaw skill quality, collect user feedback, define success expectations, inspect compliance with skill conventions, and decide whether to adopt generated improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted skill names can cause persistent records to be written outside the advertised storage area.

Mitigation: Use only trusted skill names and reject names containing slashes, '..', or absolute path components before running the scripts.

Risk: Feedback comments, ratings, tracking history, and success criteria may contain private local data.

Mitigation: Treat ~/.openclaw/workspace/.skill-polisher/ as private local storage and review its contents before sharing, syncing, or publishing.

Risk: The security evidence recommends review before installation.

Mitigation: Review the skill before installing or running it, and improve path validation, file permissions, and deletion controls before broad deployment.

## Reference(s):

- [Skill Polisher on ClawHub](https://clawhub.ai/luciuscao/skills/skill-polisher)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Skill Best Practices](references/BEST-PRACTICES.md)
- [Skill Development Pitfalls](references/PITFALLS.md)
- [Skill Quality Standards Checklist](references/QUALITY-STANDARDS.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Terminal text plus Markdown and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores feedback, expectations, tracking history, metrics, and suggestion history under ~/.openclaw/workspace/.skill-polisher/.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
