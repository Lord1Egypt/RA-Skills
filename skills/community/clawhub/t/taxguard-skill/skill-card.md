## Description:

TaxGuard monitors proposed trades for tax and trading-rule risks, supports opt-in Guardian Mode blocking, and produces daily tax summaries for trading agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronahadi23](https://clawhub.ai/user/aaronahadi23)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and developers use this skill to have trading agents check proposed trades against tax, wash-sale, pattern day trader, holding-period, and tax-loss harvesting risks. The skill can log checks, produce daily or on-demand reports, and ask for confirmation before trades only when the user enables Guardian Mode.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill sends trade details, positions, account equity, tax context, strategy details, and an email address to Rhetra's remote API.

Mitigation: Use only with explicit user approval, minimize submitted fields where possible, and define retention and account-coverage rules before enabling monitoring.

Risk: API keys or sensitive financial data could be exposed through command-line arguments or logs.

Mitigation: Store credentials in environment variables or a secret manager, avoid passing production keys in visible commands, and review local logs before sharing them.

Risk: Silent monitoring can create a broad audit trail across connected trading accounts.

Mitigation: Keep monitoring scope explicit, document which accounts are covered, and review daily reports before relying on them for tax or trading decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaronahadi23/skills/taxguard-skill)
- [Publisher Profile](https://clawhub.ai/user/aaronahadi23)
- [Rhetra](https://rhetra.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, command-line output, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trade checks can return allowed, blocked, or error status through command output and exit codes; daily reports summarize accumulated checks.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
