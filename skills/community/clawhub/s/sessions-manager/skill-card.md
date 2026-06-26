## Description: <br>
Manage OpenClaw agent sessions - list active/completed sessions, view session details, and delete sessions by ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[6eanut](https://clawhub.ai/user/6eanut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect active and completed agent sessions, review session metadata, and clean up stale or unwanted session records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deleting a session permanently removes the matching OpenClaw session metadata entry and history file without a confirmation prompt. <br>
Mitigation: Run the list command first, verify the exact session ID or key, and back up ~/.openclaw/agents/main/sessions if session history or audit trails matter. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/6eanut/sessions-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [List output includes session key, ID, label, status, model, start time, and duration; delete actions remove matching local session metadata and history files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
