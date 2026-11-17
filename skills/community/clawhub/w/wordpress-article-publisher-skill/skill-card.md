## Description:

Generates a structured article from user-provided keywords and publishes it to a WordPress site through the WordPress REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxucai](https://clawhub.ai/user/liuxucai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and WordPress site operators use this skill to draft keyword-based articles and publish them to a WordPress site. It also supports authenticated post management workflows such as category/tag assignment and modification of existing posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish live content to a WordPress site.

Mitigation: Use draft status or a staging site first, then review the generated article before making it public.

Risk: The workflow requires WordPress usernames and application passwords.

Mitigation: Use a dedicated least-privileged WordPress account, avoid passing passwords in reusable shell history when possible, and revoke application passwords after use if exposure is suspected.

Risk: Delete or modify-existing-post workflows can remove live content.

Mitigation: Confirm the exact post ID and intended consequence before running delete or replacement operations.

Risk: Publishing over non-HTTPS URLs can expose credentials.

Mitigation: Use only HTTPS WordPress site URLs for authenticated REST API operations.

## Reference(s):

- [WordPress REST API reference](references/api-reference.md)
- [WordPress application password setup](references/wordpress-setup.md)
- [Chinese encoding fix](references/encoding-fix.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline PowerShell commands and HTML article content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WordPress REST API publishing guidance and script invocations; generated article content is expected to be HTML-formatted before publishing.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
