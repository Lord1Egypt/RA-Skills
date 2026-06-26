## Description: <br>
Tencent COS helps agents manage Tencent Cloud COS object storage and CI data processing tasks, including file operations, media and document processing, content review, MetaInsight search, and knowledge base workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnminh](https://clawhub.ai/user/shawnminh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Tencent Cloud COS and CI for object storage, signed links, file transfer, media and document processing, content review, search, and knowledge base workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad Tencent COS and CI operations, including uploads, deletions, indexing, and arbitrary CI API requests. <br>
Mitigation: Install only for intentional Tencent COS/CI use, require explicit user confirmation for upload, delete, indexing, ci-request, and decrypt-env actions, and review proposed commands before execution. <br>
Risk: The skill requires sensitive Tencent Cloud credentials. <br>
Mitigation: Use least-privilege Tencent sub-account credentials or STS temporary credentials, avoid root or broad permanent keys, and prefer ephemeral environment-variable storage. <br>
Risk: Generic cloud-storage requests may activate this Tencent-specific integration even when the user did not name Tencent Cloud. <br>
Mitigation: Confirm the intended cloud provider before running the skill for broad requests such as uploading to cloud storage or creating a knowledge base. <br>
Risk: Tencent COS and CI operations can incur service fees. <br>
Mitigation: Make users aware of COS and CI charges before running storage, processing, indexing, or knowledge base workflows. <br>


## Reference(s): <br>
- [ClawHub Tencent COS skill page](https://clawhub.ai/shawnminh/tencent-cos-skill) <br>
- [COS Node.js SDK operation reference](references/api_reference.md) <br>
- [Tencent Cloud COS Node.js SDK documentation](https://cloud.tencent.com/document/product/436/8629) <br>
- [Tencent Cloud CI documentation](https://cloud.tencent.com/document/product/460) <br>
- [Tencent Cloud COS fees](https://cloud.tencent.com/document/product/436/16871) <br>
- [Tencent Cloud CI fees](https://cloud.tencent.com/document/product/460/6970) <br>
- [cos-nodejs-sdk-v5 GitHub repository](https://github.com/tencentyun/cos-nodejs-sdk-v5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials and configuration for Region and Bucket; optional Token, DatasetName, Domain, ServiceDomain, and Protocol settings are supported.] <br>

## Skill Version(s): <br>
1.1.8 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
