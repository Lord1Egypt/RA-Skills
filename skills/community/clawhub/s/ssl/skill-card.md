## Description: <br>
Set up HTTPS, manage TLS certificates, and debug secure connection issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to generate SSL/TLS setup, renewal, certificate conversion, server configuration, and troubleshooting guidance for HTTPS services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Certificate and server commands can change live HTTPS configuration, permissions, ownership, or renewal behavior. <br>
Mitigation: Run commands only for domains and servers you control, review file paths and service-specific settings before execution, and test renewal or configuration changes before applying them to production. <br>
Risk: Private keys and PKCS#12 exports are sensitive secrets. <br>
Mitigation: Limit access to private key files and exported bundles, avoid sharing them in prompts or logs, and store them using the target environment's secret-handling controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/ssl) <br>
- [Certificate Format Conversions](formats.md) <br>
- [SSL Configuration by Server](servers.md) <br>
- [SSL Troubleshooting Guide](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; commands are presented for review and manual execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
