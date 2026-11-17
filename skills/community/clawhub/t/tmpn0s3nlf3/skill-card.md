## Description:

Always use when user asks to create, generate, or design a network topology diagram for eNSP (Enterprise Network Simulation Platform), or mentions creating eNSP topologies, network simulations with Huawei devices (AR routers, S5700 switches, PC, Cloud, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[forealmy](https://clawhub.ai/user/forealmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network engineers use this skill to turn natural-language eNSP topology requests into native .topo files for Huawei network simulation. It supports common routers, switches, firewalls, wireless devices, endpoints, connection types, area boxes, and text annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates .topo files in the current workspace, which could overwrite an existing topology if the same filename is reused.

Mitigation: Review or choose the output filename before generation when preserving existing topology files matters.

Risk: Generated network topologies may not exactly match the user's intended device models, interfaces, or layout.

Mitigation: Inspect the generated .topo file in eNSP before using it as the basis for simulation or configuration work.

## Reference(s):

- [eNSP .topo File Format Reference](references/topo-reference.md)
- [Huawei eNSP product page](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604)

## Skill Output:

**Output Type(s):** [Files, Code, Markdown, Guidance]

**Output Format:** [Native .topo XML file with a short Markdown completion message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates .topo files in the current workspace and reports the output path for opening in eNSP.]

## Skill Version(s):

1.1.0 (source: server release metadata; frontmatter lists 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
