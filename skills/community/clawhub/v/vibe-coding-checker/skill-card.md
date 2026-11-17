## Description:

描述一个功能或项目，AI 快速评估用 Cursor/Windsurf/Bolt 等 AI 编程工具能否独立实现，给出可行性判断、推荐工具、拆解路径和风险提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product builders use this skill to evaluate whether a proposed feature or project can be completed with AI coding tools, choose suitable tools, split work into implementation steps, and identify likely risks before starting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an OPENAI_API_KEY value while sending requests to the DeepSeek API endpoint by default.

Mitigation: Run it in a minimal environment with only the intended DeepSeek key set, or explicitly configure the API base and model before use.

Risk: Project idea text may be sent to an external API, and the skill does not clearly disclose or constrain that data flow.

Mitigation: Avoid confidential product plans, customer data, internal architecture, and secrets in prompts until the external API handling is reviewed and disclosed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonia-sz/skills/vibe-coding-checker)
- [ClawHub publisher profile](https://clawhub.ai/user/antonia-sz)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown feasibility report in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a feasibility conclusion, dimension scores, recommended AI coding tools, task breakdown, risk notes, and practical suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
