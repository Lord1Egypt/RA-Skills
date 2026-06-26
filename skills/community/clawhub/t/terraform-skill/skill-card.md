## Description: <br>
Use when working with Terraform or OpenTofu - creating modules, writing tests (native test framework, Terratest), setting up CI/CD pipelines, reviewing configurations, choosing between testing approaches, debugging state issues, implementing security scanning (trivy, checkov), or making infrastructure-as-code architecture decisions <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmy974](https://clawhub.ai/user/jimmy974) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to design, test, review, and operate Terraform or OpenTofu modules, environments, CI/CD workflows, and security checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CI/CD, apply, or cleanup snippets may affect real infrastructure if run in the wrong account, workspace, or environment. <br>
Mitigation: Verify the active account and workspace, require manual approval for production applies, and add dry-run or confirmation safeguards for destructive commands. <br>
Risk: Infrastructure tests or examples may use credentials or create cloud resources with cost or security impact. <br>
Mitigation: Use non-production credentials for tests, isolate test environments, tag test resources, and review plans before applying changes. <br>
Risk: Pipeline examples may depend on third-party actions, installers, or scanners that can change over time. <br>
Mitigation: Pin third-party actions and installers to trusted versions and review updates before adoption. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jimmy974/terraform-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jimmy974) <br>
- [Terraform Language documentation](https://developer.hashicorp.com/terraform/docs) <br>
- [Terraform testing documentation](https://developer.hashicorp.com/terraform/language/tests) <br>
- [OpenTofu documentation](https://opentofu.org/docs/) <br>
- [Code Patterns & Structure](references/code-patterns.md) <br>
- [Module Development Patterns](references/module-patterns.md) <br>
- [Testing Frameworks - Detailed Guide](references/testing-frameworks.md) <br>
- [CI/CD Workflows for Terraform](references/ci-cd-workflows.md) <br>
- [Security & Compliance](references/security-compliance.md) <br>
- [Quick Reference](references/quick-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Terraform, OpenTofu, CI/CD, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include infrastructure-as-code examples, test patterns, pipeline snippets, review findings, and operational recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; source skill metadata reports 1.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
