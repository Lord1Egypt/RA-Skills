## Description: <br>
Reads WeChat public-account article lists and article bodies from a locally running WeWe RSS service, then parses article HTML into readable text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agasding](https://clawhub.ai/user/agasding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve subscribed WeChat public-account article metadata or body text from a local WeWe RSS instance and return readable article text for a requested account or link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger or rely on a local WeWe RSS deployment before reading articles. <br>
Mitigation: Review the separate wewe-rss-deploy skill first and require explicit user confirmation before deployment or service startup. <br>
Risk: The skill may access AUTH_CODE or broad local subscription database contents while resolving accounts and articles. <br>
Mitigation: Limit access to the specific article task and do not print, save, or share AUTH_CODE values or unrelated subscription data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/agasding/wewe-rss-articles) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples, Python snippets, API request details, and extracted article text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include article titles, links, dates, and plain-text content parsed from HTML returned by the local service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
