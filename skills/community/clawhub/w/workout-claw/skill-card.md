## Description: <br>
Log workouts, track progress, compute PRs, edit/delete sessions via a local CLI. Local-first, JSON storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsdevq](https://clawhub.ai/user/dsdevq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to log local workout sessions, query training history, calculate estimated PRs, and summarize muscle volume through the workout-claw CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads, writes, edits, and deletes local workout logs that may contain personal health data. <br>
Mitigation: Install only when the local workout-claw CLI is trusted, and treat workout notes and logs as personal health data. <br>
Risk: The documented delete command has no confirmation prompt. <br>
Mitigation: Confirm the exact session ID with the user before issuing any delete command. <br>
Risk: The edit command opens an interactive editor and may not work in chat-only or Telegram-style agent sessions. <br>
Mitigation: Avoid invoking interactive edit flows in remote chat sessions; provide the session ID or use delete plus log again when appropriate. <br>


## Reference(s): <br>
- [Workout Claw ClawHub Page](https://clawhub.ai/dsdevq/workout-claw) <br>
- [Publisher Profile](https://clawhub.ai/user/dsdevq) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and readable summaries of CLI YAML output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on local JSON workout logs under the user's home directory.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
