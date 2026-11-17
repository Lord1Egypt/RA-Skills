## Description:

Chinese-language xuanhuan novel creation workflow that coordinates outlining, drafting, review, revision, and final TXT formatting for fantasy fiction projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writers use this skill to generate long-form Chinese xuanhuan, xianxia, cultivation, and fantasy novels from minimal prompts or existing partial drafts. The workflow produces direction notes, outline discussion, integrated outlines, chapter drafts, review reports, revisions, and a final formatted TXT manuscript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create many local Markdown files and a final TXT manuscript in its workspace.

Mitigation: Run it in a dedicated project workspace and review or back up existing workspace files before use.

Risk: The workflow makes autonomous creative decisions without asking clarifying questions.

Mitigation: Provide explicit story constraints in the prompt when particular themes, characters, boundaries, or output scope are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongzichixiangjiao/skills/xuanhuan-novel-master)
- [README](artifact/README.md)
- [Main skill definition](artifact/SKILL.md)
- [Outline reviewer: 天蚕土豆](artifact/references/01-天蚕土豆/SKILL.md)
- [Outline reviewer: 我吃西红柿](artifact/references/02-我吃西红柿/SKILL.md)
- [Outline reviewer: 猫腻](artifact/references/03-猫腻/SKILL.md)
- [Outline reviewer: 烽火戏诸侯](artifact/references/04-烽火戏诸侯/SKILL.md)
- [Draft writer](artifact/references/05-写手/SKILL.md)
- [Review checker](artifact/references/06-检查/SKILL.md)
- [Formatter](artifact/references/07-排版/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown process files and UTF-8 TXT manuscript output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and resumes files under a local xuanhuan-novel-master-workspace directory and writes final TXT output under assets/output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
