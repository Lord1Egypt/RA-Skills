## Description: <br>
通过云端连接器优先执行浏览器插件数据采集，也可回退到本地连接器；适用于抖音、TikTok、小红书、Amazon、Bilibili 的采集任务，以及 web-collection 首次上手、配置、付费使用说明和 QA 排障。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiming1001](https://clawhub.ai/user/yiming1001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to configure and run browser-extension web collection workflows for Douyin, TikTok, Xiaohongshu, Amazon, and Bilibili. It routes first-time setup, paid access, troubleshooting, local connector, cloud connector, export, and recovery flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses cloud connector tokens and may persist sensitive connector credentials. <br>
Mitigation: Treat cloud tokens as secrets and prefer environment variables or a secret store over saved preferences. <br>
Risk: The skill can interact with local connector endpoints and supports local command execution paths. <br>
Mitigation: Use the skill only with trusted connectors, avoid custom base URLs unless you control them, and do not pass --bridge-cmd values from untrusted sources. <br>
Risk: The security scan verdict is suspicious because endpoint validation and disclosure may be insufficient for powerful collection workflows. <br>
Mitigation: Review the skill and connector behavior before installation or deployment, especially for cloud dispatch and export flows. <br>


## Reference(s): <br>
- [Web Collection Skill Page](https://clawhub.ai/yiming1001/web-collection) <br>
- [Web Collection Learning Guide](references/learning-guide.md) <br>
- [Quick Start and UI Operation Guide](https://vcn5grhrq8y0.feishu.cn/wiki/MoXrwwUN7iiUFkk8eWycs9JqntA?from=from_copylink) <br>
- [QA and Troubleshooting Guide](https://vcn5grhrq8y0.feishu.cn/wiki/F83hw2w6Xi7EOFkIScrccrQYnnd?from=from_copylink) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise collection status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include collection mode, command status, export status, collected count, bitable table links, CSV export confirmation, and short analysis.] <br>

## Skill Version(s): <br>
1.2.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
