## Description:

Manage branded redirects, audit traffic analytics, and execute semantic link queries using URLMitra.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urlmitra](https://clawhub.ai/user/urlmitra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing operations teams use this skill to create branded shortlinks, check redirect health, analyze link performance, and search URLMitra workspace resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command examples substitute user-provided URL, alias, and search text into shell and JSON templates, which could allow crafted input to run local shell commands.

Mitigation: Use a tightly scoped URLMitra API key, avoid running generated command templates with untrusted input, and build request JSON with jq or another structured API helper before execution.

Risk: The skill sends workspace link-management requests to URLMitra APIs using an API key.

Mitigation: Store URLMITRA_API_KEY securely, limit its permissions to the needed workspace actions, and rotate it if command history or logs may have exposed it.

## Reference(s):

- [URLMitra Link Manager on ClawHub](https://clawhub.ai/urlmitra/skills/urlmitra-link-manager)
- [URLMitra links endpoint](https://api.urlmitra.com/api/v1/links)
- [URLMitra health summary endpoint](https://api.urlmitra.com/api/v1/health/summary)
- [URLMitra semantic search endpoint](https://api.urlmitra.com/api/v1/mitra/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires URLMITRA_API_KEY plus curl and jq.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
