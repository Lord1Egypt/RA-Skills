## Description:

Queries Tencent Cloud RUM data to analyze web performance, JavaScript and Promise errors, API latency and error rates, static resource loading, PV/UV, and RUM-APM correlation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lauraytwu-create](https://clawhub.ai/user/lauraytwu-create)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend performance engineers use this skill to query Tencent Cloud RUM metrics and logs, then produce performance, exception, API stability, resource loading, and APM correlation analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup stores reusable Tencent Cloud SecretId and SecretKey values in the user mcporter configuration.

Mitigation: Use a dedicated least-privilege Tencent Cloud key limited to required RUM/APM read access, restrict access to the mcporter config, and rotate the key if the file may have been exposed.

Risk: The setup script can globally install the mcporter npm package.

Mitigation: Review the setup script and install or pin mcporter in a controlled environment before running it on shared or production systems.

## Reference(s):

- [Tencent Cloud RUM Console](https://console.tencentcloud.com/rum)
- [Tencent Cloud RUM Product Overview](https://www.tencentcloud.com/document/product/1131/44486)
- [Tencent Cloud RUM Getting Started](https://www.tencentcloud.com/document/product/1131/44493)
- [Tencent Cloud RUM Application Integration Guide](https://www.tencentcloud.com/zh/document/product/1131/44496)
- [Tencent Cloud RUM Web SDK Connection Guide](https://www.tencentcloud.com/document/product/1131/44517)
- [Tencent Cloud API Key Management](https://console.tencentcloud.com/cam/capi)
- [Tencent Cloud RUM MCP Endpoint](https://app.rumt-zh.com/sse)
- [RUM Tool Parameter Reference](artifact/references/rum_tools_docs.md)
- [RUM-WEB Problem Analysis Workflows](artifact/references/common_queries.md)
- [APM Correlation Analysis Guide](artifact/references/apm_analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis reports with query recommendations and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Tencent Cloud RUM MCP data and should attribute Tencent Cloud RUM MCP as the data source.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
