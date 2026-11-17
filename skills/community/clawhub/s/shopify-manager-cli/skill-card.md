## Description:

Manage Shopify store products, metafields, metaobjects, blogs, articles, and files via the Shopify Admin GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asenwang](https://clawhub.ai/user/asenwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators use this skill to translate Shopify administration requests into Python CLI commands for listing, creating, updating, uploading, and deleting store resources through the Shopify Admin GraphQL API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a powerful Shopify Admin API token and can perform destructive store operations.

Mitigation: Use a least-privilege Shopify custom app token and require explicit human confirmation before deletes or other store-changing actions.

Risk: A misconfigured store URL or file upload path could affect the wrong shop or expose sensitive local files.

Mitigation: Set SHOPIFY_STORE_URL only to the exact shop domain and review local file paths before upload.

Risk: The scanner notes under-scoped safeguards for use with valuable production store data.

Mitigation: Review before installing on a production store and consider adding host validation plus force or dry-run safeguards.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asenwang/skills/shopify-manager-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN, and SHOPIFY_API_VERSION environment variables.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
