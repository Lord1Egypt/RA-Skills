## Description:

Queries 1688 cross-border product details through AlphaShop using a 1688 product URL or product ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators working with 1688 product data use this skill to turn product URLs or product IDs into structured details such as title, price, images, specifications, and supplier information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AlphaShop API credentials are required and may be exposed if pasted into chat or stored insecurely.

Mitigation: Configure apiKey and secretKey only through protected configuration or a secret mechanism; do not include them in prompts, logs, or shared artifacts.

Risk: 1688 product IDs are sent to AlphaShop for lookup.

Mitigation: Use the skill only when that third-party data transfer is acceptable for the queried product data.

Risk: Broad Python dependency ranges may change behavior over time.

Mitigation: Pin and review Python dependencies before production deployment.

Risk: Forceful routing language in the artifact could cause overuse beyond the intended task.

Mitigation: Apply the skill only to explicit 1688 product-detail requests and confirm credential and account-balance prerequisites before making calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/query-1688-product-detail)
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management)
- [AlphaShop offer detail query endpoint](https://api.alphashop.cn/alphashop.openclaw.offer.detail.query/1.0)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [JSON response data with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a 1688 product URL, a numeric product ID, or comma-separated product IDs.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
