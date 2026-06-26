## Description: <br>
评估并优化简历内容，输出精美的 HTML 修改建议报告。当用户提到"修改简历"、"优化简历"、"简历评估"时使用。支持前端和后端岗位，Claude 以前端/后端架构师视角进行评估，让用户清楚知道哪些部分需要优化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifenglei](https://clawhub.ai/user/lifenglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate frontend or backend engineering resumes from an architect's perspective and produce an HTML improvement report with scores, project feedback, and optimization advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume text may contain personal, contact, employment, or other sensitive information and is sent to the configured Claude/Anthropic-compatible provider for evaluation. <br>
Mitigation: Redact sensitive resume details before use, confirm the provider is acceptable for the data, and run the Python dependencies in an isolated environment with reviewed pinned versions. <br>


## Reference(s): <br>
- [Frontend Resume Evaluation Criteria](references/frontend-evaluation.md) <br>
- [Backend Resume Evaluation Criteria](references/backend-evaluation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [HTML report generated from extracted PDF text and model-produced JSON feedback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-selected PDF resume, a frontend or backend role choice, Python dependencies, and an Anthropic-compatible API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
