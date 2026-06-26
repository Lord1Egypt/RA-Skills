## Description: <br>
Summarizes WeChat Official Account articles from mp.weixin.qq.com links and returns concise Chinese summaries of the article's core content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mick2458pan](https://clawhub.ai/user/mick2458pan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to quickly understand WeChat Official Account articles from mp.weixin.qq.com links without manually reading the full article. It is optimized for concise Chinese summaries that preserve key data, conclusions, timelines, and action suggestions when present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch and process user-provided WeChat article URLs, including links that contain private or sensitive content. <br>
Mitigation: Use explicit public article URLs and avoid submitting private, confidential, or sensitive links. <br>
Risk: WeChat anti-bot checks or page structure changes can prevent complete article extraction. <br>
Mitigation: If fetching fails or content is incomplete, verify the link or paste the article text directly for summarization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mick2458pan/wechat-mick) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown in Chinese, with fallback shell command guidance when article fetching fails.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May extract title, account, author, and article body before summarization.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
