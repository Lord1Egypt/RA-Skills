## Description:

Use when bulk-managing Terraform modules at scale across AWS, GCP, Azure, and DigitalOcean repositories, including provider upgrades, GitHub Actions standardization, semantic releases, security scans, and end-to-end maintenance cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure engineers use this skill to coordinate bulk Terraform module maintenance across cloud-provider repositories, including version updates, validation, workflow changes, and release preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk repository automation can modify Terraform files, create commits, push tags, and publish GitHub releases across matching repositories.

Mitigation: Run first in a disposable checkout or sandbox, verify the exact repository list, and manually review diffs, branches, tags, releases, and workflow changes before organization-wide execution.

Risk: Documented safety controls such as DRY_RUN and CREATE_PR may be missing or unenforced by the shipped scripts.

Mitigation: Do not rely on those controls until reviewed and fixed; use passive, reviewed configuration files and external review gates.

Risk: GitHub tokens with broad repository or workflow permissions increase the impact of mistakes during release or workflow automation.

Mitigation: Use fine-grained, repository-scoped tokens with the minimum required permissions and keep audit logging enabled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anmolnagpal/skills/terraform-ai-skills)
- [Project Homepage](https://github.com/anmolnagpal/terraform-ai-skills)
- [Safety and Rollback Reference](references/safety.md)
- [Provider Configs Reference](references/provider-configs.md)
- [Real-World Examples](references/examples.md)
- [Quick Reference](references/quick-reference.md)
- [Usage Guide](docs/USAGE.md)
- [Environment Variables Reference](docs/ENV-VARS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repository maintenance plans, validation steps, changelog text, commit guidance, and commands for Terraform and GitHub workflows.]

## Skill Version(s):

0.0.2 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
