## Description: <br>
职业规划未来镜像系统：收集用户信息，生成3条差异化职业路径的Awwwards级HTML报告，构建'3年后的自己'进行镜像对话，生成《来自未来的信》沉浸式HTML页面。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for Chinese-language career planning when they are exploring early-career choices, career transitions, bottlenecks, or returning to work. It gathers career background and preferences, proposes three differentiated career paths, supports a future-self dialogue, and generates HTML career-report and future-letter files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for resume-like details, income expectations, and personal career doubts. <br>
Mitigation: Use only with information the user is comfortable sharing, and avoid including unnecessary sensitive personal details. <br>
Risk: The skill silently saves future-self dialogue to output/data/conversation_log.json. <br>
Mitigation: Tell the agent not to silently save conversation logs, review the generated file, and delete it after use when retention is not needed. <br>
Risk: Generated HTML reports may contact third-party CDN and font services when opened online. <br>
Mitigation: Review the generated HTML before opening or sharing it, and remove or self-host external font, Tailwind, Chart.js, and Alpine.js resources where appropriate. <br>


## Reference(s): <br>
- [Career survey data](reference/career_survey_data.json) <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/yq-career-future-mirror) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese-language Markdown responses with inline shell commands, JSON snippets, and generated HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates output/reports/career_report.html, output/reports/future_letter.html, and output/data/conversation_log.json during the guided workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
