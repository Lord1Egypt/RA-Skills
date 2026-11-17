## Description:

Search and execute dynamic tools via the QVeris API for weather, search, finance, geolocation, AIGC, news, social media, health data, and other API-backed tasks; requires QVERIS_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris7iu](https://clawhub.ai/user/chris7iu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to discover QVeris-hosted API tools by capability and execute selected tools with parameters from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send user requests and tool parameters to a broad external QVeris tool-execution service.

Mitigation: Review the skill before installation, disable or gate automatic use where supported, and confirm each discovered tool before execution.

Risk: QVeris tool calls may expose secrets or sensitive personal or regulated data if those values are passed as parameters.

Mitigation: Use a scoped, revocable QVeris API key and avoid passing secrets or sensitive personal or regulated data to tool parameters.

Risk: Unpinned installation through npx may fetch code outside the server-reviewed ClawHub artifact.

Mitigation: Prefer the ClawHub install path or a manually reviewed, pinned artifact before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris7iu/skills/qverisai)
- [QVeris](https://qveris.ai)
- [QVeris API endpoint](https://qveris.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QVERIS_API_KEY; search and execution calls use configurable timeouts and response-size limits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
