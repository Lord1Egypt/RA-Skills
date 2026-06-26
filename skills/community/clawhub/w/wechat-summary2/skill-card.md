## Description: <br>
Summarizes WeChat Official Account articles from user-provided mp.weixin.qq.com links and can fall back to a Python fetch script when WebFetch cannot retrieve the content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mick2458pan](https://clawhub.ai/user/mick2458pan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and summarize WeChat Official Account articles. It is useful when a user provides a WeChat article link and wants a concise Chinese summary, key points, data, conclusions, time-sensitive information, or action suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make an outbound request to a user-provided article URL, including through the Python fallback script. <br>
Mitigation: Use only public, non-sensitive article URLs and avoid private, internal, or sensitive links. <br>
Risk: WeChat validation pages or page structure changes can prevent complete article extraction. <br>
Mitigation: Tell the user when retrieval is incomplete or fails, then ask them to check the link or paste the article text directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mick2458pan/wechat-summary2) <br>
- [Publisher profile](https://clawhub.ai/user/mick2458pan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Chinese plain text; long summaries may use concise bullet lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make outbound requests to user-provided URLs and may run the included Python fetch script when WebFetch fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
