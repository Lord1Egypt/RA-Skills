## Description: <br>
Manage Synology NAS via DSM Web API: authenticate, browse and manage files with FileStation, manage download tasks with DownloadStation, and query system information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric1932](https://clawhub.ai/user/eric1932) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent interact with their own Synology NAS through DSM Web API commands for file management, download task control, and system information lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to perform powerful file and download-management actions on a Synology NAS. <br>
Mitigation: Require explicit user confirmation with exact paths or task IDs before delete, overwrite, move, upload, download, or bulk task actions. <br>
Risk: DSM credentials and OTP codes may be exposed if placed directly in chat or URL strings. <br>
Mitigation: Use HTTPS, prefer environment variables, avoid hardcoding secrets in commands, and use a least-privileged DSM account. <br>


## Reference(s): <br>
- [FileStation API Reference](references/filestation-api.md) <br>
- [DownloadStation API Reference](references/downloadstation-api.md) <br>
- [Synology DSM API Error Codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require user-supplied DSM connection environment variables and review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
