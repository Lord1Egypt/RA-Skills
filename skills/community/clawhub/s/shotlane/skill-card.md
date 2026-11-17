## Description:

Screenshot any public web page, read pages as clean Markdown (JavaScript rendered), and render HTML or URLs to PDF using the Shotlane API. Use when the user wants to see what a website looks like, check a deployed page or layout on desktop/mobile, capture a page or element as an image, extract an article or docs page as text for analysis, or produce a PDF (invoices, reports) from HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shotlane](https://clawhub.ai/user/shotlane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can capture public webpages as screenshots, extract page content as Markdown, and create PDFs from a URL or supplied HTML. Use it to inspect a deployed page, read web content, or produce a printable document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key could be exposed through an untrusted destination or redirect.

Mitigation: Use only trusted service endpoints and destinations, and review redirect handling before invoking the skill.

Risk: Local HTML is uploaded without a clear warning.

Mitigation: Treat HTML supplied for PDF generation as content sent to the service; do not submit sensitive documents.

## Reference(s):

- [Shotlane](https://shotlane.dev)
- [Shotlane API documentation](https://shotlane.dev/docs)
- [Shotlane documentation for agents](https://shotlane.dev/llms-full.txt)

## Skill Output:

**Output Type(s):** [Images, Markdown, PDF files]

**Output Format:** [PNG, JPEG, or WebP images; Markdown text; PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A successful request uses one credit; failed calls are free.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
