## Description: <br>
Checks SSL/TLS certificates for hostnames, including expiry dates, issuer, SANs, protocol version, and cipher suite, and alerts on expired or soon-to-expire certificates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security-minded users use this skill to inspect HTTPS certificate health for hostnames they provide, including expiry status, issuer, subject alternative names, TLS protocol, and cipher details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes user-directed network connections to supplied hostnames and ports. <br>
Mitigation: Run it only against systems you own or have permission to test, and keep host and port lists narrowly scoped. <br>
Risk: Certificate status output can influence monitoring or operational decisions. <br>
Mitigation: Confirm unexpected expiry, issuer, or connection-failure results before taking disruptive operational action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogue-agent1/ssl-certcheck) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text certificate report or JSON array, with command examples in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connects to user-specified hostnames and ports; exits nonzero when certificates are expired or within the warning threshold.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
