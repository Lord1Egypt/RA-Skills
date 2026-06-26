## Description: <br>
基于 Python 和 Playwright 的 OpenClaw skill，可按关键词抓取小红书笔记并将结果推送到飞书群。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xie07418](https://clawhub.ai/user/xie07418) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill in OpenClaw and Feishu workflows to search Xiaohongshu by keyword, collect note metadata, and post a concise result summary to a configured Feishu group. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports exposed credentials and session data, including a bundled cookie and Feishu credentials. <br>
Mitigation: Remove bundled cookies, rotate exposed Feishu credentials, configure a private destination, and store secrets outside the skill artifact before installation. <br>
Risk: The security summary reports that chat input can reach shell execution and account-login flows too broadly. <br>
Mitigation: Replace exec-style command invocation with argument-safe process APIs, validate the keyword input, and restrict login flows to an isolated runtime. <br>
Risk: Saved browser profiles, cookie files, and QR login screenshots can function as account credentials. <br>
Mitigation: Run the skill in an isolated environment, restrict filesystem permissions, and treat those files as sensitive credentials. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/xie07418/xhs-crawler-xie) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Usage documentation](artifact/使用文档.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Text responses plus Feishu card-style markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts up to five Xiaohongshu note summaries to a configured Feishu chat and may emit status or error text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
