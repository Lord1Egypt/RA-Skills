## Description:

Generates native .topo files for Huawei eNSP network simulation topologies from natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forealmy](https://clawhub.ai/user/forealmy)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers, developers, and learners use this skill to turn requested Huawei eNSP lab designs into ready-to-open topology files with devices, links, labels, and layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated .topo files may include Cloud devices or adapter settings that affect how a topology connects in eNSP.

Mitigation: Review generated topologies before opening them in eNSP, especially Cloud devices and adapter settings.

Risk: Generated topology structure or interface selections may not match the intended lab design.

Mitigation: Inspect the .topo file and diagram in eNSP before using it for simulation work.

## Reference(s):

- [eNSP .topo File Format Reference](references/topo-reference.md)
- [Huawei eNSP Product Page](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604)

## Skill Output:

**Output Type(s):** [Files, Code, Guidance]

**Output Format:** [Native .topo topology file with XML content and a short file-path response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are intended to be reviewed and opened in eNSP.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
