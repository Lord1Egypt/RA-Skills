## Description:

Convert any webpage to a clean, high-quality PDF file and send it directly. Use when the user asks to view a website, screenshot a webpage, or see a page's content. Exports the webpage using browser PDF functionality for crystal-clear results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huchiyv](https://clawhub.ai/user/huchiyv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn requested webpages into readable PDF files for viewing, saving, printing, or sharing. It is suited to explicit webpage export or webpage screenshot requests where a PDF is an acceptable output format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup commands may remove the wrong file if the PDF path is substituted incorrectly.

Mitigation: Remove only the exact PDF path returned by the browser export after the file has been sent.

Risk: The workflow browses requested URLs and creates shareable PDF files from webpage content.

Mitigation: Use the skill for explicit export requests and confirm the requested URL and generated PDF before sending it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huchiyv/skills/web-to-pdf)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline tool commands and PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local PDF files that should be sent to the user and then cleaned up carefully.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
