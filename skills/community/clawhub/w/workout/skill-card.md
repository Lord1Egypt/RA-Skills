## Description: <br>
Track workouts, log sets, manage exercises and templates with workout-cli, including multi-user profiles for recording gym sessions, viewing history, and analyzing strength progression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gricha](https://clawhub.ai/user/gricha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through workout-cli commands for logging workouts, managing exercises and templates, maintaining profiles, and reviewing training history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local workout CLI can create, edit, or delete workout profiles and records. <br>
Mitigation: Review proposed commands before execution and confirm the intended profile, session, exercise, and set before making changes. <br>
Risk: Workout notes and logs can contain personal health or fitness information. <br>
Mitigation: Only record sensitive details when the user explicitly provides them, and keep responses scoped to the workout data needed for the task. <br>
Risk: Incorrect weights or reps can mislead PR, volume, and progression analysis. <br>
Mitigation: Ask for missing weight or rep values before logging, and use undo, edit, or delete commands to correct mistakes during a session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gricha/workout) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local workout CLI commands; the CLI supports JSON output when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
