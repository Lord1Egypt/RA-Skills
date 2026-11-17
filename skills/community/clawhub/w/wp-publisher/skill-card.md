## Description:

Publish WordPress posts via REST API from any OpenClaw channel (WeChat/QQ/DingTalk/etc). AI writes in Markdown, auto-converts to HTML, posts to your blog, and returns the link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxihaohao](https://clawhub.ai/user/foxihaohao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and blog owners use this skill to draft Markdown content, convert it to HTML, and publish or manage posts through a configured WordPress REST API endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe credential handling can expose WordPress credentials or application passwords.

Mitigation: Use a dedicated least-privilege WordPress application password and avoid embedding credentials directly in shared commands or logs.

Risk: Commands using relaxed TLS behavior can hide endpoint or certificate problems.

Mitigation: Use only an HTTPS WordPress endpoint with normal certificate validation and remove -k from curl commands before use.

Risk: Permanent delete operations can irreversibly remove WordPress posts.

Mitigation: Avoid enabling delete or update operations unless they are explicitly needed and protected by strong confirmation controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foxihaohao/skills/wp-publisher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WordPress REST API requests and published post links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
