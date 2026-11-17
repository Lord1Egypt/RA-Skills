## Description:

Live rate-limit awareness for Claude.ai (Max/Pro) and OpenAI (Plus/Pro/Codex).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgj](https://clawhub.ai/user/wgj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use RedLine to check Claude.ai and OpenAI/Codex usage budgets and apply pacing tiers so agents conserve work as subscription limits are approached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release documentation describes scripts that read OAuth tokens, but those scripts are not included in the reviewed artifact.

Mitigation: Install only a reviewed release that includes the referenced scripts or provides verifiable signed source, and confirm token redaction and endpoint restrictions before use.

Risk: Replacement or unofficial usage-checker scripts could misuse Claude or OpenAI OAuth tokens.

Mitigation: Do not provide OAuth tokens to replacement scripts or copied code from unofficial sources.

## Reference(s):

- [RedLine ClawHub page](https://clawhub.ai/wgj/skills/redline)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON usage output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes pacing tiers and usage-checker command outputs for Claude.ai and OpenAI/Codex plans.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
