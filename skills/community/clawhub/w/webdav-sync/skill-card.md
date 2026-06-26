## Description: <br>
Archive local files or directories into tar or tar.gz archives and upload them to a WebDAV endpoint, with optional notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyanmi](https://clawhub.ai/user/xyanmi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure repeatable backups of selected local files or directories to a WebDAV server, including archive naming, exclusions, remote paths, wrapper scripts, scheduled jobs, and optional notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill archives user-selected local paths and uploads them to a configured WebDAV destination, which can disclose unintended files if the source scope or exclusions are wrong. <br>
Mitigation: Review source paths, remote subdirectories, and explicit exclude patterns before running or scheduling the upload; use a dedicated low-privilege WebDAV account. <br>
Risk: WebDAV credentials are required for upload operations. <br>
Mitigation: Protect the env file, avoid printing credentials, and use a temporary credential file with 0600 permissions instead of passing secrets as command-line arguments. <br>
Risk: Scheduled wrapper jobs can continue uploading after backup scope or operational needs change. <br>
Mitigation: Keep wrapper and cron entries explicit and easy to disable, and update both when changing sync scope. <br>


## Reference(s): <br>
- [WebDAV Sync Operations](references/operations.md) <br>
- [ClawHub skill page](https://clawhub.ai/xyanmi/webdav-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and script arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides archive creation and WebDAV uploads that require curl, openclaw, and WEBDAV_SITE, WEBDAV_USERID, and WEBDAV_PWD environment values.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
