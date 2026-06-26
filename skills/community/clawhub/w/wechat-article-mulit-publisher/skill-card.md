## Description: <br>
Extracts articles from Markdown files or web page links and publishes them to WeChat Official Accounts, with multi-account management, standard and viral templates, automatic cover image generation, and draft publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diwuwudi123](https://clawhub.ai/user/diwuwudi123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure one or more WeChat Official Accounts, preview rendered articles, create drafts, upload images, publish content, query status, and manage drafts from an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat Official Account credentials and can create drafts, upload images, publish articles, and delete drafts. <br>
Mitigation: Keep config.json out of shared repositories, use --dry-run before API actions, and verify the selected account, publish intent, and media_id before publishing or deleting content. <br>
Risk: The skill can fetch and upload article or image URLs supplied to it. <br>
Mitigation: Avoid untrusted article and image URLs, and review fetched content before using publish or upload operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diwuwudi123/wechat-article-mulit-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local HTML previews and may invoke WeChat API operations when run outside dry-run mode.] <br>

## Skill Version(s): <br>
1.3.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
