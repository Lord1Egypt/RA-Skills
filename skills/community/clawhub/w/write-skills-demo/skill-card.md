## Description:

Use when creating new skills, editing existing skills, or verifying skills work before deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freshman94](https://clawhub.ai/user/freshman94)

### License/Terms of Use:


## Use Case:

Developers and skill authors use this skill to create, revise, and verify agent skills with a test-driven process. It focuses on writing discoverable skill documentation, testing behavior with pressure scenarios, and closing gaps before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide persistent changes to agent skills or behavior beyond the intended task.

Mitigation: Use it only in a controlled skill-development workspace with explicit user approval for each skill being created or edited.

Risk: Under-scoped local skill-directory search examples may encourage overly broad inspection of local agent skill directories.

Mitigation: Scope searches to user-approved directories and review commands before running them.

Risk: Modified skills may be activated or shared before their behavior is reviewed.

Mitigation: Require human review before committing, pushing, or activating changed skills.

## Reference(s):

- [Writing Skills](artifact/SKILL.md)
- [Skill authoring best practices](artifact/anthropic-best-practices.md)
- [Testing Skills With Subagents](artifact/testing-skills-with-subagents.md)
- [Persuasion Principles for Skill Design](artifact/persuasion-principles.md)
- [Testing CLAUDE.md Skills Documentation](artifact/examples/CLAUDE_MD_TESTING.md)
- [Claude context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with examples, checklists, and inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce proposed skill text, review notes, test scenarios, and commands for the user to approve.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
