## Description:

Error tracking, correction logging, and pattern detection via the SwarmRecall API for tracking agent mistakes, corrections, and discoveries, surfacing recurring issues, and promoting learnings into actionable rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waydelyle](https://clawhub.ai/user/waydelyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist errors, corrections, discoveries, and recurring patterns through the SwarmRecall API so future sessions can retrieve and apply prior learnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command failures, corrections, discoveries, private paths, code, or other sensitive content may be stored on SwarmRecall servers.

Mitigation: Get user consent before storing user-provided or sensitive content, and add a redaction or approval step before sending failure details or command output.

Risk: SWARMRECALL_API_URL can redirect requests away from the intended production service.

Mitigation: Verify the override is unset or points only to the intended trusted HTTPS service before use.

Risk: Shared-pool learnings and promotion candidates can shape future behavior with untrusted or incorrect suggestions.

Mitigation: Treat shared-pool results as suggestions, review promotion candidates with the user, and avoid acting on promoted learnings without approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/waydelyle/skills/swarmrecall-learnings)
- [SwarmRecall Homepage](https://www.swarmrecall.ai)
- [SwarmRecall API Base URL](https://swarmrecall-api.onrender.com)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls, Configuration, Guidance]

**Output Format:** [Markdown with JSON and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SWARMRECALL_API_KEY for authentication and may use SWARMRECALL_API_URL to override the API base URL.]

## Skill Version(s):

1.1.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
