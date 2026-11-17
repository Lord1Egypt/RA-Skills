## Description:

Generates native eNSP .topo files for Huawei Enterprise Network Simulation Platform network topology diagrams and simulations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forealmy](https://clawhub.ai/user/forealmy)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers, developers, and lab users use this skill to turn natural-language Huawei/eNSP topology requests into ready-to-open .topo files with devices, links, labels, and layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces Huawei/eNSP simulation topology files rather than generic network diagrams.

Mitigation: Confirm the user wants an eNSP .topo file and review the generated topology before opening it in eNSP.

Risk: Generated topology details can be inaccurate or incomplete for the intended lab design.

Mitigation: Inspect device models, links, interfaces, labels, and layout against the requested network before simulation.

## Reference(s):

- [eNSP .topo File Format Reference](references/topo-reference.md)
- [Huawei eNSP Product Page](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604)

## Skill Output:

**Output Type(s):** [Files, Code, Markdown, Guidance]

**Output Format:** [Native .topo XML file plus a short saved-file path message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated topology files should be reviewed before opening in eNSP.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
