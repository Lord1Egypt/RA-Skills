## Description:

Guides agents to use GLM text models through RunAPI with OpenAI-compatible Chat Completions and, where supported, other client protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure a RunAPI key, send GLM text chat or streaming requests, and verify responses and usage. Existing clients can consult the conditional guidance for compatible earlier models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests or credentials could be sent to the wrong API endpoint or reused across environments.

Mitigation: Use a RunAPI key with the disclosed RunAPI base URL; do not reuse unrelated production API keys in tests.

Risk: Unsupported protocol or input choices can cause rejected requests or misleading results.

Mitigation: Check the current RunAPI model contract before enabling extra capabilities; use text-only Chat Completions for glm-5.3 and avoid image, video, or file input for glm-5.3-flash.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/runapi-ai/skills/runapi-glm)
- [RunAPI GLM model page](https://runapi.ai/models/glm)
- [RunAPI GLM documentation](https://runapi.ai/models/glm.md)
- [RunAPI Z.AI provider documentation](https://runapi.ai/providers/z-ai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Compatibility protocols](references/compatibility-protocols.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers model and protocol selection, streaming completion checks, and returned usage.]

## Skill Version(s):

0.3.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
