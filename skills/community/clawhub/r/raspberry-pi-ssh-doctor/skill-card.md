## Description:

Diagnose Raspberry Pi SSH resolution, timeout, refusal, host-key, and authentication failures using real OpenSSH or JishuBuddy evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to classify Raspberry Pi SSH failures from real OpenSSH or JishuBuddy output and choose the smallest supported recovery step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm installation can modify the operator computer and should not be treated as SSH troubleshooting consent.

Mitigation: Review the displayed package version, registry, global prefix, and exact install command, then install only after explicit approval.

Risk: JishuBuddy TUI and AG-UI Server send disclosed activation and heartbeat telemetry by default.

Mitigation: Set JISHUBUDDY_TELEMETRY_DISABLED=true before launch when telemetry is not desired.

Risk: SSH diagnostics can expose private keys, passwords, passphrases, hostnames, usernames, IP addresses, or local key paths.

Mitigation: Do not provide secrets, and sanitize SSH output before sharing it publicly.

Risk: Incorrect host-key handling can hide device replacement, reimage, DNS error, or interception events.

Mitigation: Verify host-key fingerprints through a trusted channel and do not automatically replace or bypass host-key checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bowen-aijishu/skills/raspberry-pi-ssh-doctor)
- [Project homepage](https://github.com/x-aijishu/jishubuddy-skills/tree/main/raspberry-pi-ssh-doctor)
- [JishuBuddy npm package](https://www.npmjs.com/package/jishubuddy)
- [Installation helper](scripts/install-jishubuddy.sh)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an observed error classification, supporting evidence, and a minimal next step; may propose permissioned installation or SSH configuration checks.]

## Skill Version(s):

1.0.1 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
