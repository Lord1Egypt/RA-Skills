## Description: <br>
Use when illustrating a Markdown article with high-finish editorial visuals, visual-bible planning, structured prompts, optional Qiniu upload, and inserted image references for article publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhylq](https://clawhub.ai/user/zhylq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and publishing teams use this skill to plan, generate, and insert editorial illustrations into Markdown articles. It creates a visual bible, illustration outline, structured prompts, local image assets, an illustrated article copy, and optional CDN URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article content and image-generation requests may be sent to external image services or an under-disclosed third-party image relay. <br>
Mitigation: Use only articles that may be shared with external image services, set IMAGE_BASE_URL or XIAOMI_BASE_URL to a trusted endpoint, and avoid relying on defaults. <br>
Risk: API keys for image providers or Qiniu upload can expose broader account access than the skill needs. <br>
Mitigation: Use least-privilege API keys, store them outside committed files, and rotate or revoke keys after testing. <br>
Risk: Enabling upload can publish generated images through Qiniu/CDN when local-only output was intended. <br>
Mitigation: Keep upload=false unless remote hosting is intentional, and review generated assets before enabling upload. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhylq/zhy-article-illustrator) <br>
- [Configuration schema](references/config-schema.md) <br>
- [Prompt guide](references/prompt-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text prompts, Image files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown files, prompt text files, PNG image files, local paths, and optional CDN URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates article.illustrated.md plus illustration planning assets under illustrations/<slug>/; optional upload returns CDN URLs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
