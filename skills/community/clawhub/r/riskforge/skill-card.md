## Description: <br>
RiskForge helps development, QA, and technical leads review code changes before release by identifying financial AI, LLM, Agent, RAG, runtime, dependency, security, compliance, and regression-test risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[start-fish](https://clawhub.ai/user/start-fish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and technical leads use RiskForge during code review, pre-test, pre-release quality gates, regression planning, and defect retrospectives. It produces actionable risk findings, testing strategy, fix guidance, audit evidence, and optional unit-test suggestions for code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports and repository metadata may be sent to an external HTTP service as part of the report upload workflow. <br>
Mitigation: Review before installing; avoid proprietary, regulated, or sensitive repositories unless network egress is blocked or upload behavior is removed or changed to explicit opt-in. <br>
Risk: Risk findings, line references, and test guidance may be incomplete or inaccurate for the target codebase. <br>
Mitigation: Review generated findings, run the relevant tests, and verify high-severity recommendations before using the report for release decisions. <br>


## Reference(s): <br>
- [RiskForge on ClawHub](https://clawhub.ai/start-fish/riskforge) <br>
- [Dependency Impact Analyzer](references/dependency-impact-analyzer.md) <br>
- [Financial AI Risk Playbook](references/financial-ai-risk-playbook.md) <br>
- [Git Diff Skill](references/git-diff-skill.md) <br>
- [QA Methodology](references/qa-methodology.md) <br>
- [Risk Backtracking Validator](references/risk-backtracking-validator.md) <br>
- [Runtime Exception Detector](references/runtime-exception-detector.md) <br>
- [Test Reports](references/test-reports/test-reports.md) <br>
- [Report Upload Platform](references/test-reports/upload-platform.md) <br>
- [Unit Testing](references/unit-testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown risk and test reports with structured JSON blocks, optional unit-test code, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include severity-ranked findings, file and line references, validation notes, risk statistics, prioritized recommendations, and optional upload handling.] <br>

## Skill Version(s): <br>
6.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
