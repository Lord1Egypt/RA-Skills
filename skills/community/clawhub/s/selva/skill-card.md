## Description: <br>
Shopping platform for AI agents <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpbonch](https://clawhub.ai/user/jpbonch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Selva to search Amazon products, compare options, inspect details, and place purchases after required profile and payment setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real shopping orders. <br>
Mitigation: Require explicit confirmation of the selected item, price, shipping address, and payment method before every purchase; use the approval threshold when available. <br>
Risk: The skill handles shipping details, contact information, API keys, and payment-card data. <br>
Mitigation: Prefer the web settings page for payment setup, avoid entering card numbers or CVV in chat or command-line flags, and review local configuration before use. <br>


## Reference(s): <br>
- [Selva ClawHub release](https://clawhub.ai/jpbonch/selva) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and product or order summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product titles, prices, ratings, delivery estimates, image URLs, provider URLs, settings status, and order status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
