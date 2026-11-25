## Description:

Creates or reproduces minimalist grayscale resumes as HTML for PDF export, following a fixed single-column typography and layout specification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinqin700-arch](https://clawhub.ai/user/xinqin700-arch)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing a resume use this skill to format supplied content as a minimalist, single-column grayscale resume and export it to PDF. It can also reproduce the layout of a user-provided resume sample.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reported no findings, but was limited because a path-like reference in the PDF export command did not match a bundled artifact.

Mitigation: Check that the HTML input and PDF output paths are correct, and review the generated PDF before relying on it.

## Reference(s):

- [Typography specification](artifact/references/typography-spec.md)
- [Resume HTML template](artifact/assets/resume-template.html)
- [ClawHub skill page](https://clawhub.ai/xinqin700-arch/skills/resume-minimal-typeset)

## Skill Output:

**Output Type(s):** [HTML, PDF, Guidance]

**Output Format:** [HTML resume file with PDF export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The HTML follows the supplied typography specification; PDF export uses Chromium or a browser's print dialog.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
