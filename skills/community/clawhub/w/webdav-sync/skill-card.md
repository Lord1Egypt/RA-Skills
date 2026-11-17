## Description:

Archives local files or directories into tar or tar.gz files and uploads them to a configured WebDAV endpoint with optional notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyanmi](https://clawhub.ai/user/xyanmi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create repeatable WebDAV backups, configure exclusion rules, and wire the sync command into wrappers or scheduled jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local archive contents are uploaded to the configured WebDAV destination, so an overly broad source path or missing exclude rule can send unintended files off-host.

Mitigation: Review source paths and exclude rules before running or scheduling the skill, and use narrow paths for backup jobs.

Risk: The release evidence notes that HTTPS is not enforced for WEBDAV_SITE, which could expose uploaded data or credentials if an insecure endpoint is configured.

Mitigation: Configure WEBDAV_SITE with an HTTPS URL and use the skill only with trusted WebDAV destinations.

## Reference(s):

- [WebDAV Sync Operations](references/operations.md)
- [ClawHub skill page](https://clawhub.ai/xyanmi/skills/webdav-sync)
- [Publisher profile](https://clawhub.ai/user/xyanmi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for archive creation, WebDAV upload configuration, wrapper usage, scheduling, and exclusion rules.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
