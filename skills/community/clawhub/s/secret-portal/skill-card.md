## Description:

Spin up a one-time web UI for securely entering secret keys and env vars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awlevin](https://clawhub.ai/user/awlevin)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to collect API keys or environment variables through a temporary portal instead of placing secret values in chat history or terminal logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned external package code while handling API keys.

Mitigation: Pin and review the package version before use, and avoid production secrets until the executable code has been audited.

Risk: The cloudflared tunnel binary may be downloaded at runtime.

Mitigation: Verify cloudflared from an official source before use, or provide a pre-reviewed binary in the execution environment.

Risk: Secrets are written to an env file selected by the user or agent.

Mitigation: Use the narrowest env-file path needed, confirm file permissions, and avoid broad shared locations.

## Reference(s):

- [Secret Portal on ClawHub](https://clawhub.ai/awlevin/skills/secret-portal)
- [Publisher profile: awlevin](https://clawhub.ai/user/awlevin)
- [Artifact-listed GitHub URL](https://github.com/Olafs-World/secret-portal)
- [OpenAI API Keys](https://platform.openai.com/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI flags for key name, env-file path, instructions, link text, tunnel provider, port, and timeout.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
