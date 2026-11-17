## Description:

Parse and analyze GPX route files for trail running, cycling, hiking, and race planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forrestisrunning](https://clawhub.ai/user/forrestisrunning)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and outdoor-planning agents use this skill to parse user-provided GPX route files, extract checkpoints and elevation statistics, and produce pacing tables, roadbooks, and practical route guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GPX files may reveal sensitive location history or planned routes.

Mitigation: Use the skill only with GPX files the user intentionally provides or references, and avoid sharing route details beyond the requested analysis.

Risk: Pacing and terrain recommendations can be misleading if route files lack official checkpoints, surface details, weather, or athlete context.

Mitigation: Separate parsed route facts from assumptions, label inferred checkpoints or terrain clearly, and ask for missing race or athlete details before giving precise pacing advice.

## Reference(s):

- [Read GPX ClawHub listing](https://clawhub.ai/forrestisrunning/skills/read-gpx)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown route summaries and tables, optional JSON parser output, and concise guidance text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route facts, waypoint or checkpoint tables, segment statistics, pacing targets, clock-time roadbooks, and clearly labeled assumptions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
