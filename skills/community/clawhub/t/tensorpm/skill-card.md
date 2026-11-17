## Description:

TensorPM provides AI-powered project management with local-first project tracking, action item management, MCP tools, and A2A agent communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo552](https://clawhub.ai/user/neo552)

### License/Terms of Use:


## Use Case:

Developers, agents, and project teams use this skill to connect an AI client to TensorPM for project management, action item tracking, provider key setup, and coordination through MCP tools or local A2A endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local A2A API can read and change project data when exposed without authentication.

Mitigation: Enable A2A_HTTP_AUTH_TOKEN before using A2A and run TensorPM only on trusted local machines.

Risk: The skill directs users to install external TensorPM application binaries.

Mitigation: Install only from trusted TensorPM publisher and release channels.

Risk: The integration can store provider API keys through TensorPM.

Mitigation: Use trusted AI clients, store only intended provider keys, and rotate keys if the local system may be compromised.

## Reference(s):

- [TensorPM homepage](https://tensorpm.com)
- [TensorPM ClawHub skill page](https://clawhub.ai/neo552/skills/tensorpm)
- [TensorPM release notes](https://github.com/Neo552/TensorPM-Releases/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the TensorPM desktop app to be running; A2A can be protected with A2A_HTTP_AUTH_TOKEN.]

## Skill Version(s):

1.1.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
