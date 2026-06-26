## Description: <br>
Implements six universal, language-agnostic quality gates for APIs, web apps, and CI/CD pipelines using repository-configured checks and detailed reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheCyberCore](https://clawhub.ai/user/TheCyberCore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to evaluate application repositories against build, testing, security, performance, maintainability, and release-readiness gates. It helps produce consistent quality-gate configuration, reports, scores, statuses, and evidence references for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated quality-gate configuration, thresholds, or reports may influence release decisions before they are reviewed. <br>
Mitigation: Review generated files, thresholds, evidence paths, and reports before committing them or using them in CI/CD gates. <br>
Risk: The skill may read repository and CI evidence and write local configuration, temporary files, evidence, and reports under documented project paths. <br>
Mitigation: Run it only in an intended repository workspace and inspect generated outputs before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheCyberCore/tcc-quality-gates) <br>
- [quality-gateway-definition-template.json](artifact/templ/quality-gateway-definition-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Configuration, Guidance, Evidence references] <br>
**Output Format:** [Markdown and JSON reports with repository-relative evidence paths and configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written to configured repository paths, with temporary work kept under .tmp/quality-gates/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
