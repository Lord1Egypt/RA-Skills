## Description:

Manage Synology NAS devices through the DSM Web API by authenticating, managing files with FileStation, managing DownloadStation tasks, and querying system information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric1932](https://clawhub.ai/user/eric1932)

### License/Terms of Use:


## Use Case:

Developers, engineers, and NAS administrators use this skill to generate DSM Web API guidance and curl commands for authenticated NAS file management, download task control, system queries, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication examples can expose NAS passwords or session IDs if credentials are placed in URLs, logs, shell history, or shared transcripts.

Mitigation: Use HTTPS, avoid putting passwords or session IDs in URLs, keep credentials in user-controlled environment variables or prompts, and do not hardcode secrets in commands.

Risk: File and DownloadStation actions can delete, overwrite, move, upload, download, or change tasks on the NAS.

Mitigation: Use a least-privileged DSM account and require explicit user confirmation before any destructive or state-changing operation.

## Reference(s):

- [FileStation API Reference](references/filestation-api.md)
- [DownloadStation API Reference](references/downloadstation-api.md)
- [Synology DSM API Error Codes](references/error-codes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes curl-based DSM Web API commands that require user-supplied Synology host, port, username, password, and session values.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
