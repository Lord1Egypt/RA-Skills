## Description:

Analyzes ZenTao bug reports from Feishu-triggered links by gathering bug details, attachments, logs, local code context, and producing a root-cause report with optional ZenTao and Feishu updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeah526](https://clawhub.ai/user/yeah526)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to triage ZenTao defects, identify the affected module and branch, inspect logs and attachments, and prepare a concise root-cause analysis. It can also format the report for ZenTao comments and send a Feishu summary when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires sensitive ZenTao credentials and broad local/browser authority.

Mitigation: Use a low-privilege ZenTao account, HTTPS, isolated disposable worktrees or containers, and pinned dependencies; do not store real passwords in workspace config until credential handling and CDP/browser exposure are fixed.

Risk: Automatic ZenTao comments could publish incomplete or incorrect analysis.

Mitigation: Review generated reports before posting, and set auto_comment to false when manual approval is required.

Risk: Bug analysis can modify local repository state through checkout or worktree operations.

Mitigation: Run analysis in disposable or isolated worktrees and verify cleanup of worktrees, browser sessions, and ZenTao helper processes after each run.

## Reference(s):

- [ZenTao API Reference](artifact/references/zentao-api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/yeah526/skills/zentao-bug-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with shell command guidance, JSON metadata, HTML comment output, and Feishu-ready text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local bug artifacts such as downloaded attachments, extracted video frames, time metadata, reports, and comment HTML.]

## Skill Version(s):

1.1.0 (source: server release metadata; target metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
