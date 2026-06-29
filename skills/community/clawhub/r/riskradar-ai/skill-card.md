## Description: <br>
AI Code Review and Code Risk Review quality gate for Git Diff, release readiness, regression testing, security testing, dependency impact, runtime risk, LLM testing, Agentic AI risk, and RAG security. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[start-fish](https://clawhub.ai/user/start-fish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review Git diffs and source code for release risk, AI workflow risk, regression gaps, security exposure, dependency impact, and targeted test strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to inspect repository code and diffs, which may expose sensitive implementation details to the reviewing agent. <br>
Mitigation: Install and use it only when the agent is authorized to review the relevant repository content and change history. <br>
Risk: Code review guidance can be incomplete or incorrect if the agent lacks enough code, configuration, runtime, or test evidence. <br>
Mitigation: Require findings to cite concrete evidence and verify high-severity risks with reproduction steps or targeted tests before release decisions. <br>


## Reference(s): <br>
- [Code Risk Review Playbook](references/code-risk-review-playbook.md) <br>
- [ClawHub Listing](https://clawhub.ai/start-fish/riskradar-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes severity, confidence, exact code location, impact, verification steps, release recommendation, and test strategy.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
