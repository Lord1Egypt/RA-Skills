## Description:

Real-time whale activity monitoring and smart money following for Base blockchain. Track large transactions, wallet accumulation patterns, and smart money flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supah-based](https://clawhub.ai/user/supah-based)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to query SUPAH's Base-chain whale analytics, including recent large transfers, token or wallet tracking, historical patterns, and smart-money flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic x402 USDC payments may be triggered by API calls.

Mitigation: Use an agent or wallet policy that requires confirmation or enforces a low spending cap before paid calls are made.

Risk: Wallet, token, or query details may be sent to the configured API host.

Mitigation: Leave SUPAH_API_BASE unset or set it only to a trusted HTTPS endpoint, and avoid submitting sensitive wallet-monitoring requests.

Risk: Crypto analytics can be incomplete, stale, or unsuitable as trading advice.

Mitigation: Treat outputs as informational signals and verify material decisions against independent data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supah-based/skills/supah-whale-tracker)
- [SUPAH API](https://api.supah.ai)
- [x402 protocol](https://www.x402.org)
- [SUPAH website](https://supah.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [CLI text and JSON API responses surfaced through agent conversation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, curl, outbound access to the configured SUPAH API host, and x402-compatible USDC payment handling on Base.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
