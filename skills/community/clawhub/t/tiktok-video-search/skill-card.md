## Description: <br>
Searches TikTok videos by keyword through Gecho Bridge MCP and returns structured video metadata, creators, engagement metrics, and video links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gecho-ai](https://clawhub.ai/user/gecho-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and social media researchers use this skill to route TikTok keyword searches through Gecho Bridge MCP, collect video examples and creator metadata, and summarize the most useful results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TikTok search results may be saved as local JSON files on the user's machine. <br>
Mitigation: Use a non-shared save directory, avoid sensitive workspaces, and delete exported JSON files when they are no longer needed. <br>
Risk: Searches depend on a configured Gecho Bridge MCP server, the Gecho Chrome extension, and an active logged-in TikTok browser session. <br>
Mitigation: Complete the documented setup first, keep the extension and TikTok session logged in, and stop with the reported error if setup, CAPTCHA, login, timeout, or save failures occur. <br>
Risk: Multiple simultaneous browser-driven scraping jobs can interfere with the live browser tab and extension session. <br>
Mitigation: Run only one Gecho TikTok search job in a conversational turn and do not run Gecho scraping jobs in parallel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gecho-ai/tiktok-video-search) <br>
- [Gecho website](https://gecho.ai/) <br>
- [Gecho Bridge GitHub repository](https://github.com/gecho-ai/gecho-bridge) <br>
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md) <br>
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb) <br>
- [OpenClaw setup video](https://www.youtube.com/watch?v=ggwY9hISHcQ) <br>
- [Hermes setup video](https://www.youtube.com/watch?v=zHKnuWnxt_c) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown responses with setup commands and summarized TikTok result metadata; successful tool calls may return JSON arrays and local file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful search responses summarize only the top 3 to 5 results and avoid pasting full raw JSON.] <br>

## Skill Version(s): <br>
1.1.24 (source: evidence release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
