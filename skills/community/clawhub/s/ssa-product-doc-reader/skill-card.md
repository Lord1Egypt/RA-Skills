## Description:

Extracts structured product data from engineering drawing PDFs, using pdftotext first and Vision processing as a fallback for layout-heavy content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to extract BOMs, model numbers, drawing numbers, packaging specs, dimensions, test requirements, and Markdown knowledge-base entries from product engineering PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Engineering PDFs and BOM data may leave the local machine for third-party Vision processing.

Mitigation: Use --text-only for confidential documents, or run Vision mode only with data and service approvals that match the deployment environment.

Risk: The artifact includes unsafe credential behavior involving an embedded OpenRouter key.

Mitigation: Remove and rotate the embedded key before use, and supply service credentials through approved environment variables or secret management.

Risk: Batch cleanup behavior can be unsafe when pointed at arbitrary temporary directories.

Mitigation: Run batch cleanup only against known controlled paths and review output directories before executing batch scripts.

Risk: Broad agent configuration access could expose sensitive local settings.

Mitigation: Limit the skill's filesystem access and avoid exposing broad agent configuration files during execution.

## Reference(s):

- [ClawHub skill page: Product Doc Reader](https://clawhub.ai/cjboy007/skills/ssa-product-doc-reader)
- [Publisher profile: cjboy007](https://clawhub.ai/user/cjboy007)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Development summary](artifact/DEVELOPMENT_SUMMARY.md)
- [Hybrid extraction test report](artifact/examples/hybrid/TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Files, Shell commands, Configuration]

**Output Format:** [JSON and Markdown files, with optional JSON or Markdown emitted to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include extracted product names, model numbers, drawing numbers, packaging specs, BOM rows, tolerances, dimensions, test requirements, confidence, warnings, and batch summary Markdown.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
