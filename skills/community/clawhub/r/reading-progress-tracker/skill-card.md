## Description:

Organize reading into Now, Next, Later, and Drop, then track current position, format, purpose, next stopping point, and lightweight session notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to organize current, queued, paused, and dropped books, then turn user-provided progress and notes into a lightweight reading dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect the dashboard to sync with reading services or persist progress automatically.

Mitigation: Make clear that the skill generates a manual markdown dashboard from user-provided notes and does not sync or store progress by itself.

Risk: Heuristic extraction can miss or misclassify book titles, formats, purposes, progress, or next stopping points.

Mitigation: Review the generated dashboard before relying on it and correct any reading status or queue details in the next prompt.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single generated dashboard from user-provided reading progress; no external sync or automatic persistence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
