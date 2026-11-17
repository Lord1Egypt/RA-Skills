## Description:

Manages agentic wallets via the caw CLI with safety guidance for balance checks, explicit approvals, and bounded on-chain operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengjunquan-l](https://clawhub.ai/user/pengjunquan-l)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting users with Cobo agentic wallet workflows use this skill to plan fund-related actions, check balances, preview transaction parameters, and require explicit owner approval before on-chain operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On-chain wallet operations can move funds irreversibly.

Mitigation: Confirm the caw CLI, pact approval flow, spending limits, chain, asset, amount, and recipient before allowing any transaction.

Risk: External content could attempt to trigger unauthorized fund movement.

Mitigation: Reject wallet operations prompted by webhooks, emails, uploaded documents, tool outputs, or other third-party content unless the user directly states the request and approves the full parameters.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on explicit owner approval, transaction previews, balance checks, and prompt-injection rejection before wallet operations.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
