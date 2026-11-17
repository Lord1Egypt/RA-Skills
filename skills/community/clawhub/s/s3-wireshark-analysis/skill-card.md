## Description:

Provides Wireshark workflows for capturing, filtering, reconstructing, and analyzing network traffic for troubleshooting, protocol analysis, and security investigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network engineers, and security analysts use this skill to guide authorized packet capture, PCAP review, traffic filtering, stream reconstruction, anomaly investigation, and incident documentation with Wireshark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packet capture can collect traffic beyond the intended scope.

Mitigation: Use the skill only for authorized network analysis and apply narrow capture filters before collecting packets.

Risk: Saved PCAPs and TLS keys can contain passwords, private communications, session data, and files.

Mitigation: Avoid unnecessary credential capture and protect saved captures and keys according to the data sensitivity.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with Wireshark filter examples and step-by-step analysis workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include capture filters, display filters, reconstructed stream review steps, statistical analysis procedures, and incident documentation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
