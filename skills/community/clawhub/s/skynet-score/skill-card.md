## Description:

Search CertiK Skynet project scores, retrieve blockchain project security ratings, compare score breakdowns, and show integration examples for the public project search endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certik-ai](https://clawhub.ai/user/certik-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to look up blockchain project Skynet scores, tiers, update times, and component score breakdowns from CertiK's public project search API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project search keywords are sent to CertiK's public API.

Mitigation: Confirm that requested project names or keywords are appropriate to send to the public endpoint before execution.

Risk: The skill runs a bundled Python script with outbound HTTPS access.

Mitigation: Review the script and permit network access only when the user intends to query CertiK's public API.

## Reference(s):

- [CertiK Public Projects API](https://open.api.certik.com/projects)
- [CertiK Public API Base URL](https://open.api.certik.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown summaries with optional JSON, Python, or curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw API payload excerpts when requested; results depend on the public CertiK API response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
