## Description:

Calls GPT-4 and GPT-5 family chat models through the vwu.ai platform using an OpenAI-compatible chat completions interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and invoke vwu.ai-hosted OpenAI-compatible chat models from a shell workflow. It is useful for selecting supported GPT-4 and GPT-5 model names, setting the required API key, and submitting prompts through the included chat helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An endpoint override could send prompts and the API key to an unintended remote service.

Mitigation: Leave VWU_BASE_URL unset or pin it to a trusted HTTPS endpoint before use.

Risk: Prompts are sent to a remote provider and may contain sensitive data.

Mitigation: Avoid putting secrets or confidential information in prompts.

Risk: The security verdict requires review before use.

Mitigation: Install only after trusting vwu.ai and confirming the execution environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a3273283/skills/vwu-openai)
- [vwu.ai](https://vwu.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VWU_API_KEY; VWU_BASE_URL should remain unset or pinned to a trusted HTTPS endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
