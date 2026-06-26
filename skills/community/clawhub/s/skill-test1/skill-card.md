## Description: <br>
Tencent Cloud COS and Data Intelligence skill for managing object storage, media and document processing, content review, speech intelligence, MetaInsight retrieval, and knowledge-base workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent configure and operate Tencent Cloud COS and CI workflows for file storage, image/media/document processing, content moderation, speech tasks, and knowledge-base search. It requires Tencent Cloud credentials and should be used only with reviewed actions and least-privilege access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate Tencent Cloud COS/CI with broad cloud-data authority. <br>
Mitigation: Use STS or a dedicated sub-account with the narrowest bucket-level permissions and avoid root or broad permanent keys. <br>
Risk: Destructive or generic actions such as delete, bulk delete, ACL/CORS changes, signed URL generation, and ci-request can have significant effects. <br>
Mitigation: Review the exact target and effect before allowing those actions. <br>
Risk: Cloud credentials are sensitive and can grant access to stored data. <br>
Mitigation: Prefer ephemeral environment variables and do not echo credentials in chat or persist them unless persistence is intentionally reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skill-test1) <br>
- [Tencent Cloud COS Node.js SDK documentation](https://cloud.tencent.com/document/product/436/8629) <br>
- [Tencent Cloud Data Intelligence documentation](https://cloud.tencent.com/document/product/460) <br>
- [cos-nodejs-sdk-v5 GitHub repository](https://github.com/tencentyun/cos-nodejs-sdk-v5) <br>
- [API reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output from the bundled Node.js script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud SecretId, SecretKey, Region, and Bucket; optional STS token and dataset/domain settings are supported.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
