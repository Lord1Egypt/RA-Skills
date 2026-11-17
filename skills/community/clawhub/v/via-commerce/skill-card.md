## Description:

Agentic commerce over the VIA network. Discover products and sellers, submit a buyer brief and get genuine matches, find live buyer demand, and register your own store, all settled in USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardjhobbs](https://clawhub.ai/user/richardjhobbs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover products and sellers, submit buying briefs, find buyer demand, and register stores on the VIA commerce network. It supports commerce workflows that may involve third-party MCP endpoints and USDC settlement on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate payment workflows and route shopping or selling requests to a commerce network.

Mitigation: Confirm the product, seller, price, and payment intent with the user before payment, and enforce strict payment delegation caps.

Risk: The skill can connect to participant-provided seller or buyer MCP endpoints.

Mitigation: Verify endpoint and seller identity out of band for important purchases and limit sensitive data shared with third-party endpoints.

Risk: Store registration can collect wallet and dashboard account details.

Mitigation: Use a unique password, provide only the intended USDC payout wallet, and review registration data before submission.

## Reference(s):

- [VIA network MCP endpoint](https://app.getvia.xyz/mcp)
- [VIA Commerce on ClawHub](https://clawhub.ai/richardjhobbs/skills/via-commerce)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and MCP tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route commerce requests to external MCP tools and payment workflows after user approval.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
