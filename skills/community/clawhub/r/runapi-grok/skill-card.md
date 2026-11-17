## Description:

Guides agents in calling Grok text models through RunAPI using supported API protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure RunAPI access, select a supported Grok model and protocol, and verify text responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and other data sent through RunAPI may not meet an organization's data-handling requirements.

Mitigation: Check RunAPI account and data-handling requirements before sending sensitive content.

Risk: Misconfigured API credentials or endpoint can route requests incorrectly or expose a key.

Mitigation: Set the RunAPI key and base URL deliberately, and keep the key out of shared code and logs.

## Reference(s):

- [Grok on RunAPI documentation](https://runapi.ai/models/grok.md)
- [RunAPI Grok model page](https://runapi.ai/models/grok)
- [RunAPI xAI provider documentation](https://runapi.ai/providers/xai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Compatibility protocols](references/compatibility-protocols.md)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration instructions]

**Output Format:** [Text or Markdown with optional code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streaming responses and usage details where supported]

## Skill Version(s):

0.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
