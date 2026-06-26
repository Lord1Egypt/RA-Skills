## Description: <br>
Find fresh, viral Xiaohongshu videos by niche, apply search filters for type, date, and popularity, and extract full video URLs with valid tokens for downstream use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travislius](https://clawhub.ai/user/travislius) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and automation operators use this skill to find recent Xiaohongshu video posts in a target niche, evaluate basic popularity and visual criteria, and copy usable video or share URLs for repurposing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a logged-in Xiaohongshu browser session, so search results may be blocked if the session expires. <br>
Mitigation: Confirm the managed browser is logged in before use and re-scan the login QR code when search results are unavailable. <br>
Risk: Copied Xiaohongshu URLs can contain tokenized xsec_token values that expire and may expose session-specific access context if shared publicly. <br>
Mitigation: Use fresh URLs for downstream tools and avoid sharing tokenized links publicly. <br>
Risk: Using the Xiaohongshu share button can replace the current clipboard contents. <br>
Mitigation: Check clipboard contents after sharing and preserve any important clipboard data before clicking the share button. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travislius/xhs-video-finder) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with browser action commands and copied URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Xiaohongshu browser session; copied URLs may include expiring xsec_token values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
