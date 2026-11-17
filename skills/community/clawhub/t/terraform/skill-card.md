## Description:

Helps agents write, debug, refactor, and review Terraform and OpenTofu infrastructure code, including HCL, modules, plan and apply failures, state workflows, drift, provider pinning, CI gates, and recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to get Terraform and OpenTofu guidance for writing and reviewing HCL, diagnosing plan and apply failures, planning safe refactors and state recovery, and designing CI plan/apply gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terraform commands can affect real infrastructure when an agent or user executes them.

Mitigation: Review saved plans before apply and require explicit approval before apply, state push, state rm, or force-unlock.

Risk: State surgery and recovery operations can orphan, corrupt, or misrepresent live resources.

Mitigation: Create a state backup before state changes and prefer reviewable declarative refactors when possible.

Risk: Terraform state, plan files, logs, and local memory can expose sensitive values.

Mitigation: Do not store secrets in the skill configuration or memory files, restrict access to plans and state, and rotate secrets that appear in state, plans, or logs.

## Reference(s):

- [ClawHub Terraform Skill Page](https://clawhub.ai/ivangdavila/skills/terraform)
- [Clawic Terraform Skill Homepage](https://clawic.com/skills/terraform)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Terraform/OpenTofu, HCL, YAML, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include plan triage, command sequences, configuration examples, CI guidance, and risk-aware state/apply checklists.]

## Skill Version(s):

1.0.4 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
