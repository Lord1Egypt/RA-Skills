## Description: <br>
生成结构精简的 Claude Code skill 骨架，强制 routing-signal 三要素、五类 body taxonomy 和 Faithfulness gate，并在用户要求起草、设计、新建或 scaffold skill 时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[david0ming](https://clawhub.ai/user/david0ming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to turn a skill idea into a concise Claude Code skill scaffold with routing signals, taxonomy checks, split Markdown files, and an architect report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skill files may encode incomplete or unsuitable guidance for the intended agent workflow. <br>
Mitigation: Review the generated files and architect report before installing or relying on the scaffold. <br>
Risk: The skill writes files to a user-selected output path. <br>
Mitigation: Use a dedicated output directory and confirm the generated path before adopting the files. <br>
Risk: The README includes remote install commands that depend on external package or repository identity. <br>
Mitigation: Verify the remote repository or package source before running git, npx, or ClawHub install commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/david0ming/skill-scaffolder) <br>
- [SkillReducer paper](https://arxiv.org/abs/2603.29919) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown skill files and concise implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a scaffold to a user-chosen path and uses an alternate .new directory when the target already exists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
