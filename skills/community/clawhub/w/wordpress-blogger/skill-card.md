## Description:

Publishes articles to WordPress blogs through REST API calls, including post creation, category and tag management, markdown-to-HTML conversion, and SEO-friendly slug generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugogu](https://clawhub.ai/user/hugogu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare and publish articles to a configured WordPress blog, including taxonomy setup, slug generation, and a public URL response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live publishing power on a WordPress site.

Mitigation: Prefer draft-first publishing and require explicit confirmation before publishing or updating public content.

Risk: WordPress credentials could grant broader access than the publishing task requires.

Mitigation: Use a dedicated low-privilege WordPress application password and never hardcode credentials in generated scripts.

Risk: Publishing to an unintended or insecure endpoint could expose credentials or content.

Mitigation: Require HTTPS and a known WordPress host before sending REST API requests.

Risk: Sourcing a shared .env file as shell code can execute unintended content.

Mitigation: Avoid sourcing shared .env files directly; load only the required WordPress variables through a controlled mechanism.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hugogu/skills/wordpress-blogger)
- [Publisher profile](https://clawhub.ai/user/hugogu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and a publication summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a WordPress site URL, username, and application password supplied through environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
