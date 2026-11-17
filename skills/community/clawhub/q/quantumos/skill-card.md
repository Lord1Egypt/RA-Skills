## Description:

Install and manage QuantumOS, an AI command center dashboard for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[murtiurti4](https://clawhub.ai/user/murtiurti4)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to install, start, stop, update, and troubleshoot the QuantumOS dashboard. The dashboard supports real-time chat, Mission Control task tracking, feed aggregation, and agent settings for an OpenClaw environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may grant mutable third-party code access to an OpenClaw gateway token.

Mitigation: Install only from a pinned, reviewed release and avoid copying broad gateway tokens into project files.

Risk: Mission Control integration can add persistent automation that causes future agents to act on dashboard-created tasks.

Mitigation: Add the HEARTBEAT.md automation only when automatic task triage is intended, and review created tasks before agents act on them.

## Reference(s):

- [QuantumOS ClawHub listing](https://clawhub.ai/murtiurti4/skills/quantumos)
- [Node.js](https://nodejs.org)
- [xAI Console](https://console.x.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt the user for an OpenClaw gateway token during setup.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
