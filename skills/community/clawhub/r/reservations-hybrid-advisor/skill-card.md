## Description: <br>
Recommend optimal Azure Reservations and Hybrid Benefit coverage for maximum stacked savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Azure cost owners, FinOps practitioners, and cloud engineers use this skill to review exported Azure cost, reservation, and inventory data and plan Reservation plus Azure Hybrid Benefit savings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure cost and inventory exports may include sensitive subscription, resource, or licensing details. <br>
Mitigation: Limit exports to the relevant subscriptions and date ranges, remove secrets and unnecessary identifiers, and confirm no credentials are included before analysis. <br>
Risk: Reservation and Azure Hybrid Benefit recommendations can affect long-term cloud spend and licensing posture. <br>
Mitigation: Treat the output as planning guidance and review recommendations with the responsible FinOps, cloud, or licensing owner before purchase or configuration changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/reservations-hybrid-advisor) <br>
- [Publisher profile](https://clawhub.ai/user/anmolnagpal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, risk flags, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only analysis based on user-provided Azure exports or workload descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
