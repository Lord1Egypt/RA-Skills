## Description: <br>
Run async TikTok product, trend, competitor, and content insight jobs through Gecho Bridge MCP, and check existing insight job status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gecho-ai](https://clawhub.ai/user/gecho-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to start TikTok product, trend, competitor, and content insight jobs through Gecho Bridge, then check asynchronous job status and summarize completed results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TikTok insight jobs depend on Gecho Bridge, the Gecho Chrome extension, and data visible in a logged-in TikTok browser session. <br>
Mitigation: Install only if comfortable with Gecho Bridge and its Chrome extension using browser-session data for user-requested research jobs; keep the extension and MCP package under review. <br>
Risk: Insight jobs can fail when MCP tools are unavailable, the extension is offline, TikTok is logged out, a CAPTCHA is present, or the browser tab is blocked. <br>
Mitigation: Confirm the documented setup prerequisites before running jobs and report exact tool errors instead of retrying or inventing results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gecho-ai/tiktok-insight) <br>
- [Gecho Website](https://gecho.ai/) <br>
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md) <br>
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb) <br>
- [OpenClaw Setup Video](https://www.youtube.com/watch?v=ggwY9hISHcQ) <br>
- [Hermes Setup Video](https://www.youtube.com/watch?v=zHKnuWnxt_c) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and job status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a Gecho insight jobId, setup commands, status values, saved result paths, or concise result summaries.] <br>

## Skill Version(s): <br>
1.1.24 (source: artifact/_meta.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
