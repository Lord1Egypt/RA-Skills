## Description:

TradingBot helps download, update, build, start, and check paoosi/tradingbot for local demo-mode evaluation of a grid-trading bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frederica123](https://clawhub.ai/user/frederica123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically capable users use this skill to install and run paoosi/tradingbot on macOS or Linux, validate the local management UI and health endpoint, and keep first use in mock/demo mode without configuring real trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow downloads and builds mutable upstream GitHub code and npm/Go dependencies.

Mitigation: Review or pin a trusted upstream commit before installation and run the build only with user-account permissions you are comfortable granting.

Risk: The started management service may be reachable beyond the local machine if the host or network exposes its port.

Mitigation: Keep the system firewall enabled, avoid public port forwarding, and use the local URL for access.

Risk: Trading workflows can move beyond demo mode into live exchange configuration.

Mitigation: Do not add live exchange credentials or start real strategies unless that risk is explicitly understood and accepted.

## Reference(s):

- [TradingBot upstream repository](https://github.com/paoosi/tradingbot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports install directory, Git commit, local port, health-check result, and stop instructions without exposing local secret values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
