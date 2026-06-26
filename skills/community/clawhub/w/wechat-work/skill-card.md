## Description: <br>
Extract and summarize publicly accessible WeChat Work pages, including announcements, app information, and group invitations, without internal API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and analysts use this skill to summarize publicly accessible WeChat Work announcements, application pages, and group invitation pages. It extracts practical fields such as title, author, update time, content excerpts, app details, links, and invitation-page terms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill could be misapplied to private enterprise chats, authenticated pages, admin consoles, or confidential company material. <br>
Mitigation: Use it only with publicly accessible WeChat Work links and do not provide credentials, internal URLs, or confidential content. <br>
Risk: Repeated access to dynamically rendered public pages can create unnecessary traffic or trigger platform limits. <br>
Mitigation: Throttle visits, avoid repeated requests, and respect platform and enterprise information-security requirements. <br>


## Reference(s): <br>
- [WeChat Work homepage](https://work.weixin.qq.com/) <br>
- [ClawHub skill page](https://clawhub.ai/mike47512/wechat-work) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries and structured field lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credentials, private enterprise data, or internal API access are requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
