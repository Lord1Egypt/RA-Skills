## Description: <br>
Skill Base server deployment guide. Covers starting the Skill Base server (npx skill-base), Docker configuration, port mapping, and SQLite database backup. For deploying and operating the Skill Base platform itself only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ginuim](https://clawhub.ai/user/ginuim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy and run the Skill Base platform server with npm, source-directory commands, or Docker, including host, port, data directory, and backup configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server can be exposed beyond the intended network when bound to all interfaces or deployed without firewall controls. <br>
Mitigation: Verify the package or repository before production use, bind to 127.0.0.1 when local-only access is needed, and restrict network exposure with firewall or security group rules. <br>
Risk: Skill data and the SQLite database can be lost or made inconsistent if the data directory is not chosen deliberately or backed up during active writes. <br>
Mitigation: Use a dedicated data directory or persistent Docker volume and back up the full data directory during low write activity. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment steps, startup options, Docker commands, backup guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
