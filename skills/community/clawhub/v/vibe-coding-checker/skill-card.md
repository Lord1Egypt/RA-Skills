## Description: <br>
描述一个功能或项目，AI 快速评估用 Cursor/Windsurf/Bolt 等 AI 编程工具能否独立实现，给出可行性判断、推荐工具、拆解路径和风险提示。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to assess whether a proposed feature or project is suitable for AI-assisted coding tools. It returns feasibility, recommended tools, task decomposition, time estimates, and implementation risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project descriptions and API credentials may be sent to a remote LLM service. <br>
Mitigation: Review the skill before use, set API_BASE deliberately, and use a provider-specific API key with limited scope. <br>
Risk: Sensitive business, customer, proprietary, or regulated information could be included in the project description. <br>
Mitigation: Do not submit secrets or sensitive data in prompts; redact project details before running the evaluator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antonia-sz/vibe-coding-checker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/antonia-sz) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown feasibility report with optional CLI invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language report with feasibility rating, scoring table, recommended tools, decomposition path, risk notes, and practical advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
