## Description: <br>
RevenueCat metrics, customer data, and documentation search. Use when querying subscription analytics, MRR, churn, customers, or RevenueCat docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeiting](https://clawhub.ai/user/jeiting) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to query RevenueCat subscription analytics, customer records, project configuration, and API documentation while working with RevenueCat projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RevenueCat API key, which may expose project, subscription, customer, or revenue data to the agent. <br>
Mitigation: Use the least-privileged or read-only RevenueCat key available and expose broad customer data only when it is needed for the task. <br>
Risk: The reference material includes POST, DELETE, refund, cancel, webhook, product, entitlement, offering, project, and balance-changing operations. <br>
Mitigation: Require explicit human confirmation before using any referenced operation that can modify configuration, customer state, subscriptions, purchases, webhooks, products, entitlements, offerings, projects, refunds, cancellations, or balances. <br>


## Reference(s): <br>
- [ClawHub RevenueCat skill page](https://clawhub.ai/jeiting/revenuecat) <br>
- [RevenueCat documentation](https://www.revenuecat.com/docs) <br>
- [RevenueCat documentation index for agents](https://www.revenuecat.com/docs/llms.txt) <br>
- [RevenueCat Developer API v2 Reference](references/api-v2.md) <br>
- [RevenueCat API v2 base URL](https://api.revenuecat.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, local API reference excerpts, and RevenueCat API response interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and RC_API_KEY. The bundled shell wrapper issues GET requests to the RevenueCat API v2 base URL.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
