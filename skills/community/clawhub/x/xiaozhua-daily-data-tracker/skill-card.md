## Description:

Tracks daily key metrics in a historical table, including revenue, gross adds, EOP, paid subscribers, platform splits, week-over-week calculations, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirowangl-ops](https://clawhub.ai/user/mirowangl-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, operators, and agent users use this skill to append daily business metrics to a historical tracker, compare results week over week, and flag declining trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily revenue and subscriber metrics may be stored in the named persistent memory file.

Mitigation: Use the skill only if that storage location is acceptable, or keep the metrics in a project-local or access-controlled document.

Risk: Incomplete daily data or baseline values could lead to misleading week-over-week or trend conclusions.

Mitigation: Confirm data completeness before marking final values and preserve baseline notes when applicable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown table rows and concise analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or proposes updates for a persistent daily metrics file when the agent has access to the named memory path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
