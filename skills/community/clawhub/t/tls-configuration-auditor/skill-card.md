## Description: <br>
Audit TLS/SSL configuration of servers and applications. Check protocol versions, cipher suites, certificate chain validity, HSTS headers, and compliance with security standards (PCI-DSS, NIST, Mozilla recommendations). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and security reviewers use this skill to audit a chosen host's TLS configuration, certificate chain, cipher support, security headers, and compliance posture before assessments or operational changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TLS probes and header checks are active scans against a selected host. <br>
Mitigation: Run the generated commands only against systems the user is authorized to assess. <br>
Risk: Generated monitoring scripts or CI jobs can create recurring network checks or operational alerts. <br>
Mitigation: Review and approve any generated monitoring or CI configuration before enabling it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and audit findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated certificate-expiry monitoring scripts or CI job guidance for reviewer approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
