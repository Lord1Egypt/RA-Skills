## Description:

Guides developers in publishing selected workspace files to a Git remote without exposing unrelated files or secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanmeng9527](https://clawhub.ai/user/huanmeng9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check repository boundaries, stage only intended project files, and publish them to a Git remote. It also describes a GitHub Contents API fallback when pushes repeatedly time out.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing the wrong files or using the wrong repository visibility could expose secrets or unrelated workspace content.

Mitigation: Confirm the project directory and repository visibility, then review the final staged file list for secrets and unrelated files before uploading.

Risk: Publishing a project nested inside a parent Git repository could include files outside the intended project.

Mitigation: Compare the Git top-level directory with the target directory and use an isolated repository for a nested project.

Risk: The GitHub Contents API fallback uploads selected files using active GitHub CLI credentials.

Mitigation: Inspect each selected file for credentials and unrelated content before using the fallback.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/huanmeng9527/skills/safe-git-push)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell examples and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
