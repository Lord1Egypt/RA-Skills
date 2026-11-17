## Description:

Tariff Search provides tariff calculation and HS code classification through the TurtleClassify API for cross-border product records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncai519](https://clawhub.ai/user/simoncai519)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce operators use this skill to classify products, retrieve HS codes, calculate import tariffs and duties, and prepare tariff-enriched product lists for sourcing or landed-cost analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product names and metadata are sent to the external Accio/TurtleClassify tariff API.

Mitigation: Submit only product details that are appropriate to share with that third-party service, and avoid unnecessary identifiers or sensitive sourcing information.

Risk: CSV export examples can overwrite local files if an existing output path is reused.

Mitigation: Choose output paths deliberately and review generated CSV locations before writing results.

## Reference(s):

- [TurtleClassify API Reference](references/api-reference.md)
- [Accio TurtleClassify endpoint](https://www.accio.com/api/turtle/classify)
- [Skill page](https://clawhub.ai/simoncai519/skills/tariff-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON-like tariff lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return a flattened result list for DataFrames or CSV export, or a detailed dictionary with processing metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
