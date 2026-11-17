## Description:

Query the X2C personal dashboard to get real-time KPI data, earnings trends, platform views, recent transactions, and earning projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoyalab](https://clawhub.ai/user/luoyalab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to answer X2C dashboard questions about earnings, ROI, mining status, platform performance, recent activity, and earning project lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends authenticated requests to the X2C dashboard API endpoint.

Mitigation: Install only if the X2C API endpoint is trusted and use a scoped or revocable X2C_API_KEY where possible.

Risk: Returned dashboard data may include sensitive earnings, transaction, project, and platform-view information.

Mitigation: Invoke the skill only for X2C dashboard questions and avoid exposing returned financial details beyond the user's requested scope.

Risk: Failed API calls can return error JSON instead of dashboard data.

Mitigation: Check for success: true before presenting results, as the artifact instructs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoyalab/skills/x2c-real-dashboard)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Text]

**Output Format:** [JSON responses from shell scripts, summarized as text or Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X2C_API_KEY. Numeric script arguments are bounded for trend days, activity limit, and page size.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
