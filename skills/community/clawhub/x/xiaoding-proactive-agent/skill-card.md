## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve, with WAL Protocol, Working Buffer, Autonomous Crons, and battle-tested patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent memory, proactive check-ins, reverse prompting, self-healing routines, and safety practices to an AI agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad local plaintext memory that could capture secrets or sensitive personal data.

Mitigation: Make memory capture opt-in, exclude secrets and sensitive personal data, and review memory files before sharing or syncing them.

Risk: Proactive heartbeats, crons, or isolated agent turns can run checks without clear user scoping.

Mitigation: Disable recurring or autonomous actions unless explicitly configured, and require user approval for each scope and schedule.

Risk: Email, calendar, browser, desktop, and cleanup actions can affect private data or user workspaces.

Mitigation: Restrict these actions to user-approved scopes and require confirmation before external communication, deletion, cleanup, or publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/asterisk622/skills/xiaoding-proactive-agent)
- [Publisher Profile](https://clawhub.ai/user/asterisk622)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)
- [Creator Profile](https://x.com/halthelobster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates, checklists, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes starter memory, onboarding, heartbeat, operating-rules, and tool-configuration files for an agent workspace.]

## Skill Version(s):

3.1.3 (source: server release evidence; artifact frontmatter reports 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
