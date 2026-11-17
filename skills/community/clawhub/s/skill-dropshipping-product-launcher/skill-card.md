## Description:

Creates WooCommerce draft product listings with images, variants, and margin calculation from CJ Dropshipping products using a product ID and sell price.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT

## Use Case:

Developers and ecommerce operators use this skill to preview or create WooCommerce draft product listings from CJ Dropshipping product data, including image uploads, variants, pricing, and margin output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles CJ and WooCommerce credentials.

Mitigation: Use narrowly scoped credentials, store them outside shared workspaces, and rotate them if the skill has been run with untrusted configuration.

Risk: The skill can make live WooCommerce store changes and upload product media.

Mitigation: Run dry-run mode first and review the target store, product details, images, and draft listing before publishing.

Risk: Weak destination and download scoping can expose the store to unintended hosts or untrusted product image sources.

Mitigation: Require HTTPS, allow only exact trusted CJ and WooCommerce hosts, and avoid untrusted product or image URLs.

Risk: Dependency choices may become stale or include unreviewed transitive code.

Mitigation: Upgrade or pin reviewed dependencies before deployment and rescan after dependency changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-dropshipping-product-launcher)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Console text with a machine-readable JSON result block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create WooCommerce draft products, upload images, calculate margin, and run in dry-run preview mode.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
