## Description:

Enables AI agents to generate images using the Character Select Stand Alone App (SAA) image generation backend via command-line interface, and to polish prompts via the AI Prompt panel APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirabarukaso](https://clawhub.ai/user/mirabarukaso)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agents use this skill to send image-generation requests to a configured SAA backend and, when requested, turn a brief into a polished prompt before generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current WebSocket connection does not verify the server's identity when credentials are sent over a network.

Mitigation: Require certificate verification and fix the connection checks before using credentials across a network.

Risk: Verbose logs can expose session tokens and provider keys.

Mitigation: Avoid verbose mode with real credentials and redact secrets from logs.

Risk: Prompt briefs may be sent to the configured external AI provider.

Mitigation: Confirm the provider is trusted before sending confidential briefs, or use a trusted Local backend.

Risk: Force-unlocking may disrupt another active generation job.

Mitigation: Use force-unlock only after confirming that no other job is running.

## Reference(s):

- [SAA Agent on ClawHub](https://clawhub.ai/mirabarukaso/skills/saa-agent)
- [SAA project repository (linked in artifact documentation)](https://github.com/mirabarukaso/character_select_stand_alone_app)

## Skill Output:

**Output Type(s):** [Files (generated images), Text (polished prompts), Shell commands]

**Output Format:** [Image files (PNG by default), plain text, and command-line arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Images are saved to a file by default; base64 image output is optional.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata; artifact README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
