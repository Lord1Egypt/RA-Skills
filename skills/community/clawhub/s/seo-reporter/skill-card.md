## Description:

Audit a URL for SEO factors and generate an actionable markdown report covering title, meta description, heading structure, canonical tags, robots.txt, and sitemap.xml.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and SEO practitioners use this skill to audit a single webpage URL and receive a scored markdown report with specific optimization recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unrestricted live HTTP requests to arbitrary user-supplied URLs from the agent environment.

Mitigation: Use it only with trusted public URLs; avoid attacker-supplied, internal, or sensitive network targets; apply URL validation or network egress controls in sensitive environments.

## Reference(s):

- [Seo Reporter ClawHub Skill Page](https://clawhub.ai/kryzl19/skills/seo-reporter)
- [Publisher Profile](https://clawhub.ai/user/kryzl19)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown SEO audit report with scored findings and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and makes live HTTP requests to the provided URL, robots.txt, and sitemap.xml.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
