## Description: <br>
Search TikTok videos and run product, trend, competitor, and content insights through Gecho Bridge MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gecho-ai](https://clawhub.ai/user/gecho-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search TikTok, collect structured video metadata, and start asynchronous product, trend, or competitor insight jobs through Gecho Bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TikTok searches and insight jobs use Gecho Bridge and a logged-in Chrome/TikTok browser session. <br>
Mitigation: Install and use the skill only when you are comfortable connecting Gecho Bridge and the Gecho Chrome extension to that browser session. <br>
Risk: Search and insight outputs may be saved locally as JSON files containing research data. <br>
Mitigation: Choose a save directory deliberately when possible and delete retained result files when they are no longer needed. <br>
Risk: The skill depends on the official Gecho MCP tools and can fail if the MCP server, extension login, or TikTok session is unavailable. <br>
Mitigation: Configure the official Gecho Bridge MCP server, keep the extension and TikTok web logged in, and report exact tool failures instead of substituting unofficial scraping methods. <br>


## Reference(s): <br>
- [TikTok Search on ClawHub](https://clawhub.ai/gecho-ai/tiktok-search) <br>
- [Gecho Publisher Profile](https://clawhub.ai/user/gecho-ai) <br>
- [Gecho Website](https://gecho.ai/) <br>
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md) <br>
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb) <br>
- [OpenClaw Setup Video](https://www.youtube.com/watch?v=ggwY9hISHcQ) <br>
- [Hermes Setup Video](https://www.youtube.com/watch?v=zHKnuWnxt_c) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks and JSON-oriented TikTok result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a jobId for asynchronous insight jobs; Gecho may save search or insight results as local JSON files.] <br>

## Skill Version(s): <br>
1.1.24 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
