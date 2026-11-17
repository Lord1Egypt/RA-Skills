## Description:

Call MiniMax Hailuo models on vwu.ai through an OpenAI-compatible chat completions wrapper using a configured API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to send prompts to MiniMax Hailuo models hosted on vwu.ai from a shell-based chat wrapper. It is useful for quick OpenAI-compatible chat completion calls when a vwu.ai API key and model name are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts and a vwu.ai API key to an undocumented endpoint controlled by VWU_BASE_URL.

Mitigation: Use only a trusted HTTPS vwu.ai endpoint, keep VWU_BASE_URL unset unless explicitly needed, and avoid regulated or sensitive prompt data.

Risk: Prompt and model values are passed into request JSON by the shell wrapper.

Mitigation: Review or harden the script to JSON-encode prompt and model values before broad or automated use.

## Reference(s):

- [vwu.ai](https://vwu.ai)
- [ClawHub skill page](https://clawhub.ai/a3273283/skills/vwu-minimax)
- [Publisher profile](https://clawhub.ai/user/a3273283)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain text model responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VWU_API_KEY; VWU_BASE_URL can redirect API calls if set.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
