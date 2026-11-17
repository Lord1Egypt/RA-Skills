## Description:

Converts HTML content, web links, presentations, or HTML files into a browser-printable page that users can export to PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to stage HTML documents or URLs as printable pages and return concise instructions for exporting them to PDF in a local browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User HTML may be published to a potentially reachable long-lived URL.

Mitigation: Use only non-sensitive HTML unless deployment destination, access controls, expiration, and deletion are explicitly handled outside the skill.

Risk: URL rendering can fetch or display content outside the intended scope.

Mitigation: Confirm the exact source URL, user consent, and permitted content scope before rendering or deploying a page.

Risk: Private documents, credentials, internal pages, customer data, or regulated information could be exposed through the export workflow.

Mitigation: Do not use the skill for sensitive or regulated content without external controls that prevent unauthorized access and support cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/yq-pdf-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/tianheihei002)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and HTML/CSS templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or deploy HTML pages for browser-based PDF export; does not support direct image-to-PDF conversion.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
