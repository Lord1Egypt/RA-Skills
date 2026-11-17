## Description:

Helps agents preview and mail personalized folded greeting cards to US addresses through AgentPMT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and organizations use this skill to preview and send personalized greeting cards, invitations, and appreciation mail to recipients in the United States.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Sending a physical card spends credits and initiates real-world mail.

Mitigation: Show the preview and require explicit user approval before sending or spending credits.

Risk: Recipient addresses and card content are shared with AgentPMT and its print and mail providers.

Mitigation: Confirm the user is permitted to share the address and content before submitting them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/agentpmt/skills/send-a-custom-greeting-card)
- [AgentPMT greeting card product](https://www.agentpmt.com/marketplace/send-a-greeting-card)
- [Greeting card action schema](artifact/schema.md)
- [AgentPMT account setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Guidance, JSON tool-call examples]

**Output Format:** [Markdown with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides preview, proof, send, order-status, and tracking requests; preview responses can include temporary PDF and image links.]

## Skill Version(s):

1.0.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
