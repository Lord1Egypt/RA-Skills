## Description:

使用七牛云 Kodo 与 qshell 执行对象存储操作，包含下载 qshell、配置账号、查询 bucket、上传文件、下载文件。适用于用户提到七牛云、七牛 Kodo、qshell、对象存储上传下载、AK/SK、bucket、key、文件中转、把文件上传到七牛或从七牛下载到本地的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Qiniu Kodo object storage through qshell, including account setup, bucket creation, object lookup, upload, download, deletion, and temporary file transfer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate Qiniu Kodo using user-provided AK/SK credentials.

Mitigation: Use narrowly scoped credentials, avoid pasting secrets into chat or logs, and rotate any credentials that may have been exposed.

Risk: The bundled workflows include object deletion and bucket creation commands.

Mitigation: Review bucket names, object keys, regions, and private/public settings before authorizing destructive or provisioning actions.

Risk: The qshell binary is downloaded from an external URL referenced by the artifact.

Mitigation: Verify the qshell download against an official Qiniu source before execution, and prefer an already trusted local qshell package when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/qiniu-kodo-qshell)
- [Qiniu qshell documentation](https://developer.qiniu.com/kodo/1302/qshell)
- [qshell v2.18.0 Linux amd64 download](https://kodo-toolbox-new.qiniu.com/qshell-v2.18.0-linux-amd64.tar.gz?ref=developer.qiniu.com&s_path=%2Fkodo%2F1302%2Fqshell)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise operation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report bucket, key, local path or remote key, file size when known, and operation success status.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
