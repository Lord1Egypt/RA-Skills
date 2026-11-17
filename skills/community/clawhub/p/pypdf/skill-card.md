## Description:

Extract text, metadata, and pages from PDF files using pypdf. Use for tasks such as reading PDF content, extracting specific pages, splitting or merging PDFs, reading document metadata, and rotating or transforming pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-ai-tech](https://clawhub.ai/user/maverick-ai-tech)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect PDFs, extract text or selected pages, split or merge documents, and rotate pages through deterministic local commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned pypdf dependency or processing unintended local PDF paths can affect package trust and file-access scope.

Mitigation: Install pypdf in an isolated environment from a pinned, trusted package source, and run commands only on intended input files and output locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-ai-tech/skills/pypdf)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands, stdout text, and generated PDF file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses 0-indexed page arguments; PDF-writing commands require explicit output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
