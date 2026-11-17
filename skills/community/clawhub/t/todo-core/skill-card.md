## Description:

Provides shared rules for the todo-* command set, including TODO.md task-tree conventions, planning and verification workflows, git and no-git handling, invariants, and safety guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bassemzohdy](https://clawhub.ai/user/bassemzohdy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill as the shared guide for the todo-* command set and for keeping a TODO.md Active Backlog consistent. It explains task structure, verification, git or no-git workflows, and the guardrails for editing project state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is invoked through todo-* commands that can make changes to backlog files and repository branches as described in its workflow.

Mitigation: Review the command's documented write scope and intended task before running it; /todo alone is documented as a read-only check.

Risk: Verification examples include an unpinned npx jest command.

Mitigation: Use the project's lockfile-backed test command or pin the Jest version before relying on that example.

Risk: The security assessment reports partial coverage and degraded tool-misuse analysis.

Mitigation: Review the skill instructions and repository-specific commands before use, especially where commands can modify files or git state.

## Reference(s):

- [Todo core skill on ClawHub](https://clawhub.ai/bassemzohdy/skills/todo-core)
- [Server-resolved GitHub source](https://github.com/bassemZohdy/todo-skills/tree/main/plugin/skills/todo)
- [CI guidance](reference/ci.md)
- [Clarification guidance](reference/clarify.md)
- [Deliverables guidance](reference/deliverables.md)
- [Documentation drift guidance](reference/doc-drift.md)
- [Git flow guidance](reference/git-flow.md)
- [Git flow edge cases](reference/git-flow-edge.md)
- [Lane guidance](reference/lanes.md)
- [Review guidance](reference/review.md)
- [Requirements traceability guidance](reference/rtm.md)
- [Verification guidance](reference/verification.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files]

**Output Format:** [Task-tree entries, Markdown guidance, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command set can update TODO.md, planning and status documents, and changelog entries according to its documented workflow.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
