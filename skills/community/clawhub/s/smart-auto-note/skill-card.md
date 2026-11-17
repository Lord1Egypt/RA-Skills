## Description:

语义智能识别自动分类写入Obsidian笔记，支持待办自动归档

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaomiao-d](https://clawhub.ai/user/miaomiao-d)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to classify natural-language notes, todos, work records, and ideas, then append them to Obsidian-style Markdown files. It can request confirmation when classification confidence is low.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes to a fixed local folder and can create or append Markdown files there.

Mitigation: Review before installing and prefer a version with a configurable vault path scoped to the intended workspace.

Risk: The release requests messaging and scheduled-execution authority that the documentation does not clearly disclose.

Mitigation: Remove message sending and cron permissions unless they are implemented, needed, and accurately documented.

Risk: Import-time initialization may create files before a user action, and confirmation state is global.

Mitigation: Defer file creation until explicit use and scope confirmation state per user or session.

Risk: The bundled HTML documentation depends on a remote Mermaid script.

Mitigation: Document the remote dependency clearly or bundle the rendering dependency locally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miaomiao-d/skills/smart-auto-note)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Text confirmations and appended Markdown note entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends categorized Markdown files under /Users/macbook/Documents/OC_club.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
