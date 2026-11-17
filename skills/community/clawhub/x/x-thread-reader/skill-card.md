## Description:

Fetch full text or generate a PDF from any X/Twitter thread using twitter-thread.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngmeyer](https://clawhub.ai/user/ngmeyer)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve readable text from a specific X/Twitter thread or save that thread as a PDF for review, citation, archiving, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target tweet IDs are sent to twitter-thread.com when fetching text or generating PDFs.

Mitigation: Use the skill only after an explicit request to read or download a specific public thread, and confirm external-service sharing is acceptable.

Risk: PDF mode may write to the default Downloads location when no output path is provided.

Mitigation: Provide an explicit output path for PDF generation when file location matters.

Risk: Thread text can be unavailable or incomplete when a thread is not indexed, protected, deleted, very long, or affected by changes to twitter-thread.com page structure.

Mitigation: Check command errors and compare against the PDF or original source when completeness matters.

## Reference(s):

- [X Thread Reader on ClawHub](https://clawhub.ai/ngmeyer/skills/x-thread-reader)
- [twitter-thread.com](https://twitter-thread.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown-style text output with metadata headers, or a generated PDF file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text mode prints title, author, source links, and extracted article text; PDF mode writes a PDF to the requested path or the default Downloads path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
