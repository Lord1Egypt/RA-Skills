## Description: <br>
Fetches WeChat public-article content and saves it into a user-provided Feishu Wiki location, asking for the target wiki link before writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gift-is-coding](https://clawhub.ai/user/gift-is-coding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to archive one or more WeChat public-article links into a chosen Feishu Wiki space as structured Docx subpages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can create pages in the wrong Feishu Wiki location if the target link or permissions are incorrect. <br>
Mitigation: Require the user-provided target Wiki link, verify access before writing, and review the destination before bulk imports. <br>
Risk: WeChat article extraction may be incomplete when normal fetching is blocked or the page has not fully loaded. <br>
Mitigation: Try normal web fetching first, use Chrome DOM extraction only when needed, and confirm visible title and body text before writing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gift-is-coding/wechat-to-feishu-wiki) <br>
- [Feishu App Permission Troubleshooting](https://open.feishu.cn/document/faq/trouble-shooting/how-to-add-permissions-to-app?lang=zh-CN&utm_source=chatgpt.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status summaries and created-page links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Feishu Docx wiki subpages when the user provides a writable target wiki link and required bot permissions are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
