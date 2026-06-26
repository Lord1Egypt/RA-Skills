## Description: <br>
A structured workflow for managing product documentation in Feishu (Lark), including knowledge-base setup, requirements lifecycle management, versioned product requirements documents, and API integration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxc159620352](https://clawhub.ai/user/zxc159620352) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and product teams use this skill to set up and maintain Feishu-based product documentation, including knowledge bases, requirements documents, configuration records, and implementation notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports exposed real-looking Feishu credentials in the skill artifact. <br>
Mitigation: Do not use the included Feishu credentials; revoke and rotate them if they belong to you, and replace them with secrets stored in a secret manager. <br>
Risk: The skill encourages recording API keys, environment variables, deployment configuration, and other sensitive setup data in shared Feishu documents. <br>
Mitigation: Store only redacted configuration references in Feishu documents, keep secrets out of shared documentation, and use least-privilege Feishu app permissions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zxc159620352/simple-product-doc-manager) <br>
- [Workflow examples](references/workflow-examples.md) <br>
- [Feishu API setup guide](references/feishu-api-setup.md) <br>
- [Feishu Open Platform documentation](https://open.feishu.cn/document/) <br>
- [Obtain user_access_token](https://open.feishu.cn/document/server-docs/authentication-management/access-token/obtain-user_access_token) <br>
- [Create document API](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through document structure, lifecycle states, naming conventions, Feishu API setup, and workflow examples.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
