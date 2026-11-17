## Description:

Tests API endpoints by sending requests, validating responses, measuring performance, handling authentication, and generating detailed health reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[underbench2-gif](https://clawhub.ai/user/underbench2-gif)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to test API endpoints, validate expected responses, measure latency, and produce health reports with per-endpoint results and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make HTTP requests to user-specified APIs, including write-capable methods such as POST, PUT, or DELETE.

Mitigation: Use test accounts or non-production environments for endpoints that may create, change, or delete data.

Risk: Authentication headers or tokens may be needed for some checks.

Mitigation: Provide sensitive tokens only when necessary and prefer scoped credentials for testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/underbench2-gif/skills/ub2-api-health-checker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown health report with endpoint status, response timing metrics, validation details, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTP methods, URLs, expected status codes, timeouts, headers, request bodies, authentication details, and performance metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
