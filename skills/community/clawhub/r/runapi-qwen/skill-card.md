## Description:

Guides developers in calling Qwen models through RunAPI for text, image understanding, and streaming, with compatibility guidance for existing clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure RunAPI credentials and make Qwen text or image requests through OpenAI-compatible Chat Completions. It also guides compatible text-only clients using other supported protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A misconfigured endpoint or exposed credential could send the RunAPI key to an unintended service.

Mitigation: Use a RunAPI-scoped key and confirm OPENAI_BASE_URL is https://runapi.ai/v1.

Risk: Requests send user-provided text or images to an external model provider.

Mitigation: Avoid sending information you would not share with that provider.

## Reference(s):

- [Qwen on RunAPI](https://runapi.ai/models/qwen)
- [Qwen model documentation](https://runapi.ai/models/qwen.md)
- [Alibaba provider documentation](https://runapi.ai/providers/alibaba.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Qwen compatibility protocols](artifact/references/compatibility-protocols.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response completion and usage checks for supported protocols.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
