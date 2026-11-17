## Description:

文言文压缩技能，可将中文回复、摘要、日志和记忆存档压缩为文言文或典故化表达，并提供映射表、语法速查和典故词典供代理查阅。

This skill is ready for commercial/non-commercial use.

## Publisher:

[october27](https://clawhub.ai/user/october27)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to produce classical Chinese responses, compact Chinese-language summaries, and terse memory or log entries while preserving key information. It is most useful when token-efficient Chinese phrasing or human-facing Wenyan output is desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation guidance for summaries, record-keeping, and memory notes may cause future notes to be stored in a terse Wenyan format when that is not expected.

Mitigation: Review when the skill activates and use the compressed format only for explicit compression, logging, summary, or memory workflows.

Risk: Concise classical Chinese phrasing can omit nuance from the original text.

Mitigation: Use reversible mapped terms for internal archives and keep source context available when precision is important.

## Reference(s):

- [Compression Map](references/compress-map.md)
- [Grammar Cheatsheet](references/grammar.md)
- [Allusion Dictionary](references/dict.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text with compact Wenyan phrases and optional log-style records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use terse time-subject-action-state records for summaries, logs, and memory notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
