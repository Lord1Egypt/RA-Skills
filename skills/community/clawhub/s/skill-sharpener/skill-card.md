## Description:

Skill Sharpener evaluates existing Agent Skill packages and produces quality scores, issue findings, and optimization recommendations for skill metadata, structure, content, examples, and scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxxxu](https://clawhub.ai/user/liuxxxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to audit and improve Agent Skills before release or refactoring. It reviews SKILL.md, references, and scripts, then reports quality scores, priority issues, strengths, and description improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads target skill directories and runs a local Python analyzer.

Mitigation: Use it only on trusted skill folders and avoid directories containing secrets.

Risk: The skill can modify skill files after confirmation.

Mitigation: Review proposed changes before allowing rewrites or refactors, and keep backups for edited files.

Risk: The file-tree scanner can escape intended boundaries through symlinks.

Mitigation: Avoid running it on folders that contain symlinks to private or unrelated locations.

## Reference(s):

- [Skill quality checklist](references/checklist.md)
- [Claude Agent Skills best practices](https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/best-practices)
- [TRAE skill writing best practices](https://docs.trae.cn/ide/best-practice-for-how-to-write-a-good-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with tables, issue lists, suggested description text, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to skill files after review and user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
