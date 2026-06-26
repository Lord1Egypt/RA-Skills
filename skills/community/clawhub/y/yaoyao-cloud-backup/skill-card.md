## Description: <br>
Yaoyao Cloud Backup V2 provides guided cloud and external backup synchronization for OpenClaw memory data across IMA, WebDAV, S3-compatible storage, FTP/SFTP, and Samba/NAS targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taobaoaz](https://clawhub.ai/user/taobaoaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure, export, upload, download, and restore OpenClaw memory backups through conversational guidance and bundled synchronization scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive cloud, NAS, SFTP, and IMA credentials. <br>
Mitigation: Use dedicated least-privilege credentials, avoid root or broad cloud keys, and store secrets only in the intended local credentials file. <br>
Risk: Backup and sync actions can upload OpenClaw memory exports to third-party or self-hosted storage. <br>
Mitigation: Run status or dry-run commands first and review the exact export paths and provider configuration before uploading. <br>
Risk: Restore and download actions can overwrite or reintroduce untrusted backup data. <br>
Mitigation: Restore only backups from trusted storage locations and inspect backup contents before applying them to active memory data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/taobaoaz/yaoyao-cloud-backup) <br>
- [Jianguoyun](https://www.jianguoyun.com/) <br>
- [Alibaba Cloud OSS](https://www.aliyun.com/product/oss) <br>
- [Nextcloud](https://nextcloud.com/) <br>
- [Tencent Cloud COS](https://cloud.tencent.com/product/cos) <br>
- [Tencent IMA](https://ima.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, upload, download, or restore local backup/export files when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
