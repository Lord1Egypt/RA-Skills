## Description:

计算机行业转行规划助手通过30道交互式问题评估技术深度、学习能力、业务理解、沟通协作、市场匹配和转行驱动力，并基于18个转行方向生成个性化职业转型建议与交互式HTML报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Computer and IT professionals use this skill to evaluate career-transition readiness, compare fit across technical, product, management, public-sector, independent-development, and cross-domain paths, and receive a personalized transition roadmap. The skill is intended for Chinese-language career-planning conversations and produces recommendations for human review rather than final employment or financial decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect and place sensitive career, compensation, education, and personal-transition details into a generated local HTML report.

Mitigation: Obtain explicit user consent before report generation, warn that the report persists in the workspace, and avoid sharing the file without review.

Risk: User-provided answers may be inserted into report HTML without clear escaping or sanitization.

Mitigation: Escape or sanitize all inserted values before writing the report and review generated HTML before opening it in a networked browser.

Risk: The report template loads Chart.js from a third-party CDN.

Mitigation: Bundle Chart.js locally or use Subresource Integrity and a pinned trusted source when network loading is required.

Risk: Career guidance and readiness scores can be incomplete or misleading if treated as deterministic advice.

Mitigation: Present recommendations as decision support only and encourage users to validate market, compensation, and personal constraints before acting.

## Reference(s):

- [Career Transition Paths Catalog](references/career_paths.md)
- [Competency Assessment Framework](references/competency_framework.md)
- [Transition Matching Matrix](references/transition_matrix.md)
- [Interactive HTML Report Template](assets/report_template.html)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/tech-career-transition)
- [Publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Chinese-language conversational Q&A, structured Markdown summaries, and a generated local HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a 30-question intake, six competency scores, transition-readiness scoring, direction matching, gap analysis, learning resources, risk warnings, and a 12-month roadmap.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
