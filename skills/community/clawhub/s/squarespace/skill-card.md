## Description: <br>
Squarespace Commerce API integration with managed OAuth for managing products, inventory, orders, customer profiles, and transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and developers use this skill to let an agent manage Squarespace commerce workflows through Maton's managed OAuth proxy. It supports product, inventory, order, customer profile, and transaction operations for connected Squarespace stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive store, customer, address, order, and transaction data. <br>
Mitigation: Limit requests to data needed for the task and avoid asking the agent to fetch or display unnecessary customer, address, order, or transaction details. <br>
Risk: The skill can change live commerce content, inventory, orders, and related store records. <br>
Mitigation: Approve write operations only after checking the exact product, order, inventory, customer, or transaction target and intended effect. <br>
Risk: MATON_API_KEY and OAuth-backed Maton connections provide access to connected Squarespace stores. <br>
Mitigation: Protect MATON_API_KEY, install only if Maton is trusted to proxy OAuth-backed Squarespace access, and specify the intended connection when more than one store is connected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/squarespace) <br>
- [Maton](https://maton.ai) <br>
- [Squarespace Commerce APIs Overview](https://developers.squarespace.com/commerce-apis/overview) <br>
- [Squarespace Inventory API](https://developers.squarespace.com/commerce-apis/inventory-overview) <br>
- [Squarespace Orders API](https://developers.squarespace.com/commerce-apis/orders-overview) <br>
- [Squarespace Products API](https://developers.squarespace.com/commerce-apis/products-overview) <br>
- [Squarespace Profiles API](https://developers.squarespace.com/commerce-apis/profiles-overview) <br>
- [Squarespace Transactions API](https://developers.squarespace.com/commerce-apis/transactions-overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python, JavaScript, curl, and HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Squarespace OAuth account through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
