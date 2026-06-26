## Description: <br>
Publish articles to WordPress blogs via REST API with post creation, category and tag management, and SEO-friendly English slug generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hugogu](https://clawhub.ai/user/hugogu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to publish or update WordPress blog posts from prepared article content. It helps prepare metadata, create missing categories and tags, convert Markdown-style content to HTML, and return the public post URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make authenticated changes to live public WordPress content. <br>
Mitigation: Use a least-privileged WordPress account and require explicit confirmation of the target site, title, status, categories, and tags before publishing or updating. <br>
Risk: Default URL or username fallbacks could send content to an unintended WordPress target. <br>
Mitigation: Remove default URL and user fallbacks, and verify credentials and the target site from environment configuration before any REST API request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hugogu/wordpress-blogger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and publication result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output a public WordPress post URL, title, category, and tags after publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
