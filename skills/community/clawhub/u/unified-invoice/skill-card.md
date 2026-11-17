## Description:

Generates Korean quotes, Korean tax invoices, and freelancer invoice documents with client and item records, VAT calculations, and HTML, PDF, or Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT

## Use Case:

Freelancers and small business operators use this skill to create Korean quotes, Korean tax invoices, and client invoices while maintaining reusable client, sender, and item records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unescaped document data can affect generated HTML or PDF invoices when client, item, notes, or date values are untrusted.

Mitigation: Escape or sanitize document fields before rendering and avoid untrusted client, item, notes, or date values until escaping is fixed.

Risk: Path handling can expose unsafe file-write or PDF-conversion behavior.

Mitigation: Validate output filenames and paths before writing files or converting HTML to PDF.

Risk: Client, sender, invoice, and bank details are sensitive business data stored in local JSON and generated document files.

Mitigation: Keep the data and output directories out of shared repositories and restrict access to generated invoices.

Risk: PDF conversion depends on a browser connection and may process generated invoice HTML.

Mitigation: Run PDF conversion in an isolated browser profile until escaping and output path validation are addressed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/unified-invoice)

## Skill Output:

**Output Type(s):** [Markdown, HTML, PDF, Shell commands, Configuration]

**Output Format:** [Markdown, HTML, and PDF files plus command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated documents to an output directory and stores client, item, and sender records in JSON files.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter/package.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
