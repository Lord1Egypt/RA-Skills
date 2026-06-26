## Description: <br>
小红书数据分析 is a demo skill for searching Xiaohongshu notes, analyzing creator and trend metrics, comparing accounts or notes, and generating reports. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[legou20221023](https://clawhub.ai/user/legou20221023) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to prototype Xiaohongshu note search, creator analysis, trend tracking, competitor comparison, and report generation workflows. Reports should not be used for business decisions until a trusted live data source is configured and validated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may be based on sample data or an untrusted data source. <br>
Mitigation: Treat outputs as demonstrations until a trusted live data source is implemented, clearly label sample outputs, and cross-check results before making decisions. <br>
Risk: API keys or cookies may be needed for real Xiaohongshu data access. <br>
Mitigation: Keep credentials out of shared files, prefer least-privilege credentials, and manage secrets through environment variables or a secure secret store. <br>
Risk: Data collection can violate platform limits or privacy expectations if used carelessly. <br>
Mitigation: Respect platform rules and rate limits, avoid using proxies to bypass restrictions, and do not collect or redistribute private personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/legou20221023/xhs-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown, Configuration] <br>
**Output Format:** [Markdown instructions with bash commands; scripts emit JSON, CSV, or Markdown report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sample data is returned unless credentials or a trusted live data source are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
