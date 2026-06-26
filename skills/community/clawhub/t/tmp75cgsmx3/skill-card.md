## Description: <br>
Generates native eNSP .topo files from natural-language network topology requests for Huawei network simulations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forealmy](https://clawhub.ai/user/forealmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers, lab users, and developers use this skill to turn plain-language eNSP topology requests into ready-to-open .topo files with supported Huawei routers, switches, firewalls, wireless devices, endpoints, connections, labels, and area boxes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a new .topo file in the current working directory, which could overwrite an existing topology if the same filename is reused. <br>
Mitigation: Ask the agent to confirm the target filename or show the XML before writing when overwrites matter. <br>
Risk: Generated topology files may contain sensitive network layout details supplied by the user. <br>
Mitigation: Review the generated topology before sharing it outside the intended environment. <br>


## Reference(s): <br>
- [eNSP .topo File Format Reference](references/topo-reference.md) <br>
- [Huawei eNSP Product Page](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604) <br>
- [ClawHub skill page](https://clawhub.ai/forealmy/tmp75cgsmx3) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [eNSP .topo XML file plus a short file path message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a native .topo topology file in the working directory for the user to open in eNSP.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
