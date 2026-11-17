## Description:

Autonomous BigCommerce product content optimizer for bulk rewriting, optimizing, generating, and updating product titles and descriptions with progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veevortexiq](https://clawhub.ai/user/veevortexiq)

### License/Terms of Use:


## Use Case:

External BigCommerce store operators and developers use this skill to fetch catalog products, generate improved product titles and HTML descriptions, apply updates through the BigCommerce API, and track page-by-page progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can autonomously rewrite live BigCommerce product content across a store.

Mitigation: Use a test store first, export or back up catalog content, and review every generated update file before pushing changes.

Risk: Credential handling safeguards are weak for production catalog writes.

Mitigation: Use a narrowly scoped BigCommerce token and avoid passing tokens directly on the command line when operational alternatives are available.

Risk: Bulk updates have limited confirmation and validation before writing to BigCommerce.

Mitigation: Run with a small page limit first, inspect generated titles and descriptions, and monitor progress.json for failures before continuing at larger scale.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veevortexiq/skills/viq-bc-optimiser)
- [BigCommerce Catalog API base endpoint](https://api.bigcommerce.com/stores/{store_hash}/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON workflow files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates progress.json, page_N_products.json, and page_N_updates.json during the catalog update workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
