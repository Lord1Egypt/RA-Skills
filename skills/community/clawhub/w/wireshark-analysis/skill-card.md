## Description: <br>
Network traffic analysis with Wireshark and tshark for packet capture, filters, stream inspection, C2 beacon detection, connectivity troubleshooting, and forensic PCAP analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, network engineers, and developers use this skill to inspect live captures or PCAP files, troubleshoot network behavior, and document findings from protocol, stream, and traffic-pattern analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized packet capture or inspection can violate policy, privacy obligations, or law. <br>
Mitigation: Use the skill only for traffic you are authorized to inspect and follow the applicable privacy and data-handling policies. <br>
Risk: PCAPs and exported HTTP objects can contain credentials, confidential data, or malicious files. <br>
Mitigation: Protect packet captures as sensitive data and treat exported objects as untrusted until they are scanned and handled safely. <br>
Risk: Overbroad live capture can collect more sensitive traffic than needed. <br>
Mitigation: Use capture filters, stop captures promptly, and limit collection to the investigation scope. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Analysis] <br>
**Output Format:** [Markdown with Wireshark workflows, packet filters, procedural steps, and analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include capture filters, display filters, troubleshooting checks, and incident evidence documentation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
