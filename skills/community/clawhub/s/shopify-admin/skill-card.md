## Description:

Shopify Admin API CLI for orders, products, customers, and store management. Uses REST and GraphQL APIs with environment-based authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robsannaa](https://clawhub.ai/user/robsannaa)

### License/Terms of Use:


## Use Case:

External developers and store operators use this skill to let an agent inspect and manage Shopify orders, products, customers, marketing events, reports, and store data through Shopify Admin REST and GraphQL API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles privileged Shopify store access and recommends broad read/write scopes.

Mitigation: Use the narrowest possible Shopify token scopes and review the runtime environment before installation.

Risk: The helper includes an unguarded product deletion command.

Mitigation: Do not enable destructive product deletion without an explicit confirmation step or a separate restricted token.

Risk: The documentation mentions a PII webhook workaround.

Mitigation: Avoid the PII webhook workaround and handle customer data under the store operator's privacy and compliance controls.

Risk: The store hostname is supplied through runtime configuration.

Mitigation: Validate or hardcode the intended myshopify.com hostname before allowing the skill to run.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, SHOPIFY_STORE_DOMAIN, and SHOPIFY_ACCESS_TOKEN; API responses may include privileged store and customer data.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
