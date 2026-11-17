## Description:

This skill helps agents call five Gemini-family models on vwu.ai through an OpenAI-compatible chat completions interface after the user configures a vwu.ai API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send prompts to selected vwu.ai Gemini models and receive chat responses through a shell-based OpenAI-compatible workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's API key and prompt to an endpoint named by VWU_BASE_URL.

Mitigation: Use it only in trusted environments, keep VWU_BASE_URL unset or pinned to https://vwu.ai, and avoid putting secrets in prompts.

Risk: The shell client may reveal the API key prefix when reporting quota-related errors.

Mitigation: Remove or suppress API-key-prefix logging before routine or shared use.

## Reference(s):

- [vwu.ai](https://vwu.ai)
- [ClawHub skill listing](https://clawhub.ai/a3273283/skills/vwu-gemini)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text responses with shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VWU_API_KEY; optional VWU_BASE_URL controls the endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
