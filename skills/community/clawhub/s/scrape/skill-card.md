## Description:

Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to plan legally cautious web scraping by checking robots.txt, terms, authentication boundaries, request rate limits, and privacy-sensitive data handling before writing or running scraping code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample robots.txt helper can allow scraping when the robots.txt check fails.

Mitigation: Change robots.txt errors to fail closed or ask for explicit approval before proceeding.

Risk: Fetcher examples can be risky in shared tools or workflows that accept user-supplied URLs.

Mitigation: Add URL, redirect, and IP validation before using the fetcher with untrusted inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/scrape)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checklist-style guidance and sample request, robots.txt, rate limiting, and audit logging patterns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
