## Description: <br>
Search, bargain, order, and pay for pet supplies on Vigilath.com, an AI-powered pet commerce platform with multi-round price negotiation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gt-oliver](https://clawhub.ai/user/gt-oliver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to search for pet supplies, review AI product recommendations, negotiate eligible prices, place and track orders, manage shipping addresses, and initiate payments on Vigilath.com. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place orders and proceed into payment flows. <br>
Mitigation: Require manual confirmation before every order placement or payment, including item, quantity, price, shipping address, and payment method. <br>
Risk: The skill can create or use shipping addresses that contain personal information. <br>
Mitigation: Only create or share an address after the user explicitly approves the exact address data being sent. <br>
Risk: The skill uses a bearer token for authenticated shopping actions. <br>
Mitigation: Store VIGILATH_TOKEN as a secret and avoid exposing it in chat, logs, command output, or shared files. <br>


## Reference(s): <br>
- [Vigilath Agent Service](https://www.vigilath.com) <br>
- [Vigilath agent discovery](https://www.vigilath.com/.well-known/agent.json) <br>
- [Vigilath LLM-readable API summary](https://www.vigilath.com/llms.txt) <br>
- [Vigilath full API documentation](https://www.vigilath.com/llms-full.txt) <br>
- [ClawHub skill page](https://clawhub.ai/gt-oliver/vigilath-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Vigilath API responses for product, bargain, order, address, and payment status data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
