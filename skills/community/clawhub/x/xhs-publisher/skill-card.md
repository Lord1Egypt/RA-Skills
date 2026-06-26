## Description: <br>
Publish notes (posts) to Xiaohongshu (小红书) via the Creator Platform using browser automation (CDP). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Waao666](https://clawhub.ai/user/Waao666) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators and operators use this skill to guide an agent through publishing Xiaohongshu notes with images, Chinese text, hashtags, and publication checks in a logged-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Xiaohongshu account and may publish public content without a clear final confirmation step. <br>
Mitigation: Before publishing, require the agent to show the exact title, body, media, target account, and visibility, then ask for explicit user approval. <br>
Risk: Generated or uploaded images with broken Chinese text rendering may cause publication failure or content takedown. <br>
Mitigation: Verify cover images before upload and use a full CJK font such as DroidSansFallbackFull.ttf when rendering Chinese text. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Waao666/xhs-publisher) <br>
- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com) <br>
- [Xiaohongshu Publish Page](https://creator.xiaohongshu.com/publish/publish) <br>
- [Xiaohongshu User Profile URL Pattern](https://www.xiaohongshu.com/user/profile/{userId}) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown with browser automation steps and JavaScript CDP snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Xiaohongshu browser session and user review before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
