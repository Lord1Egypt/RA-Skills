## Description:

将剧本文本工业化转换为 Seedance 2.0 可用的视频提示词，包括文生图提示词、分组视频提示词、台词核对表和字段自检表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccx060918](https://clawhub.ai/user/ccx060918)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to turn Chinese scripts or story text into Seedance 2.0-ready video prompt packages with image prompts, grouped shot prompts, dialogue checks, and field self-checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save large generated Markdown prompt files and could overwrite existing files if the output path is not controlled.

Mitigation: Specify the output path before execution and require confirmation before overwriting an existing file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccx060918/skills/seedance-prompt-gen)
- [视频提示词工业化生成工作流SKILL.md](references/视频提示词工业化生成工作流SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown file containing image prompts, grouped video prompts, dialogue check tables, and field self-check tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the completed prompt package to a Markdown file and reports only the file path, group count, and total duration.]

## Skill Version(s):

1.9.2 (source: release evidence and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
