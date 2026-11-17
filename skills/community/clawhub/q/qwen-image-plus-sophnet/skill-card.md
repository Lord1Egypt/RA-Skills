## Description:

Generate images via Sophnet Qwen-Image-Plus and poll for task completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duffycoder](https://clawhub.ai/user/duffycoder)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create Sophnet Qwen-Image-Plus image-generation tasks, poll until completion, and return resulting image URLs to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A timing option input-validation flaw can allow local command execution.

Mitigation: Review before installing, use trusted prompt and option values, and require numeric validation for --max-wait and --poll-interval before use.

Risk: API key exposure or excess privilege could affect Sophnet account usage.

Mitigation: Prefer SOPHNET_API_KEY over command-line --api-key and use a scoped Sophnet token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duffycoder/skills/qwen-image-plus-sophnet)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text with shell command examples and IMAGE_URL lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Sophnet API key; emits TASK_ID, STATUS, and one or more IMAGE_URL values.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
