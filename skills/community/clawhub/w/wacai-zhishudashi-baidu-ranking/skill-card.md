## Description: <br>
Searches Baidu for the keyword "指数大师," extracts the main result titles in order, formats them as a numbered list, and sends the list to a WeCom robot webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shidengyun](https://clawhub.ai/user/shidengyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers can use this skill to capture a daily Baidu search-results snapshot for the keyword "指数大师" and push the ordered title list to a WeCom channel for ranking observation or reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends scraped titles, or any text passed to the helper script, to an embedded WeCom webhook. <br>
Mitigation: Review the destination before use, prefer overriding the webhook with a user-controlled secret, and use dry-run or preview behavior before sending. <br>
Risk: The artifact includes a hard-coded WeCom webhook secret. <br>
Mitigation: Rotate the exposed key and require webhook configuration through an environment variable or secret store before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shidengyun/wacai-zhishudashi-baidu-ranking) <br>
- [Publisher profile](https://clawhub.ai/user/shidengyun) <br>
- [Baidu search entry point](https://www.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown summary and numbered plain-text title list, with optional shell command execution for WeCom delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends extracted titles to WeCom unless dry-run or reporting-only behavior is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
