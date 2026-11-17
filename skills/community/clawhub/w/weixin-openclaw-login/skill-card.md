## Description:

Helps agents install and troubleshoot Weixin personal-account login for OpenClaw, including QR authorization links, scan status polling, and local token state checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqhi](https://clawhub.ai/user/aqhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect a Weixin personal account to OpenClaw and diagnose QR login, scan confirmation, and local token persistence issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can print bot login tokens and related account identifiers in terminal output.

Mitigation: Redact bot_token values, account identifiers, polling output, terminal logs, and account files before sharing them.

Risk: The install flow runs an unpinned Tencent Weixin OpenClaw package installer.

Mitigation: Review the package before installing and prefer a pinned, reviewed installer version when available.

Risk: The skill interacts with Weixin login state through Tencent Weixin OpenClaw endpoints.

Mitigation: Use it only when the Tencent Weixin OpenClaw package is trusted and the user is comfortable granting access to the relevant Weixin login state.

## Reference(s):

- [Implementation Notes](references/implementation-notes.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with inline shell commands and script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include QR authorization URLs, login status JSON, and local OpenClaw state file paths.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
