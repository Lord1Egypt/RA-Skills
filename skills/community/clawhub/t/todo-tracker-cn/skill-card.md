## Description:

Generates, tracks, displays, and verifies todo-list progress for AI assistant workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elderyang](https://clawhub.ai/user/elderyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistant operators use this skill to create, update, inspect, and verify persistent task checklists for multi-step work that needs visible progress and completion checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions are written to persistent local files and may be appended to agent memory.

Mitigation: Avoid sensitive task descriptions, review stored todo and memory files, and make memory writes opt-in or disabled for sensitive environments.

Risk: Persistent progress records can outlive the immediate task and expose prior work context.

Mitigation: Define retention expectations and clear ~/.openclaw/workspace/todo-current.json and MEMORY.md entries when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elderyang/skills/todo-tracker-cn)
- [Publisher profile](https://clawhub.ai/user/elderyang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-like progress text and command-line responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists todo state under ~/.openclaw/workspace and may append task titles to MEMORY.md.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
