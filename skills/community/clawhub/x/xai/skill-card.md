## Description:

Chat with Grok models via xAI API. Supports Grok-4, Grok-4.20, Grok-3, Grok-3-mini, vision, and real-time X search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvanhorn](https://clawhub.ai/user/mvanhorn)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to route chat, vision, model-listing, and real-time X search requests through xAI Grok models from an OpenClaw-compatible agent environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, X search queries, and images provided with --image are sent to xAI API services.

Mitigation: Invoke the skill only for requests that should be handled by xAI, avoid sensitive inputs, and review xAI data handling requirements before use.

Risk: The skill can use either XAI_API_KEY or an existing ~/.clawdbot/clawdbot.json xAI API key.

Mitigation: Prefer setting XAI_API_KEY explicitly in the intended runtime environment and verify which credential source is active before execution.

Risk: Broad triggers such as grok, xai, and ask grok can route requests to this third-party model provider.

Mitigation: Use the skill only when the user intentionally requests Grok or xAI handling.

## Reference(s):

- [xAI documentation](https://docs.x.ai)
- [xAI API documentation](https://docs.x.ai/api)
- [xAI](https://x.ai)
- [ClawHub skill page](https://clawhub.ai/mvanhorn/skills/xai)
- [Publisher profile](https://clawhub.ai/user/mvanhorn)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown or terminal text, with optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include streamed text, X post citations, model listings, and raw JSON when requested.]

## Skill Version(s):

1.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
