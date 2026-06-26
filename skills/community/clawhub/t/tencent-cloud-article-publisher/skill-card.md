## Description: <br>
Publishes Markdown or plain text articles to Tencent Cloud Developer Community by converting content to HTML and calling the article publishing API with a user-provided session cookie. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanminjie](https://clawhub.ai/user/seanminjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content publishers use this skill to publish prepared articles to Tencent Cloud Developer Community without opening a browser. The user provides the title, body, and Tencent Cloud session cookie, and the skill returns publishing status and the article link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a live Tencent Cloud session cookie with access equivalent to the logged-in user. <br>
Mitigation: Provide cookies only for the publishing session, avoid placing them in command history or chat logs, and log out or rotate the session if exposure is possible. <br>
Risk: The skill can immediately publish content under the user's Tencent Cloud account with weak safeguards. <br>
Mitigation: Review the exact title, body, account, and destination before invoking the publishing command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanminjie/tencent-cloud-article-publisher) <br>
- [Tencent Cloud Developer Community](https://cloud.tencent.com/developer) <br>
- [Tencent Cloud article publishing endpoint](https://cloud.tencent.com/developer/api/article/addArticle) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and publishing status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the Tencent Cloud article URL and article ID when publishing succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
