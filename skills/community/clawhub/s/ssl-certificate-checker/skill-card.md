## Description: <br>
Checks SSL/TLS certificate details, including expiration date, issuer, validity, cipher suites, and security warnings for a domain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeonardoDpanda](https://clawhub.ai/user/LeonardoDpanda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to inspect SSL/TLS certificates for public domains when verifying HTTPS configuration, monitoring certificate expiry, or troubleshooting certificate issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Certificate checks contact the specified domain over the network. <br>
Mitigation: Run checks only for domains you are authorized to inspect, and use dedicated internal tooling for internal certificates. <br>
Risk: Untrusted hostname text pasted directly into shell commands can produce incorrect or unsafe command execution. <br>
Mitigation: Validate or type the hostname before running generated OpenSSL commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LeonardoDpanda/ssl-certificate-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
