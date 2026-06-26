## Description: <br>
Queries UApp (友盟+) application outlier reports, yesterday anomalies, and intelligent inspection summaries for app monitoring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operations teams use this skill to fetch UApp anomaly reports, identify applications with yesterday outliers, and summarize intelligent inspection findings for apps tied to their UApp credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads UApp credentials from direct input, local configuration, or environment variables. <br>
Mitigation: Use limited-scope UApp credentials and keep umeng-config.json out of version control. <br>
Risk: Usage telemetry is enabled by default and sends app identifiers and query context through umeng-cli. <br>
Mitigation: Verify the installed umeng-cli binary and set UMENG_ENABLE_STATS=false when telemetry is not desired. <br>
Risk: The skill sends app identifiers and query parameters to UApp API endpoints. <br>
Mitigation: Run it only for accounts and applications where sharing that context with UApp is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squall0925/uapp-outlier) <br>
- [Publisher profile](https://clawhub.ai/user/squall0925) <br>
- [UApp outlier report endpoint](https://mobile.umeng.com/ht/api/v3/ai/getOutlierPoints) <br>
- [UApp yesterday outliers endpoint](https://mobile.umeng.com/ht/api/v3/ai/getYesterdayOutliers) <br>
- [UApp intelligent inspection endpoint](https://mobile.umeng.com/ht/api/v3/claw/meta/aiEventSummary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or terminal text summarizing UApp API responses, anomaly status, dates, error codes, and report URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include UApp share URLs and app identifiers returned by the queried account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
