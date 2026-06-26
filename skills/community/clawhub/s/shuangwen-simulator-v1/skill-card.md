## Description: <br>
爽文模拟器V1.0虾舍出品 is a paid Chinese story-game launcher for browsing, buying, unlocking, installing, and starting system-novel power fantasy scenario packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hengruizzzz](https://clawhub.ai/user/hengruizzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Chinese-language story-game players use this skill to preview paid scenarios, create a payment order, verify entitlement, and receive or install a paid scenario Skill package. Operators can use it to test the same launcher flow when payment and fulfillment tools are connected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a paid launcher with payment and downstream Skill installation behavior that requires user review before use. <br>
Mitigation: Before approving any action, verify the scenario name, price, merchant or payment tool, and any returned paid package or signed install URL. <br>
Risk: Payment links, wallet credentials, payment tokens, and signed install URLs may be sensitive. <br>
Mitigation: Do not share wallet credentials or payment tokens in chat, and preserve returned payment or install URLs exactly without rewriting them. <br>
Risk: A user statement that payment was completed is not sufficient to unlock paid content. <br>
Mitigation: Confirm entitlement through merchant-side order status or the connected payment tool before returning or installing the paid Skill package. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hengruizzzz/shuangwen-simulator-v1) <br>
- [Alipay Paid Access](artifact/references/alipay-paid-access.md) <br>
- [Paid Scenario Notice](artifact/references/apocalypse-space-folding.md) <br>
- [Public Scenario Catalog Preview](artifact/references/scenario-catalog-preview.md) <br>
- [System Archetypes](artifact/references/system-archetypes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or chat text with exact returned payment, package, or install links when present] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves signed URLs exactly when returned and tracks payment entitlement state before unlock.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
