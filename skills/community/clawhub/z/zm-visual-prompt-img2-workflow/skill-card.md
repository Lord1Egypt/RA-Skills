## Description:

ZM IMG2 视觉提示词编排。用于把漫画页、PPT 主视觉、封面/配图等结构化视觉需求，编译为可执行的 happy/gpt-image-2 提示词，并检查参考图、主角图、风格、禁止项和 IMG2 生产证据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to turn structured visual briefs for comic pages, PPT main visuals, covers, and illustrations into concise executable IMG2 prompts. It also checks reference images, forbidden terms, and expected IMG2 run evidence before handing work to the image generation dependency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Actual runs may send local reference image paths and prompt content to the configured external image provider.

Mitigation: Use dry-run by default, restrict reference images to approved asset directories, and provide image paths only when external provider use is acceptable.

Risk: The declared generation skill dependency and the executed dependency path are not aligned in the provided evidence.

Mitigation: Align the declared and executed generation dependency before broad use.

Risk: Untrusted JSON or YAML input can influence generated prompts, file references, and run artifacts.

Mitigation: Review input specs before execution and avoid running the skill on untrusted visual briefs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jerryxn/skills/zm-visual-prompt-img2-workflow)
- [Publisher Profile](https://clawhub.ai/user/jerryxn)
- [Happy OpenAI-Compatible Image Provider Endpoint](https://sub2api.happyhourse.cn/v1)
- [AI Readiness Checklist](checklists/ai_readiness_checklist.md)
- [Minimum Required Fields](templates/minimum_required_fields.md)
- [Subagent Execution Prompt](templates/subagent_execution_prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Compiled prompt text, Markdown command blocks, and JSON run artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compiled_prompt.txt, request.json, result.json, run_command.md, stdout.txt, stderr.txt, and summary.json in a compiler run directory.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
