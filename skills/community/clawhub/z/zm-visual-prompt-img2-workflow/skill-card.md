## Description: <br>
ZM IMG2 视觉提示词编排。用于把漫画页、PPT 主视觉、封面/配图等结构化视觉需求，编译为可执行的 happy/gpt-image-2 提示词，并检查参考图、主角图、风格、禁止项和 IMG2 生产证据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and visual content agents use this skill to turn structured comic, cover, presentation, or illustration briefs into concise IMG2-ready prompts. It also records reference images, forbidden items, execution commands, and run summaries so reviewers can check whether a visual request is ready or blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates actual image generation to a downstream image skill, and the evidence notes inconsistent dependency names. <br>
Mitigation: Confirm that the intended downstream image skill is installed, reviewed, and matches the command path before running with --run. <br>
Risk: Prompts and reference images may be sent to the configured Happy/OpenAI-compatible image provider during actual runs. <br>
Mitigation: Review prompts and reference image paths for sensitive or restricted content before enabling --run. <br>
Risk: Missing or inappropriate reference images can block or distort IMG2 output. <br>
Mitigation: Use the required-field checklist and built-in reference-image validation before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-visual-prompt-img2-workflow) <br>
- [Configured Happy OpenAI-compatible image provider endpoint](https://sub2api.happyhourse.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text prompts, JSON run artifacts, and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compiler runs create compiled_prompt.txt, request.json, result.json, run_command.md, stdout.txt, stderr.txt, and summary.json; image generation is delegated to a downstream IMG2 skill when --run is used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json; artifact SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
