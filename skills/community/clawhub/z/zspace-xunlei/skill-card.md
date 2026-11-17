## Description:

Uses OpenClaw browser automation to create a Xunlei download task in ZSpace from a trusted magnet link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengzhxyz](https://clawhub.ai/user/pengzhxyz)

### License/Terms of Use:

MIT-0

## Use Case:

External users who manage downloads through ZSpace use this skill to add a trusted magnet link to Xunlei in an authenticated ZSpace browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command can pass magnet-link input through a shell command unsafely.

Mitigation: Validate that the input is a trusted magnet URL and avoid shell interpolation when adapting or executing the command.

Risk: The skill creates real download tasks in a logged-in ZSpace account.

Mitigation: Ask for user confirmation before creating the download task and verify the resulting task in the browser after execution.

## Reference(s):

- [ZSpace web portal](https://www.zconnect.cn)
- [ClawHub skill page](https://clawhub.ai/pengzhxyz/skills/zspace-xunlei)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw binary and an authenticated ZSpace browser session.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
