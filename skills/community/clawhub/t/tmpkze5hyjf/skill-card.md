## Description:

Generate native eNSP `.topo` files for Huawei network simulation topologies from natural-language topology requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forealmy](https://clawhub.ai/user/forealmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network engineers, and learners use this skill to turn requested Huawei eNSP network diagrams into ready-to-open `.topo` topology files with devices, links, labels, and area boxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topology names or labels copied from untrusted input could break `.topo` XML attributes if written without escaping.

Mitigation: Escape XML attribute content before writing the final `.topo` file.

Risk: Generated topology files may not match the intended network design or eNSP compatibility requirements.

Mitigation: Review the generated `.topo` file and open it in eNSP before using it for simulation work.

## Reference(s):

- [eNSP .topo File Format Reference](references/topo-reference.md)
- [Huawei eNSP product page](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604)

## Skill Output:

**Output Type(s):** [Files, Text, Configuration]

**Output Format:** [Native .topo XML file plus a short text completion message with the saved file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the generated topology to the current workspace for the user to open in eNSP.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
