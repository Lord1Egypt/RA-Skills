## Description:

Generates quotation documents in Excel, Word, HTML, and PDF with pre-generation data validation to reduce accidental use of sample customer data and optional OKKI CRM workflow support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales operators and developers use this skill to turn structured quotation JSON into customer-ready quotation files and to run validation checks before sharing them externally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the all-in-one workflow on untrusted file paths or quotation JSON may lead to unintended local file handling or unsafe generated documents.

Mitigation: Use trusted quotation data files only, review workflow boundaries before installation, and inspect generated documents before sending them to customers.

Risk: Generated HTML can include customer-supplied quotation content and external font or icon assets.

Mitigation: Do not open generated HTML from untrusted data, prefer local pinned assets, and ensure content is escaped before customer distribution.

Risk: The workflow can attempt automatic OKKI synchronization through a sibling script.

Mitigation: Disable or remove automatic OKKI sync unless that integration and its credentials are trusted for the deployment environment.

Risk: The bundled signature authorization restricts signature use to quotation documents only.

Mitigation: Use signature assets only for quotation PDFs or Word quotation documents, and exclude them from contracts, invoices, financial records, and legal documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cjboy007/skills/quotation-workflow)
- [Quick Start](QUICK_START.md)
- [Standard Workflow](STANDARD_WORKFLOW.md)
- [Workflow Checklist](WORKFLOW_CHECKLIST.md)
- [PDF Export Guide](docs/PDF_EXPORT.md)
- [Format Comparison](docs/FORMATS.md)
- [Signature Usage Authorization](assets/signatures/USAGE_AUTHORIZATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON inputs and shell commands that produce Excel, Word, HTML, and PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and Chrome on macOS according to ClawHub metadata; generated HTML may depend on external font and icon CDNs.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
