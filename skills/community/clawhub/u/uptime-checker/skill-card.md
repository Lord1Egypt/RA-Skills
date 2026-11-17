## Description:

Uptime Checker is a lightweight URL uptime checker and response time monitor for checking website and API availability, response times, history, redirects, and SSL issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check website and API uptime, measure response times, detect redirects or SSL failures, and produce status reports for scripts or operational reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to user-provided URLs.

Mitigation: Run it only against endpoints you are authorized to test, and review target URLs before execution.

Risk: Authorization headers, cookies, or API keys passed on the command line may be exposed to endpoints or through redirect handling.

Mitigation: Avoid sensitive credentials in headers; use non-sensitive health-check credentials and disable redirects when checking authenticated endpoints.

Risk: Saved history files can retain endpoint URLs, statuses, response timings, timestamps, and error details.

Mitigation: Store history files in a deliberate location with appropriate access controls and retention practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/uptime-checker)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON status results, with Markdown-facing shell command examples and operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save endpoint check history containing URLs, statuses, timings, timestamps, and errors when history output is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
