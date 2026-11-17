## Description:

Implements six universal, language-agnostic quality gates for APIs, web apps, and CI/CD pipelines using repository-configured checks and detailed reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thecybercore](https://clawhub.ai/user/thecybercore)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to evaluate repository build health, test coverage, security posture, performance, maintainability, and release readiness before unattended agent changes are shipped.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update quality-gateway configuration and report files in a repository.

Mitigation: Run it on a clean branch and review generated docs/quality, .defs, and .tmp/quality-gates changes before committing.

Risk: Quality-gateway results depend on the availability and accuracy of project evidence and CI artifacts.

Mitigation: Review report evidence references and treat unknown or missing security metrics according to the configured fallback rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thecybercore/skills/tcc-quality-gates)
- [Quality gateway definition template](artifact/templ/quality-gateway-definition-template.json)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown report, JSON report, and repository-relative evidence references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default outputs are docs/quality/quality-gate-report.md, docs/quality/quality-gate-report.json, and docs/quality/evidence/ when not overridden by configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
