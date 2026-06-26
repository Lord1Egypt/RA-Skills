## Description: <br>
TravelKit flight booking and management skill for flight search, pricing, real-time price verification, order creation, payment, cancellation, refund, change, itinerary download, and TravelKit MCP integration policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travelkit](https://clawhub.ai/user/travelkit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-service agents use this skill to search, price, book, pay for, cancel, refund, change, and retrieve information for TravelKit flight orders while following confirmation and output rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real booking, payment, cancellation, refund, invoice, and change workflows. <br>
Mitigation: Require explicit user confirmation before each write action, and verify price and order details before collecting passenger data or creating an order. <br>
Risk: The skill depends on a sensitive platform-managed TravelKit API key. <br>
Mitigation: Keep credentials managed by the host platform, avoid asking users to paste API keys in chat, and treat missing or invalid credentials as a platform configuration issue. <br>
Risk: Users may misunderstand prices, policies, payment links, or confirmations if the default language is not appropriate. <br>
Mitigation: Users who prefer another language should request it before reviewing prices, policies, payment links, or confirmations. <br>


## Reference(s): <br>
- [TravelKit Skill on ClawHub](https://clawhub.ai/travelkit/travelkit-skill) <br>
- [TravelKit](https://www.travelkit.ai/) <br>
- [TravelKit Flight Skill](SKILL.md) <br>
- [Confirmation Rules](references/confirmation-rules.md) <br>
- [Output Rules](references/output-rules.md) <br>
- [TravelKit MCP Connection](references/mcp-connection.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, tool-call instructions] <br>
**Output Format:** [Markdown and concise natural-language responses, usually in Simplified Chinese unless the user requests another language.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TravelKit tool results as raw inputs, hides internal identifiers and credentials, and requires explicit confirmation before write operations.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
