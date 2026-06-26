## Description: <br>
Creates daily WeChat official-account articles by searching current topics, drafting SEO-oriented travel and food HTML content, adding images, and saving the result as a WeChat draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimo970](https://clawhub.ai/user/jimo970) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators of WeChat official accounts use this skill to generate travel and food article drafts, prepare SEO-friendly titles and structure, upload images, and stage drafts for review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive WeChat official-account credentials and may also use Feishu bot credentials. <br>
Mitigation: Install only when those integrations are intended, store credentials outside shared artifacts, scope credentials narrowly, and rotate them if exposed. <br>
Risk: The server security summary flags under-scoped Feishu/Douyin distribution features beyond the core WeChat draft workflow. <br>
Mitigation: Keep Feishu and Douyin paths disabled or remove them when only WeChat draft creation is needed. <br>
Risk: Remote image download behavior is called out as unsafe in the security guidance. <br>
Mitigation: Avoid untrusted image URLs until TLS verification is fixed, and review all local files and images before upload. <br>
Risk: Generated articles and uploaded media may contain inaccurate, misleading, or unsuitable material for publication. <br>
Mitigation: Review every WeChat draft, image, title, and outbound notification before publishing or sending. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jimo970/wechat-daily-article) <br>
- [Content type templates](artifact/references/content-types.md) <br>
- [Image prompt guidance](artifact/references/image-prompts.md) <br>
- [WeChat official-account SEO guidance](artifact/references/seo-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files, guidance] <br>
**Output Format:** [Markdown instructions with HTML article content and Python/shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat official-account credentials; optional Feishu bot credentials; writes temporary article/image files and creates drafts through external APIs.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
