## Description: <br>
Publishes one or multiple Markdown articles to a WeChat Official Account draft box, with combined drafts, cover images, custom styling, inline image upload, digest extraction, and optional immediate publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x402spark-jpg](https://clawhub.ai/user/x402spark-jpg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to turn Markdown articles into WeChat Official Account drafts or reviewed public posts. It supports single-article and multi-article workflows, including dry-run previews before upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat MP credentials to create drafts and can publish publicly when explicitly requested. <br>
Mitigation: Use environment variables or a protected credentials file, avoid committing secrets, start with --dry-run or draft-only mode, and enable --publish only after review. <br>
Risk: Markdown content and image references are uploaded to external services during non-dry-run execution. <br>
Mitigation: Review article content and local image references before upload, and use dry-run previews to inspect rendered output first. <br>
Risk: Cron automation can repeatedly push or publish content without interactive review. <br>
Mitigation: Use cron only after the workflow has been tested, keep publication separate from draft creation where possible, and monitor logs for WeChat API errors. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/x402spark-jpg/wechat-multi-publisher) <br>
- [WeChat Official Account API Endpoint](https://api.weixin.qq.com/cgi-bin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local HTML previews during dry runs and use WeChat API calls to create drafts or submit publishing requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
