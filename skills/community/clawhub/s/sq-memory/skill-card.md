## Description:

Enables OpenClaw agents to store, recall, update, list, and forget persistent hierarchical memories across sessions via the SQ protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbic16](https://clawhub.ai/user/wbic16)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use SQ Memory to give OpenClaw agents persistent text memory for user preferences, conversation summaries, project notes, and multi-agent coordination across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can expose or over-share stored agent data if users store secrets, regulated data, or full transcripts without consent and retention planning.

Mitigation: Review the data path before installation, avoid storing secrets or regulated data, and store full transcripts only with explicit user consent and a retention plan.

Risk: API keys or memory contents may be sent over plain HTTP when the skill is configured with a non-HTTPS endpoint.

Mitigation: Prefer HTTPS endpoints, never send API keys over plain HTTP, and pin the installer or Docker image used for deployment.

Risk: A self-hosted SQ endpoint can over-share memory across users or agents if exposed broadly or configured with shared scopes.

Mitigation: Bind self-hosted SQ to localhost or place it behind authenticated TLS, and use separate backend scopes or namespaces for separate users and agents.

## Reference(s):

- [SQ Memory on ClawHub](https://clawhub.ai/wbic16/skills/sq-memory)
- [Mirrorborn Help](https://mirrorborn.us/help.html)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain text and JSON-like tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory tools store and retrieve text by coordinate; delete operations return success or error status, and list operations return coordinate arrays.]

## Skill Version(s):

1.0.1 (source: server release, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
