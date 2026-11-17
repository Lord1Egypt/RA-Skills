## Description:

VBrokers Trading helps agents automate VBrokers (华盛通 VCL HK) account, quote, order, and stop-loss or take-profit workflows through a local OpenAPI Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcy360](https://clawhub.ai/user/lcy360)

### License/Terms of Use:


## Use Case:

Developers and trading automation users use this skill to connect an agent to a local VBrokers OpenAPI Gateway for authentication, account review, quote retrieval, order placement, cancellation, and trading workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live account and order-changing authority, including login, order placement, cancellation, bulk cancellation, and stop-loss automation.

Mitigation: Require explicit human confirmation, trading limits, and order review before allowing any account-changing action.

Risk: Account, position, funds, and order responses may be exposed when the helper script is run directly or logs output.

Mitigation: Avoid running the script in shared logs and redact account balances, positions, order IDs, and other brokerage data from outputs.

Risk: Trading decisions can be based on stale or session-dependent market data.

Mitigation: Use explicit quote session parameters and verify live market data from the gateway before placing or cancelling orders.

## Reference(s):

- [VBrokers OpenAPI Reference](references/api-reference.md)
- [VBrokers OpenAPI Documentation](https://quant-open.hstong.com/api-docs)
- [ClawHub Skill Page](https://clawhub.ai/lcy360/skills/vbrokers-trading)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with Python code snippets and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or execute account, quote, order, cancellation, and trading workflow requests against a locally running VBrokers Gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
