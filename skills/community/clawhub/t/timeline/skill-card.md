## Description:

Log dated events and facts to a queryable personal timeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levineam](https://clawhub.ai/user/levineam)

### License/Terms of Use:

MIT-0

## Use Case:

People using ClawHub agents can record dated personal facts, family moments, milestones, and medical events without placing them on a calendar. They can later search or list those timeline entries by text, date, or tag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script has input-handling flaws that could allow crafted entries or options to run local commands.

Mitigation: Review or fix the script before installing, especially validation and quoting for event text, dates, tags, times, and --limit.

Risk: Timeline entries can contain persistent sensitive personal, family, or medical details.

Mitigation: Treat the configured vault and Timeline.md as sensitive storage, restrict access, and avoid logging unnecessary private details.

Risk: Broad timeline triggers may capture information the user did not intend to store.

Mitigation: Prefer explicit write commands such as "add to timeline" before recording an entry.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/levineam/skills/timeline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown timeline entries and plain-text command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and searches a persistent Timeline.md file in the configured vault.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
