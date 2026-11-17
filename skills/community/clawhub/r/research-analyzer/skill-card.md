## Description:

综合研究分析工具 - 基于 Tavily API 的智能搜索和报告生成，支持深度研究、竞品分析、技术调研.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyqdq888](https://clawhub.ai/user/hyqdq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to run Tavily-powered web research on a topic and produce structured research reports for market research, competitive analysis, technical research, or general investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics are sent to Tavily for search processing.

Mitigation: Do not include secrets, private customer data, confidential strategy, or other sensitive material in research queries.

Risk: The --output option can replace an existing writable file.

Mitigation: Use simple report filenames in a safe working directory and check the target path before running the command.

## Reference(s):

- [Research Analyzer on ClawHub](https://clawhub.ai/hyqdq888/skills/research-analyzer)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research report or console text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a user-selected Markdown report file when --output is provided; uses standard or deep search modes and caps max results at 20.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
