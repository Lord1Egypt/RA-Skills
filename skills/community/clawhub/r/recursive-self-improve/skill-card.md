## Description:

Recursive Self Improve scans skill directories for improvement opportunities, proposes append/copy-only patches, tests them in a temporary sandbox, verifies results, and records evolution history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit a skills directory, identify missing frontmatter, missing learner modules, or missing self-evolution sections, and generate reviewable patch plans. When deliberately run in apply mode, it can update approved skill folders and record the change history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently modify other installed skills, and the security summary states that its safety promises do not fully match the code.

Mitigation: Run scan and propose first, use a backup or staging skills directory, review generated changes manually, and avoid broad write access to live skill folders without per-skill approval.

Risk: The learning module can persist notes and preferences that may contain sensitive information if supplied by the user.

Mitigation: Avoid recording secrets or sensitive notes, and inspect learned_patterns.json and self_improve_log.json before sharing or publishing the skill directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/recursive-self-improve)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI output, JSON patch and log data, and Python file changes when apply mode is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write learner.py, learned_patterns.json, self_improve_log.json, and append SKILL.md content when apply mode is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
