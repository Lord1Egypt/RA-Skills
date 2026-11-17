## Description:

Wb Lobster Memory bridges WorkBuddy to the lobster-memory long-term graph memory engine so an agent can store user preferences, project context, and feedback as graph memory, recall it on demand, and periodically consolidate or forget stale entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littlelollipop](https://clawhub.ai/user/littlelollipop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy users use this skill to add local long-term graph memory alongside existing markdown or profile memory. It supports remembering extracted conversation facts as graph JSON, recalling relevant memories, reviewing feedback, and consolidating stale memory entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived personal or work context in long-term local graph memory.

Mitigation: Use it only when long-term memory is intended, avoid storing secrets or sensitive details, and set the memory directory deliberately.

Risk: The release depends on an external lobster-memory installer that the security evidence describes as unpinned.

Mitigation: Pin and inspect the lobster-memory dependency before installation or execution.

Risk: Memory consolidation and deletion behavior can alter stored graph memory.

Mitigation: Use dry-run or review procedures before consolidation or deletion.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/littlelollipop/skills/wb-lobster-memory)
- [Server-resolved source repository](https://github.com/LittleLollipop/wb-lobster-memory)
- [lobster-memory dependency](https://github.com/LittleLollipop/lobster-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands and JSON memory extraction records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local status text, recall results, feedback summaries, and consolidation or dry-run reports.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
