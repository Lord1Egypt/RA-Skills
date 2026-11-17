## Description:

Create, edit, and publish WordPress posts via REST API with full Gutenberg block support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chirukinbb](https://clawhub.ai/user/chirukinbb)

### License/Terms of Use:


## Use Case:

Developers, content operators, and automation agents use this skill to prepare Gutenberg-compatible WordPress content, upload media, manage taxonomy metadata, and create or publish posts through the WordPress REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update live WordPress content when connected to a real site.

Mitigation: Use a dedicated low-privilege WordPress account and keep posts as drafts until a human reviews the generated content and metadata.

Risk: Credentials and target site settings are required for REST API writes.

Mitigation: Store credentials in environment variables or a secure secret store, confirm the exact WP_URL before writes, and avoid placing real passwords directly in shell commands.

Risk: Some troubleshooting examples show insecure patterns such as disabled TLS verification or wildcard credentialed CORS.

Mitigation: Use those examples only to understand failure modes, and do not copy verify=False or wildcard credentialed CORS settings into production environments.

## Reference(s):

- [WordPress REST API Reference](references/api_reference.md)
- [Gutenberg Block Examples](references/common_blocks.md)
- [Troubleshooting WordPress API Issues](references/troubleshooting.md)
- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline Python, shell, JSON, and Gutenberg HTML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce WordPress REST API request patterns, Gutenberg block markup, publishing scripts, media upload reports, and configuration examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
