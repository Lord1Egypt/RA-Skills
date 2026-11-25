## Description:

A structured workflow for managing product documentation in Feishu (Lark), including project knowledge bases, product requirement documents, lifecycle states, versioning, and Feishu API setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxc159620352](https://clawhub.ai/user/zxc159620352)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and documentation owners use this skill to create and maintain Feishu-based product documentation, including requirements thinking, project and code logic records, configuration records, and versioned PRDs. It also provides Feishu API setup and workflow examples for automated document management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes live-looking Feishu credentials and personal/account data.

Mitigation: Revoke and rotate the exposed App Secret, access token, and refresh token, remove personal/account data, and replace all credentials with placeholders before installation or redistribution.

Risk: The documented workflow encourages recording secrets and deployment configuration in collaborative documents.

Mitigation: Treat Feishu documents as non-secret documentation only and store tokens, API keys, passwords, and deployment secrets in a dedicated secret manager.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxc159620352/skills/simple-product-doc-manager)
- [workflow-examples.md](references/workflow-examples.md)
- [feishu-api-setup.md](references/feishu-api-setup.md)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu Open Platform documentation](https://open.feishu.cn/document/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bilingual Chinese and English document templates, lifecycle guidance, Feishu API configuration steps, and workflow examples.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
