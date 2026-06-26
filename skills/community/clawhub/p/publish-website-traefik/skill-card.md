## Description: <br>
Manages static website deployments to subdomains under *.sites.friendify.cloud using Traefik reverse proxy and Docker, with scripts to deploy, list, and delete sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailo037](https://clawhub.ai/user/mailo037) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to publish static website directories as Docker-hosted Nginx containers behind a Traefik reverse proxy on *.sites.friendify.cloud, then list or delete those deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment and deletion scripts have broad host-level Docker and filesystem effects. <br>
Mitigation: Run the skill only on a host intended for public Docker-based deployments, review generated Docker Compose configuration, and constrain deletion to known skill-owned temporary directories. <br>
Risk: A website directory may contain secrets or files not intended for publication. <br>
Mitigation: Deploy from a dedicated build output directory with no credentials, private source files, or environment-specific configuration. <br>
Risk: Subdomain input is used to form container names, Traefik labels, temporary paths, and public URLs. <br>
Mitigation: Validate subdomains against an allowlist pattern before running deployment or deletion commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mailo037/publish-website-traefik) <br>
- [Publisher Profile](https://clawhub.ai/user/mailo037) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deployment scripts generate Docker Compose configuration, update a JSON deployment registry, and print deployment URLs and status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
