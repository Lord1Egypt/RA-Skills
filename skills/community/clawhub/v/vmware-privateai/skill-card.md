## Description:

Use for VMware Private AI Foundation with NVIDIA on vSphere 9.x and VCF 9.1 to inspect GPU inventory, readiness, utilization, vGPU consumers and profiles, vGPU assignment, and Private AI Service models and data resources; it also provides access checks, local model sizing, and air-gap bundle inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

VMware administrators and infrastructure engineers use this skill to inspect GPU hosts, vGPU assignments and utilization, and Private AI Service resources in vSphere and VCF environments. They can also check account access, estimate model sizing locally, inspect local air-gap bundles, and assign a vGPU profile to an eligible powered-off VM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports instructions that could shut down a VM without separate warning or approval.

Mitigation: Review shutdown instructions and require separate approval before any shutdown.

Risk: The security scan reports credential administration beyond the stated resource-management purpose.

Mitigation: Confirm credential administration is intended before using the skill around credentials.

Risk: The security analysis was partial because several local references could not be resolved.

Mitigation: Review unresolved referenced material before installation; the available scan does not cover every referenced item.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/vmware-privateai)
- [Setup guide](references/setup-guide.md)
- [Capabilities and result limits](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Detailed guide](references/detailed-guide.md)
- [MCP result contract](references/mcp-result-contract.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance, shell commands, configuration]

**Output Format:** [CLI text and structured MCP JSON, with operational guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inventory results may be paginated; check the returned coverage fields before treating a listing as complete. PAIS gallery results may be partial when cursor continuation is unavailable.]

## Skill Version(s):

2.5.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
