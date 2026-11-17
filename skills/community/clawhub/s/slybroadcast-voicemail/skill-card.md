## Description:

Send Slybroadcast ringless voicemail campaigns from OpenClaw/LLMs using CLI or MCP, including AI voice generation (ElevenLabs or generic HTTP voice API) and campaign controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to configure and run Slybroadcast voicemail campaigns through CLI or MCP tools, including account recordings, public audio URLs, uploaded lists, and AI-generated voice recordings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables mass voicemail campaigns.

Mitigation: Use only for campaigns with lawful authority and recipient consent.

Risk: Campaign inputs may include phone numbers and message content.

Mitigation: Keep recipient data and message content minimal and handle them according to applicable privacy requirements.

Risk: The skill relies on API credentials for Slybroadcast and optional voice providers.

Mitigation: Store credentials in protected environment variables or a secrets manager.

Risk: Local or AI-generated audio may need to be staged at a public URL for Slybroadcast to fetch.

Mitigation: Use private, unguessable, short-lived staging URLs and delete staged audio promptly after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielfoch/skills/slybroadcast-voicemail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to call CLI or MCP tools that send, inspect, or control voicemail campaigns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
