## Description:

Use OpenMarlin from OpenClaw to answer questions, run tasks, and manage OpenMarlin account setup and billing flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emcraig51](https://clawhub.ai/user/emcraig51)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to register or connect OpenMarlin accounts, submit execution and long-running task requests, and manage billing recovery from inside OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Platform API keys may be exposed through ordinary configuration or logged terminal output during bootstrap.

Mitigation: Use OpenClaw auth-profile storage for steady-state credentials and avoid running bootstrap in logged terminals unless the key will be rotated afterward.

Risk: Custom server URLs can send platform API keys to insufficiently constrained origins.

Mitigation: Use the default https://api.openmarlin.ai origin or only a trusted HTTPS deployment, and keep OPENMARLIN_SERVER_URL as a bare origin.

Risk: Custom --agent-id values may be unsafe until path validation is added.

Mitigation: Avoid custom --agent-id values and use the default OpenClaw agent profile unless the environment has reviewed the path behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emcraig51/skills/web-research-agent)
- [Publisher Profile](https://clawhub.ai/user/emcraig51)
- [OpenMarlin API Origin](https://api.openmarlin.ai)
- [OpenMarlin Website](https://openmarlin.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API responses, task status, billing summaries, and setup guidance from OpenMarlin helper scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
