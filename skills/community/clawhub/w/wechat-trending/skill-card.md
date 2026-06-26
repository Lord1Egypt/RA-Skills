## Description: <br>
Extract and summarize publicly accessible WeChat shared pages including announcements, app information, and group invitation details without login or private data access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to summarize public WeChat announcement pages, app pages, and group invitation pages into titles, authors, update times, summaries, tags, version details, terms notes, and source links. It is intended for public content review and internal analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide private chats, credentials, login-only pages, or requests for account actions outside the skill's intended scope. <br>
Mitigation: Use the skill only with publicly accessible WeChat links, and do not provide private chats, credentials, login-only pages, message-sending requests, or account-management instructions. <br>
Risk: Dynamic public pages may load content asynchronously, which can lead to incomplete extraction if read too early. <br>
Mitigation: Wait for public page rendering to complete before summarizing and keep source links in the output so users can verify important details. <br>


## Reference(s): <br>
- [WeChat](https://weixin.qq.com/) <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/wechat-trending) <br>
- [Publisher profile](https://clawhub.ai/user/CodeKungfu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or concise structured text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries may include source links and extracted public metadata fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
