## Description: <br>
A Windows-native Xiaohongshu automation skill that uses Node.js and Playwright to search posts, inspect post details, publish image and text notes, and generate topic reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ken0521](https://clawhub.ai/user/ken0521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators and content creators use this skill to automate Xiaohongshu research, account status checks, post detail collection, Markdown topic reporting, and guided note publishing from a Windows environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse saved Xiaohongshu login sessions and act as the logged-in account. <br>
Mitigation: Use a dedicated account when possible, keep %USERPROFILE%\.xiaohongshu-win off shared or synced machines, and delete the saved cookies and browser profile when the tool is no longer needed. <br>
Risk: Publishing automation can post to a real Xiaohongshu account without a final confirmation step after inputs are collected. <br>
Mitigation: Review title, body, and image paths carefully before running the publish command, and monitor the visible browser window during publishing. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ken0521/xiaohongshu-win) <br>
- [Publisher Profile](https://clawhub.ai/user/ken0521) <br>
- [Xiaohongshu Web](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, JSON cache files, and Markdown topic reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Chromium browser profile and stores session cookies and generated reports under %USERPROFILE%\.xiaohongshu-win.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
