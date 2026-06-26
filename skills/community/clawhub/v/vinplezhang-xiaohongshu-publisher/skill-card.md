## Description: <br>
Draft and publish posts to Xiaohongshu/RED, including content drafting, cover image generation, review, and browser-based publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinplezhang](https://clawhub.ai/user/vinplezhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and automation operators use this skill to draft Xiaohongshu posts, generate 1080x1440 cover images, route drafts for approval, and publish through a logged-in browser session or a manual fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Xiaohongshu creator session and publish content through browser automation. <br>
Mitigation: Review the final title, body, hashtags, and cover image before approving any live publish action; use cron only to prepare drafts unless a separate explicit approval process is in place. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vinplezhang/vinplezhang-xiaohongshu-publisher) <br>
- [Browser Publishing Guide](references/browser-publish.md) <br>
- [Xiaohongshu Content Guide](references/content-guide.md) <br>
- [Xiaohongshu Creator Portal](https://creator.xiaohongshu.com/publish/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, generated draft text, cover image file paths, and browser publishing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a 1080x1440 PNG cover image and formatted manual-posting content when browser automation is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
