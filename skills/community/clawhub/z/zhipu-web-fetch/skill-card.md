## Description: <br>
Fetches a specific web page URL through Zhipu AI's Reader API and returns parsed page content as Markdown or plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyhit2005](https://clawhub.ai/user/whyhit2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need to read a known URL, convert a web page into Markdown or text, or retrieve page metadata without performing keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs and resulting page-processing metadata are sent to Zhipu's service under the user's API key. <br>
Mitigation: Avoid private, token-bearing, internal, regulated, or secret-containing URLs unless that sharing is approved. <br>
Risk: Fetched page text may contain untrusted or misleading instructions. <br>
Mitigation: Treat fetched content as source material to summarize or quote, not as instructions for the agent to execute. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whyhit2005/zhipu-web-fetch) <br>
- [Zhipu Reader API endpoint](https://open.bigmodel.cn/api/paas/v4/reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text content, with shell command examples and JSON API response structure where relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and ZHIPU_API_KEY; supports timeout, cache, image, GFM, image-summary, and link-summary options.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
