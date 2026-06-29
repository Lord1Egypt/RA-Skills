## Description: <br>
Mail custom folded greeting cards to any US address using AgentPMT-hosted actions that preview, proof, send, and track card orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams and agents use this skill to create, preview, proof, mail, and track custom folded greeting cards for outreach, appreciation, invitations, and personal messages to US recipients. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Recipient addresses and card contents are shared with AgentPMT and downstream print/mail providers. <br>
Mitigation: Before sending, confirm the exact recipient, address, card content, cost, and permission to share the address and content with the service providers. <br>
Risk: The send action mails a physical card and consumes credits. <br>
Mitigation: Use render_preview or create_proof first and require explicit user approval before calling send. <br>
Risk: International mailing is not supported. <br>
Mitigation: Verify the recipient address is in the United States and includes the required name or organization, street, city, state, and postal code fields. <br>
Risk: Preview document and image URLs are temporary. <br>
Mitigation: Review and approve previews within the stated 7-day window, or regenerate the preview before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/send-a-custom-greeting-card) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/send-a-greeting-card) <br>
- [Generated action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API Calls, Guidance] <br>
**Output Format:** [Markdown instructions with JSON action payloads and signed URL outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return order IDs, document PDFs, preview image URLs, tracking data, and order status; preview URLs expire after 7 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
