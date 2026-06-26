## Description: <br>
使用七牛云 Kodo 与 qshell 执行对象存储操作，包含下载 qshell、配置账号、查询 bucket、上传文件、下载文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Qiniu Kodo object storage through qshell, including account setup, bucket creation, object upload, object download, stat checks, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create buckets or delete stored objects when run with Qiniu credentials. <br>
Mitigation: Use least-privilege AK/SK keys and require explicit confirmation of bucket names and object keys before create or delete operations. <br>
Risk: Credential exposure could occur if AK/SK values are pasted into chat or written into persistent files. <br>
Mitigation: Load credentials from environment-backed configuration, avoid echoing secrets, and rotate any credentials that were disclosed. <br>
Risk: Downloading qshell from an unexpected source could execute an untrusted binary. <br>
Mitigation: Verify the qshell download source and preserve the documented Qiniu URL and request parameters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/qiniu-kodo-qshell) <br>
- [Qiniu qshell documentation](https://developer.qiniu.com/kodo/1302/qshell) <br>
- [qshell v2.18.0 Linux amd64 download](https://kodo-toolbox-new.qiniu.com/qshell-v2.18.0-linux-amd64.tar.gz?ref=developer.qiniu.com&s_path=%2Fkodo%2F1302%2Fqshell) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and bundled shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that create buckets, upload objects, download objects, or delete objects in Qiniu Kodo when executed with user credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
