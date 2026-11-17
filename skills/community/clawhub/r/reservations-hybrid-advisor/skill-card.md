## Description:

Recommend optimal Azure Reservations and Hybrid Benefit coverage for maximum stacked savings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

External Azure cost owners, FinOps practitioners, and cloud engineers use this skill to analyze exported reservation, usage, and license inventory data, then plan Reservation and Azure Hybrid Benefit coverage for stable workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires exported Azure cost, usage, and license inventory data, which may include sensitive business information.

Mitigation: Use only read-only exports, review pasted data for secrets or unnecessary sensitive details, and share the minimum data needed for the analysis.

Risk: Reservation and Hybrid Benefit recommendations can affect financial commitments.

Mitigation: Independently verify current Azure pricing, eligibility, workload stability, and commitment terms before purchasing reservations or changing license assignments.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with tables, recommendations, risk flags, and optional inline shell commands for exporting read-only Azure data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; the user provides exported Azure cost, usage, and license inventory data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
