## Description: <br>
Extract and summarize publicly shared WeChat pages, including announcements, app details, and group invitations, without requiring login or account access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to gather titles, authors, update times, summaries, tags, version details, and links from public WeChat share pages. It is scoped to public announcements, app pages, and group invitation pages, and excludes login, messaging, private content, and permission bypass workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill on private chats, login-required pages, account actions, messaging, or sensitive links could exceed the intended public-page scope. <br>
Mitigation: Use it only with public WeChat share links or public pages, and separately review any agent or browsing tool before handling sensitive links. <br>
Risk: Dynamically loaded public pages may be summarized before all relevant content is available. <br>
Mitigation: Wait for page rendering to complete before extraction and review summaries against the source page for important use cases. <br>
Risk: Repeated access to public pages may create unnecessary traffic or platform policy concerns. <br>
Mitigation: Apply rate limits and avoid repeated visits to the same page. <br>


## Reference(s): <br>
- [WeChat homepage](https://weixin.qq.com/) <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/wechat-hot-trend) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries and structured text fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only guidance for public WeChat pages; no account actions or credential handling.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
