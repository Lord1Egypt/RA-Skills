## Description:

Removes watermarks from PDF files after checking the local environment, detecting likely watermark elements, and asking for user confirmation before processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oalh-wh](https://clawhub.ai/user/oalh-wh)

### License/Terms of Use:


## Use Case:

External users and document-processing agents use this skill to inspect PDFs for likely watermarks, show detection results, and create processed PDF copies after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install unpinned Python libraries after confirmation.

Mitigation: Review the proposed packages before installation, avoid elevated privileges, and run in a controlled Python environment.

Risk: The skill may write extracted preview images and processed PDFs to disk.

Mitigation: Use copies of documents, choose a private output directory, and avoid shared writable folders.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with local command output and generated PDF or preview files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write watermark preview images and processed PDF copies after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
