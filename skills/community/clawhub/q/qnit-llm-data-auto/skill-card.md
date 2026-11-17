## Description:

自动生成满足需求的Python和Pandas数据处理代码，支持基于描述快速完成数据操作任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to turn a clear data-processing request into draft Python and Pandas code for common data operations. The generated code should be reviewed and tested before it is run on real datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Python or Pandas code may be incorrect, inefficient, or unsafe to run unchanged.

Mitigation: Inspect the generated code, test it with limited sample data, and run it in a constrained environment before using it on production datasets.

Risk: Prompts or data descriptions may be processed through an LLM/API workflow.

Mitigation: Avoid including sensitive datasets or confidential details unless the workflow is approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesong-hue/skills/qnit-llm-data-auto)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or plain text with Python and Pandas code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code is draft output and should be inspected before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
