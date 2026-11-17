## Description:

Use when converting markdown files to PDF with styling, code highlighting, and CJK support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuleikiro222](https://clawhub.ai/user/zhuleikiro222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to convert Markdown documents into styled PDF files for offline documentation, reports, and shareable technical materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says untrusted Markdown is rendered as active browser content with browser sandboxing disabled and unrestricted network access.

Mitigation: Use the skill only with trusted Markdown or in an isolated environment, and avoid files from other people until JavaScript is disabled, HTML is sanitized, network requests are blocked, and browser sandboxing is restored.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JavaScript configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for generating PDF files from Markdown using Node.js, marked, puppeteer-core, and a local Chrome or Edge browser.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
