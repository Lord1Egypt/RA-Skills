## Description:

Skill Finder CN Pro helps users discover and install ClawHub Skills by turning Chinese or English skill-finding requests into ClawHub searches and installation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find ClawHub Skills that match a task, inspect candidate skills, and decide whether to install them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results may lead users toward third-party skills that have their own behavior and risks.

Mitigation: Inspect recommended skills and approve any install command deliberately before installation.

Risk: The bundled search helper emits Chinese messages, which may be inconvenient for English-only users.

Mitigation: Review command output carefully and adjust the query or workflow when English-only output is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/skills/skill-finder-cn-pro)
- [Publisher Profile](https://clawhub.ai/user/lvjunjie-byte)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawhub CLI for search, inspect, and install commands.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
