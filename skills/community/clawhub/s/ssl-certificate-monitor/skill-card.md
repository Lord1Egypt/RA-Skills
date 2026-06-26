## Description: <br>
Monitor SSL certificates for expiration, security issues, and compliance across domains and subdomains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, DevOps engineers, and site operators use this skill to check SSL/TLS certificate expiration, inspect certificate metadata, and batch-check domains for renewal planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can misleadingly label a certificate as valid while not proving trust-chain validity, hostname matching, correct issuance, or full compliance. <br>
Mitigation: Treat the output as expiration and certificate-metadata guidance only, and use a separate TLS validation tool before making security decisions. <br>
Risk: The skill connects to target domains and may be inappropriate for systems the operator is not authorized to inspect. <br>
Mitigation: Run checks only against domains and servers the operator owns or is authorized to monitor. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Derick001/ssl-certificate-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/Derick001) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON CLI output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can report certificate status, expiration dates, issuer, subject, serial number, signature algorithm, warnings, and connection or parsing errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
