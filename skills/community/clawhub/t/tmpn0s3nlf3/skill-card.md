## Description: <br>
Generates native Huawei eNSP .topo topology files from natural-language network design requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forealmy](https://clawhub.ai/user/forealmy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Network engineers, lab builders, and developers use this skill to turn requested Huawei eNSP network topologies into ready-to-open .topo files with supported devices, links, labels, and area boxes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated topology files may overwrite an existing file if a filename is reused. <br>
Mitigation: Choose or review output filenames before writing files in the current working directory. <br>
Risk: Generated topology files may store sensitive real network details included in the request. <br>
Mitigation: Avoid including sensitive production network details unless storing them in the generated .topo file is acceptable. <br>


## Reference(s): <br>
- [eNSP .topo File Format Reference](references/topo-reference.md) <br>
- [Huawei eNSP Product Page](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604) <br>
- [ClawHub Skill Page](https://clawhub.ai/forealmy/tmpn0s3nlf3) <br>
- [Publisher Profile](https://clawhub.ai/user/forealmy) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Guidance] <br>
**Output Format:** [Native .topo XML file plus a brief saved-path message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated topology files in the current working directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
