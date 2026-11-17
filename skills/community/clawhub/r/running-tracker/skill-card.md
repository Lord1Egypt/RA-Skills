## Description:

Tracks, logs, and analyzes running workout times from casual run reports and stored running history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdocr](https://clawhub.ai/user/fdocr)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record running workouts, calculate pace, speed, and calories, and ask questions about running history, progress, personal bests, trends, and projections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous running messages could be logged with an incorrect distance, date, or time.

Mitigation: Confirm unclear workout details before appending a new entry to runs.md.

Risk: runs.md stores personal running history in the local workspace.

Mitigation: Review the local running log before sharing the workspace or generated outputs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown responses and markdown table entries in runs.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, append, and sort entries in the local runs.md running log.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
