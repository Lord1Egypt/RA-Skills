## Description: <br>
Helps agents summarize public WeChat Channels video, topic, account, and ranking pages, including lightweight engagement and channel statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to collect concise summaries of public WeChat Channels topics, account pages, rankings, and video engagement metrics. It is intended for public content only and does not provide login automation, private data access, API reverse engineering, or security bypass guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may be asked to process private, authenticated, or non-public WeChat Channels content. <br>
Mitigation: Use the skill only with public pages and decline requests involving private account data, authentication, or access controls. <br>
Risk: Repeated page visits may conflict with platform rules or rate limits. <br>
Mitigation: Respect WeChat Channels terms, use modest request frequency, and avoid repeated or automated access patterns that could trigger platform controls. <br>
Risk: Dynamic page loading or human verification may make extracted metrics incomplete or stale. <br>
Mitigation: Treat summaries as lightweight analysis, include source links and timestamps when possible, and verify important metrics against the live public page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawkk/wechat-video) <br>
- [WeChat Channels homepage](https://channels.weixin.qq.com/) <br>
- [Publisher profile](https://clawhub.ai/user/clawkk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text summaries with public page links and engagement metrics when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should be limited to public content and may include video titles, account names, publish times, likes, comments, favorites, source links, ranking names, and collection timestamps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
