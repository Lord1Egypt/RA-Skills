## Description:

Guides developers through securely adding API keys, web search, voice, AI providers, and rate limiting to Shipyard apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipposk](https://clawhub.ai/user/philipposk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure third-party API integrations in a Shipyard app, manage credentials, and add safeguards for cost, abuse, and privacy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on helper scripts supplied with the full Shipyard plugin and may not work as a standalone installation.

Mitigation: Install the full Shipyard plugin before using the skill.

Risk: API credentials, paid provider calls, or cached responses can expose private data or create unexpected costs.

Mitigation: Keep keys out of chat, grant only necessary keys, set spending caps, disclose external providers, and isolate private cache entries by user.

## Reference(s):

- [API key setup and safeguards](references/api-keys.md)
- [Web search integration](references/web-search.md)
- [Voice integration](references/voice.md)
- [AI provider and model routing](references/ai-router.md)
- [Rate limits and caching](references/rate-limit.md)
- [Shipyard installation guide](https://github.com/philipposk/shipyard/blob/main/INSTALL.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, Code]

**Output Format:** [Markdown guidance with shell commands and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some integrations are identified in the references as new and untested in production.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
