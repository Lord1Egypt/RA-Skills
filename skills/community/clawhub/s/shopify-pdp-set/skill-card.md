## Description:

Creates Shopify product-page still-image sets for one SKU from seller-confirmed product facts, with one image for each named theme.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shopify sellers and storefront teams use this skill to create a consistent product-detail image gallery for a single SKU from seller-confirmed facts and themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged for broader account access than the skill needs.

Mitigation: Consider waiting for narrower permissions; if installing, review the shared media and spending access and revoke the connection in the Beatra Console when appropriate.

Risk: Image generation can incur live costs.

Mitigation: Review the current estimate and explicitly approve billable generation before submission.

Risk: Optional product or brand reference images are uploaded externally.

Mitigation: Upload only references you are authorized to share after reviewing their contents and destination.

Risk: The release's uninstall checks may disconnect other Beatra skills.

Mitigation: Check other installed Beatra skills before removal and consider waiting for corrected uninstall checks; access can also be revoked from the Beatra Console.

Risk: Automatic installation analytics may report installation details.

Mitigation: Review the installation-registration data and related privacy terms before installing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/shopify-pdp-set)
- [Beatra skill page](https://beatra.ai/skills/shopify-pdp-set)
- [Product-image workflow](artifact/references/workflow.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Billing and recovery](artifact/references/billing-errors-and-recovery.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Image files, Text]

**Output Format:** [Separate product-page still images, usually 1:1 at 2K, plus task-result guidance]

**Output Parameters:** [One image per named theme; typically 4–8 images for one SKU]

**Other Properties Related to Output:** [Optional seller-provided reference images may be uploaded for generation or editing.]

## Skill Version(s):

0.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
