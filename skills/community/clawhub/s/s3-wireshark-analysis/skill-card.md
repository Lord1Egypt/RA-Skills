## Description: <br>
This skill guides agents through Wireshark-based network packet capture, filtering, stream reconstruction, statistical review, and suspicious traffic investigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and network engineers use this skill to inspect authorized network traffic or PCAP files for troubleshooting, incident investigation, malware traffic review, and protocol analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packet captures, followed streams, exported files, and TLS key material can contain sensitive data. <br>
Mitigation: Use only authorized networks and PCAPs, prefer narrow capture filters and short capture windows, perform offline analysis when possible, and treat captured artifacts as sensitive. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with Wireshark workflow steps, filter examples, tables, and inline command-style snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces analysis guidance and documentation prompts; it does not itself capture packets or execute Wireshark.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
