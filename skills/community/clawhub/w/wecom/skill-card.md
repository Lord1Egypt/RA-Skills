## Description: <br>
Send messages to WeCom via webhooks using MCP protocol for Claude Code, Claude Desktop, and other MCP clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this MCP server to let an agent send text and markdown updates into a configured WeCom group chat through an incoming webhook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured webhook URL can authorize posting into a WeCom chat if exposed. <br>
Mitigation: Keep WECOM_WEBHOOK_URL secret and configure it only in trusted runtime environments. <br>
Risk: Messages are posted to the configured WeCom destination and may disclose sensitive content. <br>
Mitigation: Confirm the destination group before use and avoid sending secrets or confidential data unless that disclosure is intended. <br>
Risk: Installing from unreviewed package sources can introduce supply-chain risk. <br>
Mitigation: Prefer reviewed local files or verified npm provenance for installation. <br>


## Reference(s): <br>
- [ClawHub Wecom Release Page](https://clawhub.ai/qidu/wecom) <br>
- [WeCom Group Chat Message Receiving and Sending](https://developer.work.weixin.qq.com/document/path/99110) <br>
- [WeCom Apps Download](https://work.weixin.qq.com/#indexDownload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls] <br>
**Output Format:** [MCP tool responses and WeCom webhook payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WECOM_WEBHOOK_URL; optional WECOM_TIMEOUT_MS controls request timeout.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
