## Description:

Use when completing tasks, implementing major features, or before merging to verify work meets requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to request a structured code review after meaningful implementation work, before merges, or when a fresh technical review is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a referenced code-reviewer subagent and template that may not exist in the user's environment.

Mitigation: Confirm that the superpowers:code-reviewer subagent and code-reviewer.md template are installed before relying on the skill.

Risk: Using the skill shares implementation details, requirements, and git commit ranges with the reviewer process.

Mitigation: Review the code and commit range for sensitive information before dispatching the code-reviewer subagent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soponcd/skills/timeflow-requesting-code-review)
- [Skill homepage](https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/requesting-code-review)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline shell commands and review-request placeholders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the agent to share implementation summaries, requirements, and git commit ranges with a code-reviewer subagent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
