## Description:

Web Health Suite helps agents run HTTP health checks, response quality analysis, compliance validation, SSL certificate monitoring, API endpoint verification, and HTML report generation for web applications and services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guo5404](https://clawhub.ai/user/guo5404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, DevOps engineers, and SREs use this skill to check owned or authorized web services for availability, response quality, HTTP compliance, SSL certificate status, API endpoint behavior, and reportable health findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live authenticated checks and broad endpoint verification can expose credentials or affect production services if run outside an approved scope.

Mitigation: Use only systems you own or have written authorization to monitor, prefer test or least-privilege credentials, avoid real session cookies when possible, and document scope before running checks.

Risk: Endpoint verification may use mutating HTTP methods such as POST, PUT, or DELETE.

Mitigation: Override methods to safe read-only checks unless the target environment is designed for safe testing of mutating requests.

Risk: Request rate, concurrency, or proxy settings can disrupt service availability or route sensitive traffic unexpectedly.

Mitigation: Configure rate limits, threads, timeouts, and proxies conservatively, and align monitoring windows and exclusions with the target owner.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; referenced workflows produce JSON status files and HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference target URLs, authentication tokens or cookies, proxy settings, request rates, HTTP methods, timeouts, and output file paths.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
