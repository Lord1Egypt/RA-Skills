## Description: <br>
Reads WeChat Official Account article links through a local WeWe RSS REST API and returns article text for reading, summarization, and subscription lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to retrieve plain-text content from WeChat Official Account article links, query subscribed accounts, and subscribe new accounts from article URLs through a local WeWe RSS deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose WeChat Read login QR codes or confirmation URLs by sending them to a shared Feishu group. <br>
Mitigation: Send login material only to an approved private channel, get explicit user approval before login, and treat QR codes and confirmation URLs as sensitive temporary credentials. <br>
Risk: The included AUTH_CODE and localhost services could be misused if the WeWe RSS deployment is not controlled. <br>
Mitigation: Use only a trusted local WeWe RSS deployment, rotate or replace the AUTH_CODE before use, and keep the REST API bound to localhost or another controlled network boundary. <br>
Risk: The skill can prompt an agent to start Docker services or manage account login state without clear user control. <br>
Mitigation: Require explicit approval before running Docker commands, starting services, refreshing subscriptions, or changing account login state. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/axelhu/wewe-rss-reader) <br>
- [Deployment guide](artifact/references/deployment.md) <br>
- [WeWe RSS fork referenced by deployment guide](https://github.com/AxelHu/wewe-rss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with REST API examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Article text retrieval is capped at the first 15000 characters according to the skill instructions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
