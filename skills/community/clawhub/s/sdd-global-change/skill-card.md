## Description:

通过自然语言修改全局 spec 文档。解析需求，展示变更计划，执行修改，并生成配图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to update Chinese-language SDD global specification documents from natural-language requests. It plans document changes for confirmation, applies approved Markdown edits, checks cross-document consistency, and generates needed supporting images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently edit SDD global documentation and create image files in the configured workspace.

Mitigation: Review the proposed change plan before confirming execution, and use the skill only in intended workspaces.

Risk: The workflow is designed for Chinese-language global SDD documentation.

Mitigation: Use it for projects that maintain global SDD documents in Chinese, or review and translate outputs before adoption.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mahingbun-dev/skills/sdd-global-change)
- [Publisher profile](https://clawhub.ai/user/mahingbun-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Chinese Markdown plans, document edits, image-generation requests, and completion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes approved changes to scoped SDD global documentation and may create image files under the configured workspace.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
