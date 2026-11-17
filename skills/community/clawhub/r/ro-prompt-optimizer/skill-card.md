## Description:

基于R-O框架（角色&现实情况、对象&输出）优化用户提示词，将普通需求转化为专业、结构化的AI提示词，以激发AI最大潜力。当用户需要优化提示词、改善与AI的交互效果、创建更有效的指令时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dukeacco](https://clawhub.ai/user/dukeacco)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this Chinese-language skill to turn vague or simple requests into structured R-O framework prompts. It supports prompt design for creative, analytical, execution, decision, and communication tasks across common business domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional save and clipboard paths may place prompt text on local disk or in the system clipboard.

Mitigation: Do not use those options with secrets, credentials, private business data, or regulated content unless the local environment and clipboard history are acceptable for that data.

## Reference(s):

- [Ro Prompt Optimizer on ClawHub](https://clawhub.ai/dukeacco/skills/ro-prompt-optimizer)
- [Industry Templates](references/industry-templates.md)
- [Task Types](references/task-types.md)
- [Examples Library](references/examples-library.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown R-O prompt templates, with optional JSON output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional helper script can save generated prompts as Markdown or JSON files and can copy prompt text to the system clipboard when the clipboard dependency is installed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
