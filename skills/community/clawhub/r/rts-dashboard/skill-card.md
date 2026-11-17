## Description:

RTS Dashboard provides a browser-based Real-Time Strategy style command center for monitoring OpenClaw agents, skills, sessions, cron jobs, system vitals, and Gateway chat messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[282059559donghui-prog](https://clawhub.ai/user/282059559donghui-prog)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to launch and operate a local RTS-style monitoring dashboard for agents, skills, sessions, cron jobs, system vitals, and Gateway chat actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard may expose OpenClaw conversation content and Gateway controls to anyone who can reach the dashboard port.

Mitigation: Run only in a trusted local environment and restrict network access to the dashboard port; add authentication and strict origin checks before broader deployment.

Risk: Gateway actions and chat messaging can affect connected agents if access is not tightly scoped.

Mitigation: Validate inputs, review Gateway actions before deployment, and require transcript opt-in or redaction when sensitive conversations may be displayed.

Risk: The security evidence recommends reviewing the WebSocket dependency before installation.

Mitigation: Update and scan the ws dependency before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/282059559donghui-prog/skills/rts-dashboard)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and local URL guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start a local Node.js dashboard on localhost and provide Gateway configuration guidance.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
