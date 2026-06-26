## Description: <br>
Publishes images or videos to Xiaohongshu (Little Red Book) using Playwright after a user-authenticated browser session is saved. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[widebluesky](https://clawhub.ai/user/widebluesky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, creators, and developers use this skill to upload media, titles, and captions to Xiaohongshu through Creator Studio after completing a manual login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The saved Playwright session state can grant posting access to the user's Xiaohongshu account. <br>
Mitigation: Keep state.json private, delete it when session reuse is no longer needed, and run the skill in an isolated environment. <br>
Risk: The skill can publish user-provided title, caption, and media content to a live account. <br>
Mitigation: Review the title, caption, and media paths before running the posting command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/widebluesky/xiaohongshu-auto-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/widebluesky) <br>
- [Xiaohongshu Creator Studio login](https://creator.xiaohongshu.com/login) <br>
- [Xiaohongshu Creator Studio publish page](https://creator.xiaohongshu.com/publish/publish) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local media file paths and a saved Playwright browser session.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
