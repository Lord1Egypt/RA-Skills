## Description:

指导开发者预检技能包、发布到 SkillHub 和 ClawHub 并核对发布状态；平台因安全原因拒绝时，指导停止操作并联系官方支持或申诉。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to prepare and publish local agent skills to SkillHub and ClawHub, confirm review and publication status, and diagnose common packaging or metadata errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags concerns involving installer verification and authenticated requests.

Mitigation: Independently verify the installer and confirm authenticated requests go only to trusted destinations before using credentials.

Risk: Collecting files for a release could include unintended local content.

Mitigation: Review the dry-run file list and confirm the package contains only the intended skill files.

Risk: The skill includes deletion and GitHub publishing capabilities beyond basic package preparation; deletion is irreversible.

Mitigation: Review these actions against the task, verify the target before deletion, and use the explicit delete confirmation only when permanent removal is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oracis/skills/skillhub-publish-skill)
- [SkillHub CLI publishing tutorial](https://skillhub.cn/tutorials#publish-via-cli)
- [Publishing and release status workflow](SKILL.md)
- [ClawHub categories and topics](references/clawhub-catalog.md)
- [GitHub repository workflow](references/github-repo.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, JSON]

**Output Format:** [Markdown guidance with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preflight findings, packaging instructions, and release status checks.]

## Skill Version(s):

1.7.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
