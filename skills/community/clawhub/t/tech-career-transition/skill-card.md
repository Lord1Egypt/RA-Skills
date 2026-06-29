## Description: <br>
计算机行业转行规划助手通过30道交互式问题评估技术深度、学习能力、业务理解、沟通协作、市场匹配和转行驱动力，并基于18个转行方向生成匹配度分析、技能差距、12个月路线图和交互式HTML报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT and computer-industry workers use this skill to explore career-transition options, compare 18 target directions, and receive a personalized readiness assessment with a practical transition plan. The skill is especially suited to users considering moves from engineering roles into architecture, AI, product, security, management, government or state-owned IT, independent development, consulting, training, or content roles. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The generated HTML report can contain sensitive personal career history, salary expectations, education, and risk-tolerance details. <br>
Mitigation: Store the report only in an appropriate workspace, review its contents before sharing, and delete it when the personal planning record is no longer needed. <br>
Risk: Opening the report may load Chart.js from a third-party CDN. <br>
Mitigation: Open the report only in environments where external CDN loading is acceptable, or replace the CDN dependency before using it in a restricted environment. <br>
Risk: Career-transition recommendations may be incomplete or misleading if the user's answers are vague, outdated, or missing important personal constraints. <br>
Mitigation: Treat the result as planning guidance, verify recommendations against current market information and personal constraints, and seek human career or domain review before making major decisions. <br>


## Reference(s): <br>
- [计算机行业转行路径图谱](references/career_paths.md) <br>
- [计算机行业转行能力评估框架](references/competency_framework.md) <br>
- [转行方向匹配矩阵](references/transition_matrix.md) <br>
- [HTML report template](assets/report_template.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Interactive Chinese Q&A followed by a local HTML report and a concise Markdown summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report is written as a timestamped HTML file and may load Chart.js from a third-party CDN when opened.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
