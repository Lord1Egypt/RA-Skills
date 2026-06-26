## Description: <br>
Search, read, analyze, and automate Xiaohongshu (小红书) content via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasygu](https://clawhub.ai/user/lucasygu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, creators, marketers, and developers use redbook to research Xiaohongshu topics, analyze creator and note performance, plan content, render Xiaohongshu-style image cards, and perform account actions through a CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can access an active Xiaohongshu browser session through local cookies. <br>
Mitigation: Use a dedicated browser profile when possible, avoid pasting raw cookies into prompts or shell history, and install only when local agent access to the account is acceptable. <br>
Risk: Commands such as post, comment, batch-reply, collect, like, upload, and delete can change the user's Xiaohongshu account state. <br>
Mitigation: Require explicit human approval before account-changing commands and use dry-run or preview modes where available. <br>
Risk: High-volume reads or writes can trigger Xiaohongshu captcha, account throttling, or IP blocks. <br>
Mitigation: Use the documented research loop, keep reads human-paced and non-parallel, apply jittered delays, and stop rather than auto-retry when captcha or throttling appears. <br>
Risk: Install hooks register the tool into agent environments and adjust local package behavior. <br>
Mitigation: Review postinstall behavior before installation and keep the package limited to environments where this integration is intended. <br>


## Reference(s): <br>
- [ClawHub redbook page](https://clawhub.ai/lucasygu/redbook) <br>
- [Publisher profile](https://clawhub.ai/user/lucasygu) <br>
- [Project homepage](https://github.com/lucasygu/redbook) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Content Language Strategy](docs/content-language-strategy.md) <br>
- [Research: Automation, OpenClaw, ClawHub, and Gemini Integration](docs/research-task-1789.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, PNG files] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON or PNG outputs from redbook commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands use the user's browser session cookies; account-changing commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.8.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
