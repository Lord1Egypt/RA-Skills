## Description:

OpenClaw homepage plugin that lets visitors chat with an AI assistant on a personal homepage, with concurrent visitor support and session-scoped context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaoyi001](https://clawhub.ai/user/yaoyi001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site owners use this skill to run an OpenClaw-backed homepage chat service for visitors. It provides setup, lifecycle scripts, an HTTP chat endpoint, and per-session conversation history for a personal homepage assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a networked homepage chat service where weak or missing authentication could allow unintended use.

Mitigation: Require authentication on every non-health endpoint and deploy behind a protected reverse proxy or restricted bind address.

Risk: Gateway credentials and chat metadata may be exposed through query strings, logs, or overly broad file permissions.

Mitigation: Avoid credentials in URLs, stop logging tokens, and enforce 0600/0700 permissions for configuration, data, and log files.

Risk: User-controlled session IDs and retained conversation history can create session integrity and privacy risks.

Mitigation: Validate or server-generate session IDs, disclose retention and Gateway forwarding, and bound stored conversation history.

Risk: Unpinned runtime dependencies and direct service startup can make deployments harder to review and reproduce.

Mitigation: Pin dependencies in an isolated environment and review the lifecycle scripts before installing or starting the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yaoyi001/skills/skill-fixon-homepage)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill runs a local HTTP chat bridge and writes configuration, logs, and per-session JSON history under ~/.openclaw/homepage.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
