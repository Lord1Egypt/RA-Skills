## Description:

Indexes ambient sound events by device and time so users can ask plain-English questions about incidents and retrieve timestamped results with confidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Property managers, alarm operators, and rental operators use the skill to index sound events from monitored devices and review incidents across devices and dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambient audio, speech-derived data, incident queries, and audit notes are sent to a third-party persistent memory service.

Mitigation: Use only with an approved vendor and authority to process site audio; confirm consent, recording-law requirements, and the provider's retention, deletion, access-control, and audit policies.

Risk: Incident records can contain sensitive site or personal identifiers.

Mitigation: Avoid unnecessary identifiers in audio submissions, queries, and audit notes.

## Reference(s):

- [Sound Event Memory release](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/sound-event-memory)
- [BlueColumn API documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain-language incident answers and Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Incident answers may include device identifiers, timestamps, and confidence scores.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
