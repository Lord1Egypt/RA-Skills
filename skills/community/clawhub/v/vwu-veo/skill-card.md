## Description:

Calls vwu.ai Veo model identifiers through an OpenAI-compatible chat completions interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to invoke vwu.ai Veo models after configuring a VWU_API_KEY. It is useful for sending prompts to the listed model IDs through a simple command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send the user's API key and prompt to an endpoint controlled by the VWU_BASE_URL environment variable.

Mitigation: Use the skill only where VWU_BASE_URL cannot be set by untrusted shell profiles, wrappers, CI variables, or other users; prefer a pinned HTTPS API host.

Risk: Sensitive prompts may be transmitted to the configured vwu.ai-compatible endpoint.

Mitigation: Avoid sending secrets or sensitive data unless the destination and account controls are trusted.

Risk: The helper builds JSON request bodies in shell, which can be fragile for prompts containing special characters.

Mitigation: Review generated commands before use and prefer a proper JSON encoder such as jq when maintaining or extending the script.

## Reference(s):

- [vwu.ai](https://vwu.ai)
- [ClawHub skill page](https://clawhub.ai/a3273283/skills/vwu-veo)
- [Publisher profile](https://clawhub.ai/user/a3273283)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text model responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VWU_API_KEY; accepts a model identifier and prompt; depends on curl and jq in the provided helper script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
