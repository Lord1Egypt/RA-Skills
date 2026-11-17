## Description:

Professional career roadmap platform that generates personalized learning paths and specialization recommendations for aspiring financial analysts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request personalized financial analyst career roadmaps, specialization options, and curated learning paths from an external API. It is intended for career changers, recent graduates, and working professionals planning financial analysis skill development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted assessment details are shared with the external API operator.

Mitigation: Minimize assessment data to fields needed for roadmap generation and avoid sensitive personal or employment details.

Risk: Supplying userId can enable persistent profile tracking.

Mitigation: Use an opaque sessionId and omit userId unless persistent profile tracking is intentionally required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-financial-analyst)
- [Financial Analyst API route](https://api.mkkpro.com/career/financial-analyst)
- [Financial Analyst API docs](https://api.mkkpro.com:8187/docs)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [JSON API responses that agents may summarize in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Roadmap responses can include phases, milestones, specialization recommendations, estimated duration, and learning resources.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
