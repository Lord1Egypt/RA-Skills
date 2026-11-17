## Description:

简历生成技能（W工作室）通过结构化信息收集生成 Reactive Resume v2 JSON, 可导入 aicv.weinuo.work 创建 PDF 简历。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xk103295870-alt](https://clawhub.ai/user/xk103295870-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to collect resume details, generate a Reactive Resume v2 JSON file, and prepare supporting resume outputs for review, import, or export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill states resume data is processed locally while also directing users to upload generated resume JSON to an external import site.

Mitigation: Review generated JSON before upload and use the external aicv.weinuo.work workflow only when sharing the contained personal resume data is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xk103295870-alt/skills/resume-gen-ws)
- [AI resume platform](https://aicv.weinuo.work)
- [Reactive Resume schema](https://rxresu.me/schema.json)
- [Reactive Resume](https://rxresu.me)
- [Local Reactive Resume schema reference](references/schema.md)
- [Local resume template reference](references/template.md)

## Skill Output:

**Output Type(s):** [guidance, JSON, markdown, files]

**Output Format:** [Structured prompts and generated Reactive Resume v2 JSON, with optional Markdown backup and PDF output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Resume outputs can contain personal contact details, education, work history, and other sensitive profile data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
