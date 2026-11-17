## Description:

Yaoyao Cloud Backup V2 helps an agent guide users through setup, detection, synchronization, backup, and restore workflows for local and external cloud storage services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taobaoaz](https://clawhub.ai/user/taobaoaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to configure backup destinations, detect existing storage services, and run guided upload, download, status, migration, and restore operations for OpenClaw memory data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials for cloud and network storage services.

Mitigation: Use dedicated least-privilege backup accounts and do not paste real passwords or API keys into chat.

Risk: The security scan flags broad local data handling and unsafe restore behavior.

Mitigation: Review the skill before installing and treat imported backup files as untrusted unless the restore code is fixed.

Risk: Some supported transports may be weaker or misconfigured.

Mitigation: Avoid FTP and unverified SFTP configurations.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/taobaoaz/skills/yaoyao-cloud-backup)
- [Jianguoyun](https://www.jianguoyun.com/)
- [Alibaba Cloud OSS](https://www.aliyun.com/product/oss)
- [Nextcloud](https://nextcloud.com/)
- [Tencent Cloud COS](https://cloud.tencent.com/product/cos)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to local credential and backup configuration files.]

## Skill Version(s):

1.0.1 (source: artifact/SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
