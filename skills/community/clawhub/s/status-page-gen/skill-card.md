## Description: <br>
Generates a lightweight static HTML status page for self-hosted services with health endpoint checks, ping checks, SSL certificate validation, and uptime history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and self-hosting operators use this skill to configure checks for their services, collect status and certificate data, maintain uptime history, and generate a static status page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated status pages can expose internal hostnames, private URLs, service names, uptime history, or certificate details if published publicly. <br>
Mitigation: Prefer local or private hosting, and redact sensitive service metadata before sharing or publishing the generated page. <br>
Risk: The service and certificate checks contact the services configured by the user. <br>
Mitigation: Configure only services the user owns or is authorized to monitor, and run checks from an approved network environment. <br>


## Reference(s): <br>
- [status-page-gen Setup Guide](references/setup-guide.md) <br>
- [Status Page Gen ClawHub Page](https://clawhub.ai/newageinvestments25-byte/status-page-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, status JSON, certificate JSON, history JSON, and generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local artifacts from user-provided service configuration; outputs may include service names, URLs, uptime history, and certificate status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
