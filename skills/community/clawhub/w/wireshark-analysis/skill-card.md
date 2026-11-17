## Description:

Network traffic analysis with Wireshark and tshark. Capture packets, write display and BPF filters, follow TCP/UDP/TLS streams, detect C2 beacons, troubleshoot connectivity, and perform forensic PCAP analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, network engineers, developers, and incident responders use this skill for authorized packet capture, PCAP review, protocol filtering, traffic troubleshooting, and forensic investigation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live packet capture can collect credentials, private traffic, or other sensitive data.

Mitigation: Capture only authorized interfaces, use capture filters to minimize collection, and protect PCAP files according to applicable privacy and security policies.

Risk: Network traffic analysis may lead to incorrect conclusions if filters, protocol behavior, or encrypted traffic limitations are misunderstood.

Mitigation: Review findings with qualified security or network personnel and account for documented limitations such as encrypted content visibility, packet loss, and protocol decoding constraints.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline filters, commands, and procedural steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for Wireshark and tshark analysis; it does not execute captures or inspect traffic by itself.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
