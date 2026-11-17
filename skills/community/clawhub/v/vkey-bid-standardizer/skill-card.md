## Description:

Standardizes Chinese banking bid-response DOCX documents by applying Word heading/body styles, GB/T 9704-style formatting, numbering repair, Markdown conversion, and JSON review reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyonghui0810](https://clawhub.ai/user/wuyonghui0810)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers preparing banking bid responses use this skill to normalize DOCX layout, heading hierarchy, numbering, tables, footers, and review outputs before submission.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Install metadata creates an avoidable dependency-resolution risk for Python dependencies.

Mitigation: Review the install path before use and prefer pinned Python requirements or a lock file instead of allowing an npm installer to resolve Python packages.

Risk: The skill processes sensitive bid documents and can write modified document files.

Mitigation: Run it only on user-selected document copies and use --dry-run or --backup before changing files that contain sensitive bid material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuyonghui0810/skills/vkey-bid-standardizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, CLI commands, JSON review reports, and standardized DOCX or Markdown-derived document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews and backup output handling for user-selected document files.]

## Skill Version(s):

1.0.1 (source: server release evidence; package metadata lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
