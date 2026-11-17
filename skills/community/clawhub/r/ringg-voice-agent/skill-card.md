## Description:

Integrate Ringg AI voice agents with OpenClaw for making, receiving, and managing phone calls powered by Ringg's Voice OS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siddharthpilani](https://clawhub.ai/user/siddharthpilani)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect OpenClaw agents to Ringg AI for outbound calls, campaigns, call status, call history, analytics, assistants, and transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real outbound calls and campaign launches.

Mitigation: Require explicit approval before every outbound call or campaign launch, and verify recipient consent and legal compliance before use.

Risk: The skill uses a Ringg API key and workspace configuration.

Mitigation: Protect the API key, use only a Ringg workspace the operator controls, and minimize dynamic variables and contact fields.

Risk: Webhook-driven events may expose transcripts, summaries, or trigger agent actions.

Mitigation: Do not expose webhook endpoints publicly unless signed webhook verification, replay protection, strict event allowlists, and safe handling of transcripts and summaries are enforced.

## Reference(s):

- [Ringg Voice Agent Skill](https://clawhub.ai/siddharthpilani/skills/ringg-voice-agent)
- [Ringg AI](https://www.ringg.ai)
- [Ringg AI API Docs](https://docs.ringg.ai)
- [Ringg AI API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Ringg API requests for calls, campaigns, assistants, analytics, transcripts, and webhook setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
