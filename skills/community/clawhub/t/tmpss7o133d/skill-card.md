## Description: <br>
Generates native eNSP .topo topology files for Huawei Enterprise Network Simulation Platform diagrams from natural-language network design requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forealmy](https://clawhub.ai/user/forealmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network engineers, and learners use this skill to turn requested eNSP network designs into local .topo files with devices, links, labels, layout coordinates, and optional grouping shapes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated topology files may not match the user's intended network design or valid eNSP semantics. <br>
Mitigation: Review the generated .topo file and topology layout before opening or using it in eNSP. <br>
Risk: The skill writes a requested topology file into the current workspace. <br>
Mitigation: Use the skill in the intended project directory and inspect the generated file path before use. <br>


## Reference(s): <br>
- [eNSP .topo File Format Reference](references/topo-reference.md) <br>
- [Huawei eNSP product page](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604) <br>
- [ClawHub skill page](https://clawhub.ai/forealmy/tmpss7o133d) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Guidance] <br>
**Output Format:** [Local .topo XML file with a short Markdown status message containing the saved path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files should be reviewed before opening in eNSP.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter declares 1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
