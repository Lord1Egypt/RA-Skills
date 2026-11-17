## Description:

Track workouts, log sets, manage exercises and templates with workout-cli. Supports multi-user profiles. Use when helping users record gym sessions, view history, or analyze strength progression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gricha](https://clawhub.ai/user/gricha)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to guide workout-cli sessions for tracking workouts, logging accurate sets, managing exercises and templates, and reviewing workout history or progression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes commands that modify workout records, including destructive profile deletion.

Mitigation: List profiles and confirm the exact profile name before deleting a profile or making irreversible record changes.

Risk: Incorrect or assumed weight and rep values can corrupt workout history, PRs, volume, and progression analysis.

Mitigation: Ask for missing weight or rep values before logging sets, and use undo, edit, or delete commands to correct mistakes during a session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gricha/skills/workout)
- [Publisher profile](https://clawhub.ai/user/gricha)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workout-cli commands that support --json output.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
