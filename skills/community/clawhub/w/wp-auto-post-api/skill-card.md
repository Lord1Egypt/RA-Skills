## Description:

Publish SEO-optimized articles to WordPress via REST API with RankMath meta fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l1angjy](https://clawhub.ai/user/l1angjy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to publish approved SEO article JSON to WordPress as drafts or posts while setting RankMath title, description, and focus keyword metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a WordPress Application Password and can create or update web content through the WordPress REST API.

Mitigation: Install only in a trusted workspace, keep the .env file private, and use a dedicated WordPress account with the minimum post-editing permissions.

Risk: Publishing to a live WordPress site can expose incomplete or incorrect SEO content.

Mitigation: Test with draft status first and rely on the approval step before publishing each article.

Risk: REST API credential use over an insecure site can expose credentials.

Mitigation: Verify WP_SITE_URL starts with https:// before using the skill.

Risk: The WordPress setup snippet exposes selected RankMath meta fields through the REST API.

Mitigation: Remove the snippet and revoke the application password if the skill is no longer used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/l1angjy/skills/wp-auto-post-api)
- [Rank Math SEO](https://rankmath.com/)
- [Code Snippets WordPress Plugin](https://wordpress.org/plugins/code-snippets/)
- [Artifact README](artifact/README.md)
- [WordPress REST Meta Setup Snippet](artifact/docs/wordpress-setup.php)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, code]

**Output Format:** [Plain text and Markdown guidance with shell commands and structured JSON result output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WordPress REST API credentials and article JSON; defaults posts to draft unless publish is specified.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
