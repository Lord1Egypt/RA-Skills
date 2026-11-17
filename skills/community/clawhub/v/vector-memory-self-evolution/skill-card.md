## Description:

向量记忆自我进化系统 - 结合 BGE 向量模型、Chroma 向量库、四层记忆架构，实现自动错误捕获、用户纠正学习、最佳实践积累、语义检索的自我进化能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxbl79](https://clawhub.ai/user/lxbl79)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add local, vector-searchable memory for command errors, user corrections, best practices, and recurring events. It supports pre-execution checks, semantic memory search, conflict detection, and redaction-oriented handling of stored memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores and reuses user and agent content, including conversation-derived memories, command errors, corrections, and vectorized text.

Mitigation: Use it only where local long-term memory storage is acceptable, and add review, deletion, and retention controls before enabling automatic capture for sensitive work.

Risk: The security evidence says the skill overstates its safety and implemented features.

Mitigation: Review the artifact behavior and test the claimed redaction, scan, and memory workflows before deployment.

Risk: The included examples mention privileged or forceful commands such as sudo, --break-system-packages, and kill -9.

Mitigation: Treat generated command guidance as advisory and require manual verification before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxbl79/skills/vector-memory-self-evolution)
- [Publisher profile](https://clawhub.ai/user/lxbl79)
- [Local embedding endpoint](http://localhost:11434/api/embeddings)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reference local memory files, Chroma vector data, and suggested command checks under the user's OpenClaw workspace.]

## Skill Version(s):

2.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
