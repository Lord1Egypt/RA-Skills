## Description: <br>
Extract and summarize public QQ app pages, announcements, and group invites without login or message access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize publicly accessible QQ application pages, announcement or share pages, and group invite pages. It is intended for public content only and excludes login, messaging, private data, and access bypass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide QQ credentials, cookies, private messages, account pages, or non-public group content. <br>
Mitigation: Use only public share, app, announcement, or invite links, and do not provide credentials or private QQ content. <br>
Risk: Automated access to dynamic public pages may repeat requests while waiting for rendered content. <br>
Mitigation: Wait for page rendering only as needed, parse public content, and apply rate limits to avoid repeated access. <br>


## Reference(s): <br>
- [QQ homepage](https://im.qq.com/) <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/qq-hot-trend) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and structured text fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should stay limited to public page content and include source links when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
