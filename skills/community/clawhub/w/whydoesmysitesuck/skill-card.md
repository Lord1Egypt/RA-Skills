## Description:

Grade any website 0-100 across categories like SEO, security, performance, accessibility, content, email authentication, and AI/LLM readiness using the free whydoesmysitesuck.com API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcindudekdev](https://clawhub.ai/user/marcindudekdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and agents use this skill to obtain a concise website quality baseline, compare domains, and identify weak areas across SEO, security, performance, accessibility, content, email authentication, and AI/LLM readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill shares the audited domain with whydoesmysitesuck.com and may trigger a crawl of a live site.

Mitigation: Use it only for domains the user owns, has permission to check, or has a legitimate reason to audit.

Risk: API key registration shares an email address with the service.

Mitigation: Ask the user before registration and use the user's provided email address rather than an invented or third-party address.

Risk: Rate limits, scan delays, failed scans, or stale results can affect how current or complete an audit result is.

Mitigation: Honor Retry-After responses, avoid retry loops, report failed scans plainly, and treat stale results as older baselines unless a refreshed scan completes.

## Reference(s):

- [whydoesmysitesuck.com](https://whydoesmysitesuck.com)
- [whydoesmysitesuck.com API Documentation](https://whydoesmysitesuck.com/api)
- [OpenAPI Specification](https://whydoesmysitesuck.com/openapi.json)
- [ClawHub Skill Page](https://clawhub.ai/marcindudekdev/skills/whydoesmysitesuck)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes score, grade, weakest categories, and report URL when returned by the API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
