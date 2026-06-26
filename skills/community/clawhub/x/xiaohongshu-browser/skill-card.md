## Description: <br>
Browse Xiaohongshu (小红书) and take screenshots of posts. Supports keyword search, post modal screenshots, and returns post links. Requires prior manual login. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[besty0121](https://clawhub.ai/user/besty0121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate Xiaohongshu keyword searches, capture post preview screenshots, and collect post links after a manual account login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable Xiaohongshu login and browser session data are stored locally under ~/.openclaw/xhs_data and ~/.openclaw/xhs_auth.json. <br>
Mitigation: Run the skill only on trusted machines, restrict access to those files, and delete them when the browser session is no longer needed. <br>
Risk: Automated browsing and repeated searches may trigger Xiaohongshu anti-abuse controls or account/IP restrictions. <br>
Mitigation: Use conservative search volumes, stop when blocks appear, and follow the service's applicable terms and account policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/besty0121/xiaohongshu-browser) <br>
- [Xiaohongshu website](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files, JSON] <br>
**Output Format:** [Markdown instructions with shell commands; scripts produce PNG screenshots and JSON result records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and Playwright; output screenshots are written under the skill output directory] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
