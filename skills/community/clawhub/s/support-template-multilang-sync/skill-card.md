## Description:

Updates multilingual customer support reply templates in Markdown, syncs finalized content to Feishu Wiki, logs changes in GitHub, and packages the workflow for ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Support operations teams and developers use this skill to maintain multilingual support reply templates, verify placeholder consistency, publish Feishu Wiki mirrors, and prepare GitHub change logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External sync and publication steps can write support content to Feishu, GitHub, and ClawHub.

Mitigation: Require manual review and explicit approval before each Wiki sync, GitHub issue creation, skill update, or ClawHub publish.

Risk: Support templates may contain internal or customer-sensitive data.

Mitigation: Review and redact template content before sending it to external systems.

Risk: Placeholder drift across language sections can change the meaning or utility of support replies.

Mitigation: Verify every language section preserves required placeholders, aligned bullets, and clean Markdown headings before syncing.

## Reference(s):

- [Publishing Notes](references/publishing-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/support-template-multilang-sync)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown content, GitHub issue body text, Python helper output, shell commands, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Feishu, GitHub, and ClawHub credentials before external sync or publication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
