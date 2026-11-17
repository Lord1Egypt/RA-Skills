## Description:

Reviews Terraform, OpenTofu, and Terragrunt plan output for destructive changes, drift, secret exposure, IAM permission widening, public exposure, and provider-specific risks, then produces severity-graded findings, a gating decision, and suggested fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and platform engineers use this skill to review Terraform, OpenTofu, or Terragrunt plans before apply in PR, CI/CD, and manual infrastructure change-review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CI workflow examples may use external GitHub Actions or broad workflow permissions.

Mitigation: Pin external actions to reviewed commit SHAs and set least-privilege workflow permissions before adopting generated CI configuration.

Risk: Backup or pre-apply checklist guidance may reference storage destinations that are unsafe for a user's environment.

Mitigation: Verify any backup destination is owned and trusted before using it for state, plan, or infrastructure data.

## Reference(s):

- [Terraform Plan Reviewer on ClawHub](https://clawhub.ai/charlie-morrison/skills/terraform-plan-reviewer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown review comments, optional JSON gating decisions, and CI or runbook snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes P0/P1/P2 findings, an apply gating decision, line citations when available, and suggested fixes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
