## Description:

Access seven Kling models on vwu.ai through an OpenAI-compatible chat completions shell helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call vwu.ai Kling models for chat completion requests with a configured VWU_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the VWU_API_KEY bearer token can be sent to another host if VWU_BASE_URL is changed.

Mitigation: Keep VWU_BASE_URL at the default vwu.ai endpoint unless the replacement endpoint is fully trusted, and rotate the API key if it may have been used with an untrusted endpoint.

Risk: The security verdict is suspicious because the endpoint override behavior can redirect sensitive requests.

Mitigation: Review before installing, use a scoped and revocable API key, and deploy only where sending prompts to vwu.ai is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a3273283/skills/vwu-kling)
- [Publisher profile](https://clawhub.ai/user/a3273283)
- [vwu.ai](https://vwu.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VWU_API_KEY; supports an optional VWU_BASE_URL endpoint override.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
