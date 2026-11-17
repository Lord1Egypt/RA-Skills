## Description:

新环境测试 helps agents manage Tencent Cloud COS object storage and CI workflows, including object operations, media and document processing, content review, speech tasks, MetaInsight retrieval, and knowledge-base setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to configure Tencent Cloud COS credentials, run storage and CI operations through the provided Node.js helper, and create or query document knowledge bases. It is intended for agent-assisted workflows that need JSON-producing shell commands and guidance for Tencent Cloud object storage, media processing, content review, and retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate Tencent COS resources, including object deletion, ACL/CORS changes, dataset binding, and generic CI requests.

Mitigation: Require manual review before running delete, delete-multiple, ACL/CORS, dataset binding, or ci-request actions; prefer test buckets and least-privilege sub-accounts.

Risk: The skill can use powerful Tencent Cloud credentials and may persist or decrypt them locally.

Mitigation: Use short-lived STS credentials where possible, avoid --persist and decrypt-env in shared or logged workspaces, and never use root account keys.

Risk: .env.enc is a convenience protection and should not be treated as strong encryption for shared environments.

Mitigation: Keep credentials ephemeral when practical, remove local credential files after use, and rely on cloud-side least privilege and credential expiration.

## Reference(s):

- [Artifact API reference](artifact/references/api_reference.md)
- [Tencent Cloud COS Node.js SDK documentation](https://cloud.tencent.com/document/product/436/8629)
- [Tencent Cloud CI documentation](https://cloud.tencent.com/document/product/460)
- [cos-nodejs-sdk-v5 GitHub repository](https://github.com/tencentyun/cos-nodejs-sdk-v5)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/skill-test1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script reports operation results as JSON; user-facing responses should summarize results in readable prose.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
