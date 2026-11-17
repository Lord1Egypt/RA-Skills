## Description:

Tracks skill execution details, including matched skills, decomposed tasks, execution status, outputs, and timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abo-hub](https://clawhub.ai/user/abo-hub)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to record skill and tool execution details across conversation turns for analysis and debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content may be retained in tracking records.

Mitigation: Install only where users have consented to logging and where retention, access controls, and deletion procedures are defined.

Risk: Assistant replies may be altered by an appended Deck reminder.

Mitigation: Review whether reply modification is acceptable for the deployment and disclose the behavior to users or administrators.

Risk: Local service and network probing may expose environment details such as a Deck URL.

Mitigation: Run only in environments where local service discovery and external IP checks are permitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abo-hub/skills/skill-tracker)

## Skill Output:

**Output Type(s):** [Files, JSON, Text, Shell commands]

**Output Format:** [JSONL records and short text reminder]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends one record per tracked conversation turn and may append a Deck reminder to the assistant reply.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
