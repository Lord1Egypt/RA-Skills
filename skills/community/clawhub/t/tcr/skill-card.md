## Description:

Run OpenClaw on tcr, a local proxy that pools your own Claude and ChatGPT subscriptions: check the pool, start the Gateway on it, and confirm turns go through it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhkts1](https://clawhub.ai/user/dhkts1)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers can use this skill to check their own tcr account pool, configure OpenClaw, and run and verify the Gateway through the local proxy using their own Claude and ChatGPT subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: tcr can read pooled Claude and ChatGPT prompts and replies, and its local files include account tokens and operational logs.

Mitigation: Use tcr only if you trust it with these credentials and conversations; protect its configuration and logs, verify release checksums, and review requested configuration or startup approvals.

## Reference(s):

- [tcr OpenClaw documentation](https://github.com/dhkts1/tcr/blob/main/docs/openclaw.md)
- [tcr project repository](https://github.com/dhkts1/tcr)
- [tcr website](https://dhkts1.github.io/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tcr and openclaw on macOS or Linux.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
