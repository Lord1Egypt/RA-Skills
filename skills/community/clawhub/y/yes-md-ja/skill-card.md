## Description:

YES.md 日本語版 guides coding agents through evidence-based debugging, safer changes, verification after edits, and structured handoff when a task cannot be completed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sstklen](https://clawhub.ai/user/sstklen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill as a Japanese governance checklist for implementation, debugging, configuration, deployment, API integration, and data-processing tasks that require evidence, scoped changes, and post-change verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can push agents to search error messages online, which may expose secrets or sensitive system details.

Mitigation: Require agents to redact credentials, tokens, customer data, hostnames, and other sensitive fragments before any external search.

Risk: The skill requires backups before certain edits, which can create unmanaged copies of secret-bearing files.

Mitigation: Constrain backups to approved locations with clear exclusions, permissions, retention, and cleanup rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sstklen/skills/yes-md-ja)
- [Publisher profile](https://clawhub.ai/user/sstklen)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Encourages agents to provide evidence, verification results, and structured handoff notes.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
