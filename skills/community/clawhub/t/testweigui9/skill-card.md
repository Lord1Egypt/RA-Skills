## Description:

在任何创造性工作之前必须使用 - 创建功能、构建组件、添加新功能或修改行为。通过协作对话探索用户意图、需求和设计。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lky115](https://clawhub.ai/user/lky115)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this Chinese-language brainstorming skill before creative implementation work to turn early ideas into validated designs, then document the agreed design and optionally move into implementation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project context and recent commits while shaping a design.

Mitigation: Use it only where that project context may be shared with the agent, and avoid exposing sensitive material that is not needed for planning.

Risk: The workflow may create and commit a design document after the design is validated.

Mitigation: Review the generated docs/plans/YYYY-MM-DD-<topic>-design.md content and proposed commit before accepting repository changes.

Risk: The skill is written in Chinese and does not provide an explicit language-selection step.

Mitigation: Use it with Chinese-capable operators or request translation before acting on its guidance.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Conversational text and Markdown design documents, with shell commands only when committing the validated plan.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create docs/plans/YYYY-MM-DD-<topic>-design.md after user validation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
