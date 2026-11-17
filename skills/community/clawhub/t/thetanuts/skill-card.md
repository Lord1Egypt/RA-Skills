## Description:

Trade crypto options on Thetanuts Finance with orderbook fills, RFQ lifecycle support, multi-strike structures, real-time market data, wallet management, early settlement, and referrer fees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goheesheng](https://clawhub.ai/user/goheesheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to explore Thetanuts Finance crypto options markets, manage a local wallet, inspect balances and positions, build RFQs, prepare approvals, and execute supported orderbook or RFQ trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet seeds and can prepare or run transaction-signing flows.

Mitigation: Use only a dedicated low-value wallet, treat the local .env seed as highly sensitive, and review transaction details before signing or broadcasting.

Risk: The updater can change code that signs transactions.

Mitigation: Run updates only after explicit user consent and verify the update source and changes before applying them.

Risk: Token approvals may allow contracts to spend more funds than the immediate trade requires.

Mitigation: Prefer exact approval amounts, verify spender addresses, and review approvals carefully before confirming.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/goheesheng/skills/thetanuts)
- [Thetanuts Finance](https://thetanuts.finance)
- [Thetanuts SDK](https://github.com/Thetanuts-Finance/thetanuts-sdk)
- [Thetanuts OpenClaw Repository](https://github.com/Thetanuts-Finance/thetanuts-openclaw)
- [Tether WDK](https://docs.wdk.tether.io)
- [OpenClaw Docs](https://docs.openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide wallet, approval, RFQ, and trade execution flows; transaction-related actions require user review and explicit confirmation.]

## Skill Version(s):

1.5.4 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
