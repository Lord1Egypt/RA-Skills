## Description: <br>
WeChat Article Fetcher extracts readable content from mp.weixin.qq.com article links by sending the link to a third-party conversion service and returning article text, commonly as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HLGate](https://clawhub.ai/user/HLGate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user provides a WeChat public-account article link and wants readable article content, a summary, or answers grounded in that article. It is intended for public or otherwise safe-to-share article URLs because the URL is forwarded to an external conversion service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat article links are sent to down.mptext.top for conversion, which may expose private, access-controlled, tokenized, or sensitive URLs. <br>
Mitigation: Ask for confirmation before fetching and avoid using the skill with private, access-controlled, tokenized, or sensitive article URLs. <br>
Risk: Article fetching may fail or return incomplete content because some articles can have word limits, anti-scraping controls, or time-limited image links. <br>
Mitigation: Treat fetched content as best-effort, retry with text format when Markdown fails, and disclose fetch failures or missing media to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HLGate/wechat-article-fetcher) <br>
- [Publisher profile](https://clawhub.ai/user/HLGate) <br>
- [WeChat article conversion endpoint](https://down.mptext.top/api/public/v1/download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text extracted from a WeChat article, with optional HTML or JSON depending on the requested conversion format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required. Article links are forwarded to down.mptext.top, and some articles or image links may be incomplete, restricted, or time-limited.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
