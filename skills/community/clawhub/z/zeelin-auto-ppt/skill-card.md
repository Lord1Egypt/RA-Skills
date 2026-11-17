## Description:

ZeeLin Auto-PPT helps an agent draft presentation source content, automate Google NotebookLM to create illustrated slides, and download the result as a PDF after the user has logged in to NotebookLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn a requested topic into structured presentation content, invoke NotebookLM browser automation, and obtain a local PDF presentation. The user must provide or authorize any source material and complete NotebookLM login outside the agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation material is sent to Google NotebookLM and may remain in the user's NotebookLM account.

Mitigation: Use only content that may be shared with NotebookLM, and remove sensitive or confidential material before running the skill.

Risk: The artifact directs the agent to suppress or ignore failures and configuration issues.

Mitigation: Require visible error reporting and user confirmation before retrying, continuing after failures, or using fallback browser automation.

Risk: Fixed temporary-file and output-file handling could expose data or overwrite local files.

Mitigation: Use secure temporary files or stdin, validate output filenames, refuse unexpected overwrites, and make the save location explicit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/zeelin-auto-ppt)
- [Publisher profile](https://clawhub.ai/user/kelcey2023)
- [Google NotebookLM](https://notebooklm.google.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown instructions with inline bash commands and a generated local PDF file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be saved as PDF files on the user's Desktop through NotebookLM automation.]

## Skill Version(s):

4.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
