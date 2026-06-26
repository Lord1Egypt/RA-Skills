## Description: <br>
Provides automated testing and integration validation for OpenClaw's skill management in agency-agents projects with error handling and logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyzhao0609](https://clawhub.ai/user/dannyzhao0609) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to validate OpenClaw skill management workflows, API behavior, accessibility, performance, test evidence, tool choices, workflow quality, and release readiness for agency-agents projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad testing and data-handling authority. <br>
Mitigation: Constrain use to authorized local or staging systems unless production testing is formally approved. <br>
Risk: Generated test scripts or shell commands may run tools in ways the operator did not intend. <br>
Mitigation: Review proposed commands and local scripts before execution, and pin external CLI tools where possible. <br>
Risk: Screenshots, logs, and reports may capture secrets or real user data. <br>
Mitigation: Use non-production data by default, redact sensitive content, and keep generated evidence out of public or committed locations unless reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dannyzhao0609/testing-agency-agents-huyue) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Accessibility Auditor](artifact/testing-accessibility-auditor.md) <br>
- [API Tester](artifact/testing-api-tester.md) <br>
- [Evidence Collector](artifact/testing-evidence-collector.md) <br>
- [Performance Benchmarker](artifact/testing-performance-benchmarker.md) <br>
- [Reality Checker](artifact/testing-reality-checker.md) <br>
- [Test Results Analyzer](artifact/testing-test-results-analyzer.md) <br>
- [Tool Evaluator](artifact/testing-tool-evaluator.md) <br>
- [Workflow Optimizer](artifact/testing-workflow-optimizer.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with code examples, shell commands, JSON examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce testing reports, validation checklists, remediation guidance, screenshots or references to visual evidence, and implementation recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
