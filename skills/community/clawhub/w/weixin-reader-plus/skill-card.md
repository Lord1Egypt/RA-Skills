## Description: <br>
Reads mp.weixin.qq.com WeChat Official Account article links and extracts the article title, account name, and body text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnwarden](https://clawhub.ai/user/cnwarden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users use this skill when they provide a WeChat Official Account article URL and ask the agent to read or inspect the article content. It returns the article metadata and body text so the agent can work from the retrieved text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided article URLs may be inaccessible, require verification, or fail parsing. <br>
Mitigation: Treat access and parsing failures as expected outcomes and ask the user for alternate accessible content when needed. <br>
Risk: The skill fetches external web content from a user-provided URL. <br>
Mitigation: Confirm the target is an mp.weixin.qq.com article link before execution and avoid using private or credential-bearing URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnwarden/weixin-reader-plus) <br>
- [Publisher profile](https://clawhub.ai/user/cnwarden) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output with article title, account name, and body text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return an error message when an article requires verification or cannot be parsed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
