## Description: <br>
Use this skill when a user wants to browse, compare, buy, pay for, query orders, track logistics, manage addresses, cancel/refund eligible orders, or apply after-sale service on Filtalgo through the bundled Agent Tool Gateway CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[microtobe](https://clawhub.ai/user/microtobe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers use this skill to search Filtalgo products, manage cart and checkout flows, prepare wallet payment, review orders and logistics, manage delivery addresses, and request eligible cancellation, refund, or after-sale service through the bundled CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth-backed access can change cart, checkout, address, cancellation, refund, and after-sale state. <br>
Mitigation: Confirm the exact action, item, address, order, and amount with the user before executing sensitive commands. <br>
Risk: The skill uses wallet payment preparation and sensitive credentials for Filtalgo shopping workflows. <br>
Mitigation: Use it only for intended Filtalgo shopping tasks and avoid exposing access tokens, refresh tokens, client secrets, or payment links beyond the user who must complete the payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/microtobe/shopping-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, OAuth login, and explicit confirmation before sensitive shopping actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
