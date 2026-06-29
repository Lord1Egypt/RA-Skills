## Description: <br>
Web Collection helps an agent run browser-extension data collection for Douyin, TikTok, Xiaohongshu, Amazon, and Bilibili, using a cloud connector first and a local connector as fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiming1001](https://clawhub.ai/user/yiming1001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to configure a browser collection connector, collect data from supported consumer platforms, and export results to Feishu Bitable or CSV. It also guides first-time setup, connector authorization, re-export recovery, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may reuse stored connector or App credentials and bearer tokens while dispatching browser collection tasks. <br>
Mitigation: Install only when the publisher and connector service are trusted, verify the cloud base URL and login confirmation link before authorization, and treat connector tokens and Bitable authorization codes as sensitive secrets. <br>
Risk: Shell helper paths can start or control connector processes, and an untrusted bridge command could run with broad local authority. <br>
Mitigation: Avoid untrusted --bridge-cmd values, review the command before execution, and prefer the bundled scripts and documented connector authorization flow. <br>
Risk: Browser-based collection and export depend on connector state, platform-specific filters, and Bitable table compatibility. <br>
Mitigation: Run the preflight checks, preserve platform-specific filter shapes, confirm export settings, and use the cached-task re-export path when collection succeeds but Bitable export fails. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yiming1001/skills/web-collection) <br>
- [Quick Start and UI Guide](https://vcn5grhrq8y0.feishu.cn/wiki/MoXrwwUN7iiUFkk8eWycs9JqntA?from=from_copylink) <br>
- [Demo Scenarios](https://vcn5grhrq8y0.feishu.cn/wiki/GO11wlXkriSwNakXrt2ck0GanEe) <br>
- [Browser Extension and Connector Installation Guide](https://vcn5grhrq8y0.feishu.cn/wiki/R6f2w6o7ci1db1kYLK4cgJIYnWh) <br>
- [Bitable Configuration and Connector Authorization Guide](https://vcn5grhrq8y0.feishu.cn/wiki/EAtJw2irFiDvMpkZXb4cBjYonNg) <br>
- [Bitable Template](https://vcn5grhrq8y0.feishu.cn/base/UKQsbVHpMac293s0cnFc1hq1nDd?table=tblTXM4lclXM6Jzr&view=vew8OdcKHw) <br>
- [QA and Troubleshooting Guide](https://vcn5grhrq8y0.feishu.cn/wiki/F83hw2w6Xi7EOFkIScrccrQYnnd?from=from_copylink) <br>
- [Learning Guide](references/learning-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and connector status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu Bitable links, CSV export status, collection counts, and brief troubleshooting analysis.] <br>

## Skill Version(s): <br>
1.2.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
