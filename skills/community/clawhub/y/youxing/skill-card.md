## Description:

Looks up Youxing youth community event listings and activity details, returning JSON by default and Markdown when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longbai](https://clawhub.ai/user/longbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer explicit questions about Youxing youth community activities, including recent event lists and details for a specific activity ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags unsafe shell-based instructions for user-provided activity IDs.

Mitigation: Validate campaign IDs and pass them as safe process arguments or through a scoped HTTP tool before execution.

Risk: The security evidence flags broad activation and third-party API calls.

Mitigation: Invoke the skill only for explicit Youxing activity queries and disclose that requests contact api.cumen.fun.

Risk: The third-party event API may return unsorted or changing activity data.

Mitigation: Treat returned event details as live third-party data and sort or verify results before presenting time-sensitive summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longbai/skills/youxing)
- [Cumen service API base](https://api.cumen.fun/api/xx.cumen.v1.CumenService)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [JSON by default; Markdown tables or detail summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses UTC+8 time conversion and maps event status, kind, price, address, image, share, and comment fields from the activity API response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
