## Description:

Queries TTPOS restaurant business data through the ttpos-agent API and helps produce revenue, order, payment, menu item, member, shift, and time-period reports after first fetching the service query guide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bendaye](https://clawhub.ai/user/bendaye)

### License/Terms of Use:

MIT-0

## Use Case:

External TTPOS users and operators use this skill to ask for restaurant sales, order, payment, item ranking, member, shift, and time-period summaries. The agent fetches the service query guide, selects an accessible merchant, submits SELECT-style SQL to the ttpos-agent API, and returns concise human-facing report summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a bearer token and merchant data to an external ttpos-agent service.

Mitigation: Install only when the service is trusted and use a least-privilege, preferably read-only API key.

Risk: The agent submits generated SQL to the service, and package evidence does not show backend safeguards.

Mitigation: Confirm the service enforces tenant isolation, SELECT-only execution, row or date limits, SQL auditing, and a trusted query guide source before use.

Risk: Missing or stale query guidance can cause incorrect table names, field use, or duplicated statistics.

Mitigation: Fetch GET /api/v1/query/guide before constructing SQL and keep individual query ranges limited as directed by the skill.

## Reference(s):

- [TTPOS Agent ClawHub page](https://clawhub.ai/bendaye/skills/ttpos-agent)
- [bendaye publisher profile](https://clawhub.ai/user/bendaye)
- [ttpos-agent service endpoint](https://claw.doge6.com)
- [ttpos-agent Web panel](https://claw.doge6.com/web/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or concise text summaries with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LIGHT_BRIDGE_API_KEY and communicates with the ttpos-agent external API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
