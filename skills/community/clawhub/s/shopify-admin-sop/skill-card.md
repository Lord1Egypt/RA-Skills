## Description:

Shopify Admin API SOP for product tags, inventory, and other write operations via GraphQL/REST, for stores using a Custom App access token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happynocyohei](https://clawhub.ai/user/happynocyohei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators use this skill to guide Shopify Admin API write operations, including product tags, inventory-related scopes, and token refresh workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Shopify Admin credentials that can modify products, inventory, themes, and orders depending on token scopes.

Mitigation: Use least-privilege Shopify scopes, verify the intended myshopify.com store domain before each request, and review proposed write operations before execution.

Risk: The OAuth example uses example.com and a static state value, which could expose an authorization code if followed literally.

Mitigation: Use a HTTPS callback endpoint you control, generate fresh state values, and handle client secrets, authorization codes, and access tokens securely.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline GraphQL, REST, TOML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Shopify store domain and Admin API access token secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
