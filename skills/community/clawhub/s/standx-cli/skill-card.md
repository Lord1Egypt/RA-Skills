## Description:

StandX CLI helps agents use the StandX exchange command-line tool for crypto market data, account queries, order management, real-time streams, leverage, and margin settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjllance](https://clawhub.ai/user/wjllance)

### License/Terms of Use:

MIT

## Use Case:

External developers and traders use this skill to guide an agent in installing, configuring, and operating the StandX CLI for market-data queries, account checks, order management, WebSocket streams, and leverage or margin commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release can install an unverified trading binary with elevated privileges.

Mitigation: Prefer Homebrew or another verified release path, and avoid direct sudo curl/tar installation unless the binary is independently verified.

Risk: JWT tokens and private keys can expose account data or enable trading operations if printed, logged, or stored carelessly.

Mitigation: Keep private keys out of shell startup files and logs, rotate short-lived tokens, restrict credential-file permissions, and never pass secrets on command lines.

Risk: Order, cancel-all, leverage, and margin commands can change real trading positions.

Mitigation: Require explicit confirmation before trading or risk-setting commands, and use dry-run previews before executing state-changing operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wjllance/skills/standx-cli)
- [Publisher Profile](https://clawhub.ai/user/wjllance)
- [StandX CLI API Documentation](references/api-docs.md)
- [StandX CLI Command Examples](references/examples.md)
- [StandX CLI Troubleshooting](references/troubleshooting.md)
- [StandX CLI GitHub Repository](https://github.com/wjllance/standx-cli)
- [StandX CLI Documentation](https://github.com/wjllance/standx-cli/tree/main/docs)
- [StandX Credential Session](https://standx.com/user/session)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and references to JSON, CSV, table, or quiet CLI output modes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require the standx binary, STANDX_JWT for authenticated reads, and STANDX_PRIVATE_KEY for trading operations.]

## Skill Version(s):

0.5.0 (source: ClawHub release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
