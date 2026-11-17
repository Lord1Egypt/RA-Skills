## Description:

RiskForge analyzes code changes for financial AI, LLM, Agent, RAG, runtime, dependency, security, compliance, performance, and regression risks, then produces test strategy, audit evidence, unit-test suggestions, and standardized reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[start-fish](https://clawhub.ai/user/start-fish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and technical leads use this skill before code review, test handoff, and release gates to identify code-risk findings, prioritize validation work, and produce auditable test reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill uploads detailed reports and local project metadata to a fixed plaintext HTTP service without clear per-run consent.

Mitigation: Review before installing; for private, enterprise, regulated, or security-sensitive repositories, require explicit approval, local-only operation, HTTPS, and payload redaction before any upload.

Risk: Generated reports may include file paths, repository identifiers, tester metadata, issue details, and full report content.

Mitigation: Treat reports as potentially sensitive, redact confidential content, and restrict use to repositories where this data can be shared with the configured external service.

## Reference(s):

- [RiskForge ClawHub Skill Page](https://clawhub.ai/start-fish/skills/riskforge)
- [README](README.md)
- [Dependency Impact Analyzer](references/dependency-impact-analyzer.md)
- [Financial AI Risk Playbook](references/financial-ai-risk-playbook.md)
- [Git Diff Skill](references/git-diff-skill.md)
- [QA Methodology](references/qa-methodology.md)
- [Risk Backtracking Validation Protocol](references/riREDACTED-SECRET.md)
- [Runtime Exception Detector](references/runtime-exception-detector.md)
- [Test Reports Template](references/test-reports/test-reports.md)
- [Test Report Upload Platform Guide](references/test-reports/upload-platform.md)
- [Unit Testing](references/unit-testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with structured JSON blocks, inline code, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include risk severity, code locations, validation notes, test strategy, remediation guidance, and optional unit-test recommendations.]

## Skill Version(s):

6.1.4 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
