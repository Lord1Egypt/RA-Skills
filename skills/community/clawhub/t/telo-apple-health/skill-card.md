## Description:

Connects OpenClaw to Apple Health records synced by the telo iPhone app for sleep, HRV, resting heart rate, activity, workouts, and long-term trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[telo-inc](https://clawhub.ai/user/telo-inc)

### License/Terms of Use:

MIT-0

## Use Case:

External users can connect OpenClaw to their telo account to review Apple Health sleep, HRV, resting heart rate, activity, workouts, and longer-term trends. The skill guides data retrieval and presents summaries while preserving gaps and avoiding diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial, with a local path-like reference unresolved and an install-mechanism note unexplained; the benign verdict has medium confidence.

Mitigation: Review those unresolved aspects before deployment and do not treat the scanner verdict as a complete assessment.

Risk: The connected account contains sensitive Apple Health records.

Mitigation: Authorize access only for the intended account and run `openclaw mcp logout telo` when OpenClaw should no longer have access.

Risk: Incomplete or missing records can lead to misleading health summaries.

Mitigation: Check data availability and coverage, treat missing values as unavailable, and do not diagnose or infer causation from the records.

## Reference(s):

- [telo website](https://telo.health)
- [Weekly health review workflow](references/weekly-health-review.md)
- [Long-term trends workflow](references/long-term-trends.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Text and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health metric summaries with dates, units, and observed coverage where available.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
