## Description: <br>
将剧本文本工业化转换为 Seedance 2.0 可用的视频提示词，包括文生图提示词、分组视频提示词、台词核对表和字段自检表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccx060918](https://clawhub.ai/user/ccx060918) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
创作者和视频制作人员用它将剧本或故事文本转化为 Seedance 2.0 的角色、场景、道具文生图提示词、分组视频提示词和核对表。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a Markdown file in the working directory, which could overwrite or place generated content in an unintended location. <br>
Mitigation: Confirm the target filename and directory before use, and run it in a workspace where generated prompt files are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccx060918/seedance-prompt-gen) <br>
- [视频提示词工业化生成工作流 SKILL](references/视频提示词工业化生成工作流SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, files] <br>
**Output Format:** [Markdown file containing image prompts, grouped video prompts, dialogue checks, and field self-check tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the completed prompt package to a .md file and reports the path, total groups, and total duration.] <br>

## Skill Version(s): <br>
1.9.2 (source: server evidence release.version and artifact version text) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
