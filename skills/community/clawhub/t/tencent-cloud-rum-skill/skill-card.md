## Description: <br>
Query Tencent Cloud RUM data, analyze Web performance (LCP/FCP/WebVitals), troubleshoot JS/Promise errors, analyze API latency & error rates, diagnose slow static resource loading, and view PV/UV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lauraytwu-create](https://clawhub.ai/user/lauraytwu-create) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query Tencent Cloud RUM metrics and logs, diagnose frontend performance and error issues, and produce actionable analysis reports. It supports Web RUM workflows including page performance, API stability, static-resource loading, PV/UV review, and RUM-APM correlation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Tencent Cloud credentials. <br>
Mitigation: Use a dedicated least-privilege Tencent Cloud key, keep generated mcporter configuration private, and rotate credentials if exposure is suspected. <br>
Risk: The skill can query detailed RUM telemetry, including user-related logs. <br>
Mitigation: Use it only for authorized applications and avoid user-targeted log searches unless they are necessary and approved. <br>
Risk: The skill connects an agent to the disclosed Tencent Cloud RUM MCP endpoint. <br>
Mitigation: Install it only when the agent is intended to query Tencent Cloud RUM data through that endpoint. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/lauraytwu-create/tencent-cloud-rum-skill) <br>
- [Tencent Cloud RUM Console](https://console.tencentcloud.com/rum) <br>
- [Tencent Cloud API Key Management](https://console.tencentcloud.com/cam/capi) <br>
- [Tencent Cloud RUM Product Overview](https://www.tencentcloud.com/document/product/1131/44486) <br>
- [Tencent Cloud RUM Application Integration Guide](https://www.tencentcloud.com/zh/document/product/1131/44496) <br>
- [Tencent Cloud RUM Web SDK Connection Guide](https://www.tencentcloud.com/document/product/1131/44517) <br>
- [Tencent Cloud RUM Getting Started](https://www.tencentcloud.com/document/product/1131/44493) <br>
- [Tencent Cloud RUM MCP Tool Parameter Reference](references/rum_tools_docs.md) <br>
- [RUM-WEB Problem Analysis Workflows](references/common_queries.md) <br>
- [APM Correlation Analysis Guide](references/apm_analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis and guidance with optional shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should attribute queried data to Tencent Cloud RUM MCP and avoid exposing SecretId, SecretKey, or user telemetry beyond the authorized analysis need.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
