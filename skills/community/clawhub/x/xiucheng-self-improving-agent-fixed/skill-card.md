## Description:

Self-improving agent system that analyzes conversation quality, identifies improvement opportunities, and continuously optimizes response strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pp-chicken](https://clawhub.ai/user/pp-chicken)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to analyze conversation quality, log improvement notes, generate weekly improvement reports, and suggest updates to an agent personality file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can analyze conversations and retain derived improvement notes in workspace files.

Mitigation: Use it only in workspaces where improvement_log.md can safely contain those notes, and avoid automatic analysis for sensitive conversations until consent, retention, and purge controls are clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pp-chicken/skills/xiucheng-self-improving-agent-fixed)
- [Publisher profile](https://clawhub.ai/user/pp-chicken)
- [Project homepage](https://github.com/xiucheng/self-improving-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON analysis results, Markdown reports, text suggestions, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local improvement notes to improvement_log.md and reads SOUL.md when generating update suggestions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
