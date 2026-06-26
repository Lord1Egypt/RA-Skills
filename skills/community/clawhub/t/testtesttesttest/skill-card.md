## Description: <br>
Provides Tencent Cloud COS object storage, CI data processing, MetaInsight retrieval, and knowledge-base workflows through guided setup and command execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and cloud operators use this skill to configure Tencent Cloud COS access, manage buckets and objects, process media and documents with Tencent CI, and run retrieval or knowledge-base workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tencent Cloud credentials and can persist them locally if the user selects persistent setup. <br>
Mitigation: Use least-privilege sub-account keys or temporary STS credentials, prefer non-persistent environment variables, and avoid root or full-account keys. <br>
Risk: The skill can delete cloud objects, batch delete files, change ACL or CORS settings, and call Tencent CI APIs. <br>
Mitigation: Review destructive or permission-changing commands before execution and restrict credentials to the specific bucket and CI actions needed. <br>
Risk: Server security evidence marks the release suspicious because of sensitive cloud operations and credential handling. <br>
Mitigation: Install only after security review confirms the requested COS and CI permissions match the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/testtesttesttest) <br>
- [Tencent Cloud COS API documentation](https://cloud.tencent.com/document/product/436/8629) <br>
- [Tencent Cloud CI documentation](https://cloud.tencent.com/document/product/460) <br>
- [COS Node.js SDK](https://github.com/tencentyun/cos-nodejs-sdk-v5) <br>
- [API reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; invoked scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud SecretId, SecretKey, Region, and Bucket configuration; optional STS token and dataset/domain settings are supported.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
