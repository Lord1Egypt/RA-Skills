## Description:

Fetch global news from RSS/API sources, auto-generate articles with images, and publish to WordPress or custom CMS platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tankeito](https://clawhub.ai/user/tankeito)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure an automated news publishing workflow that fetches articles, sources images, composes posts, and publishes or previews them in WordPress or a custom CMS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish live CMS content from fetched news and image sources.

Mitigation: Default first runs to preview or draft and review generated articles before allowing live publication.

Risk: Unsafe TLS handling and HTTP CMS URLs can weaken transport security.

Mitigation: Require HTTPS with normal certificate validation and avoid HTTP CMS URLs before installation or publishing.

Risk: Broad URL fetching can contact untrusted news, image, or custom API destinations.

Mitigation: Restrict news, image, and custom API URLs to trusted public destinations.

Risk: WordPress application passwords and API keys may grant publishing or external service access.

Mitigation: Use a dedicated low-privilege WordPress application password and keep secrets in environment variables.

## Reference(s):

- [Publish-Mate ClawHub listing](https://clawhub.ai/tankeito/skills/publish-mate)
- [Publisher profile](https://clawhub.ai/user/tankeito)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Configuration example](artifact/config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and generated article content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create runtime config, logs, cached images, publishing history, CMS posts, uploaded media, and status reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
