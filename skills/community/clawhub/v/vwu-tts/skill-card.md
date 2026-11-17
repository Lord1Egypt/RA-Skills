## Description:

Helps an agent call vwu.ai speech models through an OpenAI-compatible chat completions endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill to configure a vwu.ai API key and send prompts to the supported speech-2.8-hd and speech-2.8-turbo models. It is intended for vwu.ai model access through the included shell helper and model list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell helper can send the user's API key and prompt to an unintended server if VWU_BASE_URL is changed.

Mitigation: Review the endpoint before running, keep VWU_BASE_URL unset or set only to the intended HTTPS vwu.ai endpoint, and avoid sending sensitive prompts until the destination is verified.

Risk: The helper constructs JSON in shell before calling the API.

Mitigation: Review prompt handling before use with untrusted input and prefer a proper JSON serializer for production workflows.

## Reference(s):

- [vwu.ai](https://vwu.ai)
- [ClawHub skill page](https://clawhub.ai/a3273283/skills/vwu-tts)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VWU_API_KEY; sends prompts and API keys to the configured vwu.ai endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
