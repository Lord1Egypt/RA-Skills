## Description:

Auto-create and manage digital products on Whop.com from product creation through plan and checkout link generation using the Whop REST API v1 with a Company API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up digital product sales on Whop by creating products, pricing plans, and checkout links for free, recurring, or one-time offers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create public products, paid plans, and checkout links in a Whop company account when run with a Company API key.

Mitigation: Use a least-privileged or test Whop API key when available, confirm the target company account, and review the intended products and prices before execution.

Risk: The security evidence notes live commercial account changes without a dry run or clear safety warning.

Mitigation: Run the script only when those products and prices are intended, and avoid production Company API keys unless the changes are approved.

## Reference(s):

- [Whop API Reference](https://docs.whop.com/api-reference/)
- [Whop Developer Portal](https://sell.whop.com/developer)
- [ClawHub Skill Page](https://clawhub.ai/ssidharhubble/skills/whop-digital-sales)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WHOP_API_KEY; the provided script can create public Whop products, paid plans, and checkout links in the target company account.]

## Skill Version(s):

1.0.14 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
