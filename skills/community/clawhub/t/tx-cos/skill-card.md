## Description: <br>
面向 OpenClaw 的腾讯云 COS 原生操作技能。适用于上传本地文件、批量同步目录、大文件分片上传、生成临时签名链接、浏览对象与文件夹视图、复制/移动/重命名/删除对象、统计目录体量，以及排查 COS 凭证和 Bucket 配置。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[156554395](https://clawhub.ai/user/156554395) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent manage Tencent Cloud COS objects, including uploads, signed URLs, object listing, copy, move, rename, deletion, folder statistics, and configuration checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete Tencent Cloud COS objects, including bulk and recursive deletion. <br>
Mitigation: Use least-privilege COS credentials scoped to the intended bucket or prefix, verify object keys and prefixes before destructive operations, and require explicit confirmation before recursive or bulk deletion. <br>
Risk: Incorrect bucket, region, credential, or object-key configuration can apply operations to the wrong target or fail unexpectedly. <br>
Mitigation: Run the configuration check first, confirm the bucket, region, and path mapping, and do not proceed when required COS settings are missing. <br>
Risk: Signed URLs can expose access to COS objects for their configured lifetime. <br>
Mitigation: Use short expiration times, confirm the intended object key before generating a link, and avoid sharing links beyond the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/156554395/tx-cos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Concise human-facing text with JSON command results and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm, plus Tencent Cloud COS environment variables for bucket access.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
