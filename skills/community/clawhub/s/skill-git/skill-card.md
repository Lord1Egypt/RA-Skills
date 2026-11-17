## Description:

Manage AI agent skills with local version control to initialize tracking, commit changes with semantic versions, inspect conflicts, scan overlap, merge skills, and revert versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zijinoier](https://clawhub.ai/user/zijinoier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use this skill to manage local skill folders as versioned assets, review changes, compare and merge overlapping skills, and roll back problematic versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad local authority over installed skills and can make durable changes to future agent behavior.

Mitigation: Review the target paths, diffs, merge plans, and revert summaries before approving any commit, merge, or revert operation.

Risk: Sensitive files may be retained in Git history, caches, temporary backups, or copied skill folders.

Mitigation: Keep secrets out of skill folders, verify sensitive filename blocklists before staging or merging, and clean caches and backups when they are no longer needed.

Risk: Incorrect conflict or merge guidance could introduce misleading rules into a skill.

Mitigation: Run the skill's check and scan workflows, then manually review the resulting rules and merged content before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zijinoier/skills/skill-git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose and execute local git and jq operations after user confirmation, depending on command.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
