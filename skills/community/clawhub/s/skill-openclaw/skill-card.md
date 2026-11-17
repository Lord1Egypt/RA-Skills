## Description:

Gives OpenClaw agents stablecoin payment, spending policy, and compliance capabilities through Oris.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fluxaventures](https://clawhub.ai/user/fluxaventures)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to let OpenClaw agents make stablecoin payments, check balances, manage spending, route cross-chain transfers, and interact with Oris marketplace services under configured credentials and spending policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real payments, withdrawals, fiat funding, cross-chain transfers, and marketplace purchases.

Mitigation: Review requests before execution, start with low spending limits, and require explicit human confirmation for transfers, withdrawals, fiat funding, and purchases.

Risk: The skill uses persistent Oris credentials for authenticated payment operations.

Mitigation: Run it only in trusted launch environments and rotate or revoke Oris credentials if logs or local configuration may have been exposed.

Risk: The security summary flags raw sensitive argument logging.

Mitigation: Avoid sensitive free-text payment details, redact financial logs, and prefer a release that redacts tool arguments.

Risk: The API base URL can be set through ORIS_BASE_URL.

Mitigation: Use the default Oris API endpoint and avoid untrusted environments that can override runtime environment variables.

Risk: The setup package depends on an unbounded oris-sdk version.

Mitigation: Review installed dependencies and prefer a release that pins the production SDK dependency.

Risk: Payment controls depend on usage and policy enforcement before execution.

Mitigation: Prefer a release that validates endpoint configuration and initializes fail-closed usage checks correctly before enabling real fund movement.

## Reference(s):

- [Skill Openclaw listing](https://clawhub.ai/fluxaventures/skills/skill-openclaw)
- [Oris OpenClaw documentation](https://useoris.finance/docs/openclaw)
- [Oris documentation](https://useoris.finance/docs)
- [Oris dashboard](https://useoris.finance/dashboard)
- [Oris API base URL](https://api.useoris.finance)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON-formatted MCP tool responses and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORIS_API_KEY, ORIS_API_SECRET, ORIS_AGENT_ID, python, and node; payment tools call the Oris API.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
