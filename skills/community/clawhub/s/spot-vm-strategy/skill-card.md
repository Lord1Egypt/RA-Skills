## Description: <br>
Design an interruption-resilient GCP Spot VM strategy for eligible workloads with 60-91% savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, cloud engineers, and FinOps teams use this skill to evaluate GCP workloads for Spot VM suitability, estimate savings, and plan interruption-resilient Managed Instance Group, GKE, Dataflow, Dataproc, and Batch configurations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud inventory, billing exports, or pasted configuration may include secrets or unnecessary project details. <br>
Mitigation: Use least-privilege read-only GCP access when exporting data, remove secrets or unnecessary project details before sharing outputs, and confirm pasted data contains no credentials before analysis. <br>
Risk: Generated gcloud commands or YAML changes could alter production cloud infrastructure if run without review. <br>
Mitigation: Review all generated commands and configuration through normal cloud change control before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/spot-vm-strategy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, YAML examples, and inline gcloud and bq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output based on user-provided exports or workload descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
