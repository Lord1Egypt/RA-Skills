## Description:

Use when working with Terraform or OpenTofu to create modules, write tests, set up CI/CD pipelines, review configurations, choose testing approaches, debug state issues, implement security scanning, or make infrastructure-as-code architecture decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmy974](https://clawhub.ai/user/jimmy974)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to get Terraform and OpenTofu guidance for module architecture, testing strategy, CI/CD workflows, security scanning, and production infrastructure reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready examples may run mutable remote code through installers or unpinned CI actions.

Mitigation: Inspect installer scripts before use and pin third-party actions, tools, and dependencies to approved versions.

Risk: Generated Terraform commands or cleanup scripts may change or destroy infrastructure with weak safeguards.

Mitigation: Use sandbox accounts, manual plan review, state protections, and approval gates before apply or destroy operations.

Risk: Guidance may lead to secret or state handling mistakes if copied without adaptation.

Mitigation: Use least-privilege credentials, approved secret stores, encrypted remote state, and access controls for plans and state files.

Risk: Generated documentation may include attribution defaults that are not appropriate for the adopting project.

Mitigation: Review and edit generated attribution text to match project policy before release.

## Reference(s):

- [Terraform Skill on ClawHub](https://clawhub.ai/jimmy974/skills/terraform-skill)
- [Quick Reference](references/quick-reference.md)
- [Module Development Patterns](references/module-patterns.md)
- [Testing Frameworks](references/testing-frameworks.md)
- [CI/CD Workflows](references/ci-cd-workflows.md)
- [Security & Compliance](references/security-compliance.md)
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [OpenTofu Documentation](https://opentofu.org/docs/)
- [Terraform Best Practices](https://terraform-best-practices.com)
- [Terratest Documentation](https://terratest.gruntwork.io/docs/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Terraform/OpenTofu examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations and generated snippets should be reviewed before execution in real infrastructure environments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
