## Description: <br>
Reviews Terraform, OpenTofu, and Terragrunt plan output for destructive changes, drift, secret exposure, IAM widening, public exposure, and cloud-provider risk, then returns severity-graded findings, a gating decision, line-cited fixes, and optional CI review configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and platform engineering teams use this skill to review Terraform, OpenTofu, or Terragrunt plans before apply, especially for PR gating, drift triage, destructive-change review, IAM widening checks, and cloud-exposure risk review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terraform plans, state summaries, or generated review artifacts may expose secrets or sensitive infrastructure details. <br>
Mitigation: Redact secrets and avoid pasting full state unless necessary. <br>
Risk: Generated CI workflows, hooks, or gating configuration may not match the repository's operational controls. <br>
Mitigation: Manually review generated workflow or hook changes before committing them. <br>
Risk: Production or destructive Terraform applies can cause outages, data loss, or security exposure if acted on without review. <br>
Mitigation: Keep human approval for production or destructive applies, and use the skill's blocking and approval-with-conditions decisions as review inputs. <br>


## Reference(s): <br>
- [Terraform Plan Reviewer ClawHub release](https://clawhub.ai/charlie-morrison/terraform-plan-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown review comments, JSON gating decisions, CI configuration, Slack summaries, and runbook checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity-graded findings, line citations, suggested fixes, drift commands, pre-apply checklists, and CI workflow snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
