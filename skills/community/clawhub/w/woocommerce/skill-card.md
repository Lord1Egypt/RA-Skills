## Description: <br>
WooCommerce REST API integration with managed OAuth for products, orders, customers, coupons, shipping, taxes, reports, webhooks, payment gateways, store settings, and system status tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators, developers, and support staff use this skill to manage WooCommerce e-commerce operations, process orders, maintain catalog data, inspect reports, and administer store integrations through Maton-mediated API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect a real WooCommerce store through Maton-mediated access. <br>
Mitigation: Install only for intended store administration use and connect the least-privileged WooCommerce account practical. <br>
Risk: Refunds, deletes, payment gateway changes, store settings, webhook creation, and system maintenance can change store behavior or disrupt operations. <br>
Mitigation: Require explicit user confirmation of the target resource, requested action, and expected effect before allowing these operations. <br>
Risk: Customer and order endpoints can expose personal information. <br>
Mitigation: Retrieve and display customer or order PII only when needed for the user's task, and avoid retaining it in generated outputs. <br>


## Reference(s): <br>
- [ClawHub WooCommerce Skill](https://clawhub.ai/byungkyu/woocommerce) <br>
- [WooCommerce REST API Documentation](https://woocommerce.github.io/woocommerce-rest-api-docs/) <br>
- [WooCommerce API Authentication Guide](https://woocommerce.github.io/woocommerce-rest-api-docs/#authentication) <br>
- [WooCommerce Developer Resources](https://developer.woocommerce.com/) <br>
- [Maton Settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and a valid MATON_API_KEY for Maton-mediated WooCommerce API calls.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
