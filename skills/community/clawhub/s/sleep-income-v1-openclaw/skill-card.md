## Description:

Helps OpenClaw users plan repeatable AI-assisted workflows for WeChat article drafting, digital product packaging, marketplace asset publication, and feedback-driven iteration toward passive income.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suda6632](https://clawhub.ai/user/suda6632)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users with WeChat Official Account access use this skill to organize repeatable AI-assisted content and digital product workflows, including draft production, package creation, publishing preparation, data tracking, and feedback iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to scan local workspace content before packaging assets.

Mitigation: Restrict scans to explicit allowlists and exclude secrets, private files, and unrelated projects.

Risk: The workflow involves WeChat AppID/AppSecret values and external publication.

Mitigation: Store secrets in a secure secret store and require manual approval for uploads, draft submissions, marketplace releases, and account-impacting actions.

Risk: Security evidence marks the release suspicious because external publishing and workspace scanning lack clear review and secret-protection steps.

Mitigation: Review the package manifest and approve each account-impacting action before installation and execution.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/suda6632/skills/sleep-income-v1-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with workflow outlines, checklists, and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include monetization workflow steps and publication-preparation instructions; users should review them before external publishing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
