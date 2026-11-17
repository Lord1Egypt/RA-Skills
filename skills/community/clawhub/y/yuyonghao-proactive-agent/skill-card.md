## Description:

Transforms AI agents from task-followers into proactive partners that anticipate needs and continuously improve through persistent memory, verification, and security-hardening patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to add proactive behavior, persistent local memory, context-recovery routines, self-improvement loops, and safety checks to an AI agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory and proactive checks can collect more user or workspace context than intended.

Mitigation: Make memory opt-in, scope readable files and accounts, and define redaction and deletion rules before use.

Risk: Autonomous cron or sub-agent work can act without clear current user intent.

Mitigation: Disable autonomous cron and sub-agent work by default and require explicit approval before enabling it.

Risk: Changes to AGENTS.md or other instruction files can alter future agent behavior.

Mitigation: Require user approval before modifying instruction files and review those changes before deployment.

Risk: The bundled security audit is a lightweight checklist rather than a complete security scanner.

Mitigation: Use the audit as a starting point and add independent review or scanning for deployed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-proactive-agent)
- [Security Patterns Reference](references/security-patterns.md)
- [Onboarding Flow Reference](references/onboarding-flow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operating procedures and workspace file guidance for local agent use.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
