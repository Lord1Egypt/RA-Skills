## Description:

Provides Python mock trading API examples and agent guidance for Chinese securities workflows, including market data, order management, position tracking, and automated trading patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically proficient trading workflow authors can use this skill to draft or inspect simulated Chinese securities trading API examples for market data, order management, account views, and strategy automation. Users should treat generated trading behavior as illustrative until real broker integration, controls, and reconciliation are independently verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents broker trading operations while the bundled implementation returns simulated login, market data, account, position, and order results.

Mitigation: Treat generated behavior as examples or simulation only until real broker authentication, paper/live separation, order confirmation, risk limits, and authoritative broker reconciliation are documented and reviewed.

Risk: The workflow accepts account and password inputs for broker-style operations.

Mitigation: Do not provide production broker credentials to this version; use non-sensitive test values until credential handling is independently reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/skills/quant-trading-api)
- [Huatai OpenAPI documentation](https://openapi.htsc.com)
- [Galaxy API documentation](https://api.galaxy.com)
- [Tushare Pro API](https://tushare.pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include broker configuration examples, API usage snippets, and simulated trading workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
