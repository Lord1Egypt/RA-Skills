## Description:

tradr manages onchain trade execution after receiving a contract address and score, including position sizing, Bankr-based entry, mode-based exits, verification, and trade logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riskanon](https://clawhub.ai/user/riskanon)

### License/Terms of Use:


## Use Case:

External developers and trading operators use this skill to connect scored token signals to an automated Bankr-backed trade lifecycle with entry guards, exit modes, monitoring, and logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated trading can place real-money Bankr trades from supplied signals.

Mitigation: Review the configuration before use, test with tiny limits or dry-run behavior, and only fund wallets after entry and exit behavior has been validated.

Risk: Default persistence and setup can create an over-privileged long-running service.

Mitigation: Run the exit manager as a user service or under a dedicated unprivileged account, and avoid sudo or system-wide setup unless explicitly reviewed.

Risk: Weak input boundaries can allow untrusted or malformed signal sources to trigger trades.

Mitigation: Validate contract addresses, score ranges, chain values, and token metadata, and require authentication for webhook or adapter inputs.

Risk: Dashboard and configuration exposure can reveal sensitive wallet, trading, or notification details.

Mitigation: Keep the dashboard local or authenticated, avoid exposing full config.json, and restrict file and endpoint access.

Risk: Telegram notification broadcasts can leak trade activity or credentials if configured unsafely.

Mitigation: Disable Telegram broadcasts until reviewed, store tokens securely, and route only intended notification content to external channels.

## Reference(s):

- [tradr ClawHub skill page](https://clawhub.ai/riskanon/skills/tradr)
- [Publisher profile](https://clawhub.ai/user/riskanon)
- [Signal adapter guide](adapters/README.md)
- [Bankr](https://bankr.bot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and local runtime files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing setup and operation guidance for a local trading workflow that depends on Bankr, jq, Python, wallet configuration, and optional dashboard endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
