## Description:

在任何创造性工作之前必须使用 - 创建功能、构建组件、添加新功能或修改行为。通过协作对话探索用户意图、需求和设计。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lky115](https://clawhub.ai/user/lky115)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use this skill to turn vague feature ideas into validated design specifications through structured dialogue, alternative exploration, and section-by-section review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect current project files, documentation, and recent commits while brainstorming.

Mitigation: Use it only in workspaces where project context is appropriate to share with the active agent session.

Risk: The skill may create and commit a design document after the design is validated.

Mitigation: Review the generated design document and intended git changes before allowing repository updates.

Risk: The workflow text is primarily in Chinese, which can cause misunderstanding for non-Chinese readers.

Mitigation: Review a translation before use if the operator is not comfortable reading Chinese.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown and conversational text, with optional design document files and git commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a validated design document under docs/plans and may prepare follow-on implementation planning guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
