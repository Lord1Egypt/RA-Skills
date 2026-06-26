## Description: <br>
Generates native eNSP `.topo` topology files for Huawei network simulation from natural-language network descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forealmy](https://clawhub.ai/user/forealmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers, instructors, and learners use this skill to turn described Huawei/eNSP network designs into ready-to-open `.topo` files with devices, links, annotations, and layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated topology files may not accurately represent sensitive or complex networks. <br>
Mitigation: Review device, connection, annotation, and layout details before opening or relying on the `.topo` file in eNSP. <br>
Risk: The skill creates local topology files in the working directory. <br>
Mitigation: Run it only in directories where creating new `.topo` files is acceptable and choose clear, non-conflicting filenames. <br>


## Reference(s): <br>
- [eNSP .topo File Format Reference](references/topo-reference.md) <br>
- [Huawei eNSP Enterprise Support](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Guidance] <br>
**Output Format:** [eNSP `.topo` XML file plus a short Markdown response with the saved file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local `.topo` file in the current working directory for the user to open in eNSP.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
