## Description:

生成结构精简的 Claude Code skill 骨架，强制 routing-signal 三要素、五类 body taxonomy 和 Faithfulness gate。

This skill is ready for commercial/non-commercial use.

## Publisher:

[david0ming](https://clawhub.ai/user/david0ming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this agent skill to turn a skill idea into a concise Claude Code skill scaffold. It produces a day-zero structure with routing signals, taxonomy checks, split-file frontmatter, and a Faithfulness audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes scaffold files into a target directory, so an incorrect target path can create files in an unintended location.

Mitigation: Provide a fresh target directory and review generated files before enabling or publishing the scaffolded skill.

Risk: The README includes an unpinned npx install command, which may resolve changing installer behavior over time.

Mitigation: Prefer ClawHub or a reviewed pinned installer before installing the skill.

Risk: Broad trigger wording can cause the skill to activate for general skill-authoring discussions where a full scaffold is not needed.

Mitigation: Use it only when intentionally creating a new skill scaffold, and retire ideas that can be handled by the base model, an existing tool, or CLAUDE.md rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/david0ming/skills/skill-scaffolder)
- [SkillReducer: A Two-Stage Compression Method for Agent Skills](https://arxiv.org/abs/2603.29919)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown files and structured scaffold content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a new skill directory with SKILL.md, optional background.md, examples.md, templates.md, and ARCHITECT_REPORT.md; avoids overwriting an existing target directory by writing to a .new directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
