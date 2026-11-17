## Description:

Central status dashboard for the PA agent. Use when: owner asks 'what's the status', 'what are you working on', 'what's happening', or any status/overview question. Aggregates active tasks, open issues, monitored groups, pending follow-ups, and system health into one structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

PA owners and administrators use this skill to ask an agent for a structured status report covering active tasks, blockers, group activity, pending follow-ups, completed work, and system health. It can also scope reports to the requester context, such as owner DMs or a specific group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an unsafe shell/Python path handling pattern while reading group metadata.

Mitigation: Review and fix path handling before installation, and avoid interpolating untrusted directory names into inline Python commands.

Risk: The skill can perform credentialed billing health checks and may touch local OpenClaw memory, WhatsApp-derived notes, PA status data, and billing health.

Mitigation: Make external billing checks explicit, opt-in, and cached; restrict access to local memory and status files to authorized agents.

Risk: Full reports, scheduled reports, and PA pings can expose sensitive operational context to the wrong recipient.

Mitigation: Confirm who may receive full reports or pings, enforce requester-based scoping, and never send full supervisor reports in groups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/supervisor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status reports with optional shell and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include scoped status sections, counts, health checks, and follow-up summaries.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
