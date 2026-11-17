## Description:

Access and use the sora-2 model on the vwu.ai platform through an OpenAI-compatible chat completions API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can configure a vwu.ai API key and call the sora-2 model from an agent workflow or shell command. The skill is useful when an OpenAI-compatible chat completions interface is needed for vwu.ai-hosted Sora model access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's API key and prompts to vwu.ai or to a custom VWU_BASE_URL endpoint.

Mitigation: Install only if comfortable using vwu.ai for these prompts, avoid putting secrets in prompts, and set VWU_BASE_URL only to an endpoint you trust.

Risk: The shell wrapper builds JSON request payloads directly from user input.

Mitigation: Review inputs before use and prefer a safer version that constructs JSON with a proper encoder such as jq.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/a3273283/skills/vwu-sora)
- [vwu.ai](https://vwu.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VWU_API_KEY; supports VWU_BASE_URL override for trusted endpoints.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
