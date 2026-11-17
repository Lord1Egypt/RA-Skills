## Description:

Guides developers in calling MiMo models through RunAPI for text generation, tool use, streaming, and supported compatibility clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure RunAPI access and integrate MiMo text generation, custom tool calling, streaming, and supported client protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, public image URLs, tool results, and optional metadata may be sent to the third-party RunAPI service.

Mitigation: Use only for approved provider paths and avoid secrets or regulated data unless your organization has approved that data flow.

Risk: A RunAPI API key is needed for requests and may be exposed if embedded in code or shared output.

Mitigation: Use a scoped key stored in the environment or a secret manager, not in source code.

## Reference(s):

- [RunAPI MiMo model overview](https://runapi.ai/models/mimo)
- [RunAPI MiMo documentation](https://runapi.ai/models/mimo.md)
- [RunAPI Xiaomi provider page](https://runapi.ai/providers/xiaomi.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [MiMo compatibility protocols](references/compatibility-protocols.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes model-specific request boundaries and response verification guidance.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
