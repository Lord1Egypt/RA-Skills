## Description:

Multi-exchange perpetuals trading CLI for 15+ venues via the TTC Box API, supporting market data, order placement, position management, TWAP/DCA workflows, technical signal scans, and trailing-stop loops through bundled darwin-arm64 and linux-x64 binaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tetrac-official](https://clawhub.ai/user/tetrac-official)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to let an OpenClaw agent inspect perpetuals markets, manage exchange account state, and prepare or execute trading workflows with explicit checks before mutating orders or positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact financial actions including order placement, position closure, and leverage changes.

Mitigation: Use dry-run previews, require explicit user confirmation for real orders, and verify balance, positions, and open orders before any trading action.

Risk: Reusable TTC Box and exchange credentials are required, and over-permissioned exchange keys can increase account impact.

Mitigation: Use trade-only exchange API keys with withdrawals disabled, store secrets only in the environment, and avoid exposing .env contents during troubleshooting.

Risk: Failed or ambiguous write operations can create duplicate exposure if retried blindly.

Mitigation: After any in-flight write failure, re-check positions, open orders, and balances before deciding whether a single retry is appropriate.

Risk: The release evidence classifies the skill as a high-impact financial integration with a suspicious security verdict.

Mitigation: Install only after reviewing the security guidance and trusting TTC Box with the required credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tetrac-official/skills/tetrac-perp-trader)
- [Project Homepage](https://github.com/tetrac-official/tetrac-perp-trader)
- [TTC Box REST API](references/api-reference.md)
- [Supported Exchanges](references/exchanges.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured CLI output references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output may be table, JSON, CSV, or quiet mode depending on skill configuration.]

## Skill Version(s):

0.1.5 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
