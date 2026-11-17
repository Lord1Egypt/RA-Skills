## Description:

Build and operate a file-driven Memory Palace for multi-agent systems that combines spatial project rooms, task corridors, and a continuously maintained LLM Wiki reflection layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1one0415](https://clawhub.ai/user/z1one0415)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-system builders use this skill to design durable file-based memory systems for multi-agent teams, separating project facts, task state, and reusable reflection. It is suited to long-running projects that need lower token waste, reduced context drift, and repeatable memory maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent file-based memory structure can retain project materials longer than expected if memory folders are too broad.

Mitigation: Scope memory folders to materials the agent is intended to read and summarize, and review retained files during routine project cleanup.

Risk: Archivist or Librarian workflows can promote incomplete project observations into reusable guidance.

Mitigation: Compile reflections only from completed task cards and review candidate principles, prompt kernels, and constitution entries before reuse.

## Reference(s):

- [Architecture Reference](artifact/references/architecture.md)
- [Publishing Note](artifact/references/publishing-note.md)
- [Naming Quick Reference](artifact/references/naming-quickref.md)
- [Z1 Matrix Memory Palace Method | English Release Copy](artifact/references/release-copy-en.md)
- [Z1矩阵宫殿记忆法｜中文发布介绍](artifact/references/release-copy-zh.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with directory structures, naming conventions, task-card patterns, and memory maintenance workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-based memory architecture guidance; no API keys, MCP tools, or credential environment variables were detected.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
