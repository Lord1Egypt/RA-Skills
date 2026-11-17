## Description:

Routes natural-language trading and account requests to exact `zerodha` CLI commands with validation for orders, quotes, positions, holdings, margins, authentication, configuration, GTT, and mutual fund flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jatinbansal1998](https://clawhub.ai/user/jatinbansal1998)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to convert plain-English Zerodha trading and account requests into exact CLI commands. It helps route market data, portfolio, authentication, configuration, order, GTT, margin, and mutual fund tasks while asking for missing required inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands pipe remote GitHub content directly into a shell.

Mitigation: Review the installer source first and prefer a pinned release with checksum or signature verification.

Risk: Authentication flows may expose Zerodha API keys, API secrets, request tokens, or refresh tokens in chat or shell history.

Mitigation: Use safer credential prompts or environment-specific secret storage, and rotate credentials if they were exposed.

Risk: Generated order, cancel, exit, revoke, delete, and SIP/MF commands can trigger live financial actions.

Mitigation: Manually verify every generated command and all order parameters before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jatinbansal1998/skills/zerodha-kite)
- [Linux/macOS installer script referenced by skill](https://raw.githubusercontent.com/jatinbansal1998/zerodha-kite-cli/main/scripts/install.sh)
- [Windows installer script referenced by skill](https://raw.githubusercontent.com/jatinbansal1998/zerodha-kite-cli/main/scripts/install.ps1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown with command, why, and missing fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs one routed command or asks for missing required inputs; installer commands may be returned for setup requests.]

## Skill Version(s):

v1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
