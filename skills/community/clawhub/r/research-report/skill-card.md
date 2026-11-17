## Description:

Research technical projects/papers and generate comprehensive reports with PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaruoji](https://clawhub.ai/user/huaruoji)

### License/Terms of Use:


## Use Case:

Developers, engineers, and researchers use this skill to scaffold technical research reports for papers or projects, with optional local code analysis and PDF export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate its research capability because the script primarily scaffolds notes, report files, logs, and PDF conversion rather than completing substantive research automatically.

Mitigation: Review and edit generated reports before relying on them, and treat the output as a starting draft rather than a completed research deliverable.

Risk: Untrusted topic text is written into generated report, log, and memory files.

Mitigation: Use the skill only in private, trusted workspaces; avoid untrusted or multiline topic input; and inspect or remove generated memory entries after use.

Risk: The artifact mentions Telegram delivery without clearly implementing or scoping that delivery path.

Mitigation: Treat any external delivery step as requiring separate explicit consent and review before sending generated reports outside the workspace.

## Reference(s):

- [Report Template](references/report-template.md)
- [ClawHub skill page](https://clawhub.ai/huaruoji/skills/research-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, optional PDF files, logs, and memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pandoc for PDF output; full mode may require conda, dependencies, and manual experiment setup.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
