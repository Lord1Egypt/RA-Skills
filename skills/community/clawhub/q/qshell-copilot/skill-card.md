## Description: <br>
Manage files on Qiniu Cloud Storage (Kodo) with qshell for uploads, downloads, listing, deletion, copy or move operations, CDN refresh and prefetch, private URLs, and bucket management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijianfei](https://clawhub.ai/user/lijianfei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Qiniu Kodo buckets and objects through the qshell CLI from natural-language requests. It helps choose the appropriate qshell command, check installation and authentication, format batch-download configuration, and guide recovery from common qshell errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Qiniu access keys can grant storage access if exposed or over-scoped. <br>
Mitigation: Use least-privilege Qiniu keys when possible and avoid pasting secrets into chat. <br>
Risk: Storage commands can overwrite, move, delete, refresh CDN content, or create buckets. <br>
Mitigation: Review bucket names, object keys, overwrite flags, move and delete operations, CDN refreshes, and bucket-creation commands before approving them. <br>
Risk: A qshell binary from an unofficial source could create credential or execution risk. <br>
Mitigation: Verify qshell from an official source before using it with a Qiniu account. <br>


## Reference(s): <br>
- [Batch Download Configuration](references/batch-download.md) <br>
- [qshell Installation Guide](references/install-guide.md) <br>
- [Qiniu Key Management](https://portal.qiniu.com/user/key) <br>
- [qshell GitHub Releases](https://github.com/qiniu/qshell/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include qshell command sequences, pre-flight checks, result summaries, and confirmation prompts for destructive operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
