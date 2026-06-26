## Description: <br>
Drafts, formats, reviews, and publishes 小红书 (Xiaohongshu/RED) posts, including cover image generation and browser-based publishing with manual fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuf1011](https://clawhub.ai/user/yuf1011) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and operators use this skill to prepare Xiaohongshu posts, generate 1080x1440 cover images, obtain review approval, and publish through a logged-in browser session or manual copy-paste fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content from a logged-in Xiaohongshu creator session. <br>
Mitigation: Review the title, body, tags, and cover image before approving publication, and require explicit approval before each publish action. <br>
Risk: Scheduled use could publish posts without timely human review if configured too broadly. <br>
Mitigation: Keep scheduled jobs limited to draft-and-review workflows unless each post is intentionally authorized. <br>
Risk: Generated cover images may be written to local paths selected by the user or agent. <br>
Mitigation: Save generated covers only to ordinary working directories and avoid sensitive or system paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuf1011/xiaohongshu-publisher) <br>
- [Content guide](artifact/references/content-guide.md) <br>
- [Browser publishing guide](artifact/references/browser-publish.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown draft text, browser publishing guidance, shell commands, and PNG cover image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates 1080x1440 PNG cover images and requires explicit user approval before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
