## Description:

Generate structured meeting minutes from transcripts or raw notes by extracting key decisions, action items, owners, and follow-ups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and team leads use this skill to turn transcripts, raw notes, or concise summaries into structured meeting records for standups, 1:1s, client meetings, design reviews, retrospectives, and steering meetings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes may be written to a local meetings/ folder and retained there.

Mitigation: Avoid using the skill for confidential meetings unless local retention is acceptable, or instruct the agent not to save the notes.

Risk: For recurring meetings, prior notes in meetings/ may be read for continuity.

Mitigation: Review existing notes in that folder and remove sensitive or irrelevant material before using recurrence continuity.

Risk: Generated minutes may contain uncertain decisions, owners, deadlines, or follow-ups when the source transcript is incomplete or ambiguous.

Mitigation: Review the generated notes before distribution and ask the agent to mark uncertain items for confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/skills/zcx-meeting-notes)
- [Publisher profile](https://clawhub.ai/user/zhaocaixia888)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown meeting notes saved as local .md files with structured sections and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save notes under meetings/YYYY-MM-DD_[topic-slug].md and may use prior notes in meetings/ for recurring-meeting continuity.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
