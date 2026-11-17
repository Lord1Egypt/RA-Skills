## Description:

Read-only balance checking and spending analytics for Sardis agent wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efedurmaz16](https://clawhub.ai/user/efedurmaz16)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to inspect Sardis wallet balances, spending summaries, transaction history, vendor spend, and remaining budgets without initiating payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles financial wallet balances, transaction history, vendor spend, budget data, and a Sardis API key.

Mitigation: Use a Sardis API key limited to the wallets and read-only permissions required for the task.

Risk: The release asks to install an unnecessary unpinned npm package.

Mitigation: Install only after the dependency is removed or pinned, or review the package before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/efedurmaz16/skills/sardis-balance)
- [Sardis homepage](https://sardis.sh)
- [Sardis Balance API documentation](https://sardis.sh/docs/balance-api)
- [Sardis API reference](https://api.sardis.sh/v2/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SARDIS_API_KEY and read-only Sardis API endpoints for wallet analytics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
