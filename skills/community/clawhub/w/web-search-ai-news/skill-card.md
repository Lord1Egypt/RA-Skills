## Description: <br>
Fetches recent AI industry news and sends the results through a configured email account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stringtwb1220](https://clawhub.ai/user/stringtwb1220) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for current AI industry news from selected technology news sources and receive the update by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically email fetched AI news through a local SMTP configuration. <br>
Mitigation: Use a dedicated low-privilege sender account, verify the recipient, and require explicit confirmation before any email is sent. <br>
Risk: Fetched news content may be incomplete, outdated, or misleading. <br>
Mitigation: Review the generated update and source links before relying on or forwarding the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stringtwb1220/web-search-ai-news) <br>
- [Configured news source: The Paper](https://www.thepaper.cn/) <br>
- [Configured news source: Huxiu](https://www.huxiu.com/) <br>
- [Configured news source: TMTPost](https://www.tmtpost.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text news update sent through the agent response and configured email flow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches from configured news URLs with a 10000 character cap before post-processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
