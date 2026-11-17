## Description:

Presentation creation, editing, and analysis for creating new PowerPoint files, modifying existing presentations, working with layouts, and adding comments or speaker notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicky1108](https://clawhub.ai/user/nicky1108)

### License/Terms of Use:

Proprietary

## Use Case:

Employees, external users, developers, and agent operators use this skill to create, inspect, edit, validate, and package PowerPoint presentations through HTML-to-PPTX and Office Open XML workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes Office files and includes broader DOCX/XLSX code paths beyond normal PowerPoint tasks.

Mitigation: Review the bundled Office-document scripts before installation and limit use to the presentation workflows needed for the deployment.

Risk: Untrusted PPTX, DOCX, or XLSX files can expose archive extraction and XML parsing risks.

Mitigation: Run the skill in an isolated, non-admin environment, work on copies of documents, keep backups, and harden archive extraction and XML parsing before handling untrusted files.

Risk: The artifact includes privileged or globally scoped dependency setup guidance.

Mitigation: Pre-provision and pin dependencies instead of allowing agents to run sudo or global install commands during routine workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicky1108/skills/x-92bilal26-pptx)
- [Skillstore skill page](https://skillstore.io/skills/x-92bilal26-pptx)
- [HTML to PowerPoint Guide](html2pptx.md)
- [Office Open XML Technical Reference for PowerPoint](ooxml.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, generated scripts, JSON inventories, thumbnails, and PowerPoint files when the agent executes the workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presentation workflows may create or modify .pptx files and supporting temporary files.]

## Skill Version(s):

1.0.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
