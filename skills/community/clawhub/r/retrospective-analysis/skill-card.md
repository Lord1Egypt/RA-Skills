## Description:

A project retrospective automation tool for friction identification, failure analysis, and improvement generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terr123123](https://clawhub.ai/user/terr123123)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to capture project retrospectives, identify gate friction and failures, and generate prioritized improvement candidates and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON save, load, and export operations read or write paths selected by the caller.

Mitigation: Use only intended local paths and avoid sensitive or shared locations unless reading or overwriting those files is expected.

Risk: Generated severity, priority, recommendations, and action items are heuristic process-analysis outputs.

Mitigation: Review reports with the project team before using them to drive process changes or accountability decisions.

## Reference(s):

- [Retrospective Analysis on ClawHub](https://clawhub.ai/terr123123/skills/retrospective-analysis)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance, files]

**Output Format:** [Text summaries and JSON retrospective or report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save, load, and export JSON at caller-selected paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
