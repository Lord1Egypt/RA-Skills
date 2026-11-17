## Description:

Syncs Claude Code project context by auditing and updating CLAUDE.md, project skills, memory, and settings suggestions at the start of a session or after significant project changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiaswestholm](https://clawhub.ai/user/tobiaswestholm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to bring project instructions and related context files back in line with the current repository before continuing work. It is useful after time away from a project, after significant stack or infrastructure changes, or when Claude context may be stale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly change persistent Claude instructions, project skills, and memory that future sessions may trust.

Mitigation: Use it only in repositories you trust, ask for proposed changes before writes when appropriate, and review git diffs after every run.

Risk: Broad activation around session startup, sync requests, and significant project changes may lead to context updates when the user expected a read-only review.

Mitigation: Confirm intended write behavior before running in sensitive repositories, or ask the agent to audit and propose changes first.

Risk: Incorrect updates to CLAUDE.md, .claude/rules, .claude/skills, or memory files can leave misleading guidance for later agents.

Mitigation: Keep updates surgical, compare changes against current repository files, and require human review before relying on the updated context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobiaswestholm/skills/sync-claude-context)
- [Publisher profile](https://clawhub.ai/user/tobiaswestholm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command snippets, repository file edits, and settings recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update CLAUDE.md, .claude/rules, .claude/skills, and memory files; settings changes are presented as suggestions.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
