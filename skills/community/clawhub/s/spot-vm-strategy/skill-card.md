## Description:

Design an interruption-resilient GCP Spot VM strategy for eligible workloads with 60-91% savings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers and cloud infrastructure teams use this skill to evaluate eligible GCP workloads for Spot VM adoption, estimate savings, and draft interruption-resilient deployment guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated GCP commands or managed instance group configuration could create or change infrastructure if run without review.

Mitigation: Review generated commands and configuration in the user's normal change process before running them, especially commands that create Spot VMs or managed instance groups.

Risk: User-provided instance inventory or billing exports may contain credentials, access keys, or unrelated sensitive data.

Mitigation: Check exported inventory and billing summaries before sharing them, and remove credentials, access keys, secrets, and unrelated sensitive fields.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with eligibility matrices, cost estimates, YAML configuration examples, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output intended for user review before any infrastructure changes are made]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
