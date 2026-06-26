## Description: <br>
Shopify Admin guides agents through Shopify Admin API workflows for product tags, inventory, OAuth token refresh, and other GraphQL or REST operations using a Custom App access token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happynocyohei](https://clawhub.ai/user/happynocyohei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and store operators use this skill to guide agents through Shopify Admin API operations such as reading and updating product tags, preparing inventory-related requests, and refreshing OAuth tokens while handling store credentials carefully. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopify Admin API credentials can authorize sensitive product, inventory, theme, order, or customer-data changes. <br>
Mitigation: Use least-privilege Shopify scopes, verify the store domain, keep tokens and client secrets out of chats and logs, rotate exposed credentials, and require explicit confirmation before write operations. <br>
Risk: Product tag updates replace the full tag list when using the documented productUpdate pattern. <br>
Mitigation: Fetch current tags first, merge the intended changes, and confirm the complete final tag set before updating. <br>
Risk: OAuth refresh flows can expose client secrets or use placeholder redirect domains if copied directly. <br>
Mitigation: Configure an approved redirect URL for the target app and protect client secrets during the short-lived code exchange. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happynocyohei/shopify-admin-sop) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline GraphQL, REST, TOML, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Shopify store domain and Admin API access token; write operations should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
