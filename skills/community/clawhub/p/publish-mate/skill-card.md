## Description: <br>
Fetch global news from RSS/API sources, auto-generate articles with images, and publish to WordPress or custom CMS platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankeito](https://clawhub.ai/user/tankeito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, site owners, and automation-focused developers use this skill to fetch news, draft article content with images, and publish or preview posts for WordPress or compatible CMS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live website content. <br>
Mitigation: Run preview or dry-run mode first and set the default post status to draft before allowing live publication. <br>
Risk: WordPress credentials may be exposed if TLS verification is bypassed. <br>
Mitigation: Fix or remove the TLS verification bypass before production use and use a dedicated low-privilege WordPress application password. <br>
Risk: Untrusted custom endpoints or direct image URLs can affect fetched content and media. <br>
Mitigation: Use trusted RSS/API and image sources, and review generated posts and media before publication. <br>


## Reference(s): <br>
- [Publish-Mate on ClawHub](https://clawhub.ai/tankeito/publish-mate) <br>
- [Publisher profile](https://clawhub.ai/user/tankeito) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Example configuration](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can execute scripts that fetch articles and images, write local logs and history, and publish or preview CMS posts based on user configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
