## Description: <br>
Searches Qingbo Open Platform for online articles by keyword, date range, media type, and sentiment, then returns article links, publication details, or counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangqiang327](https://clawhub.ai/user/zhangqiang327) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to query Qingbo Open Platform for article search and media monitoring workflows. It helps retrieve matching article titles, URLs, publication times, media sources, sentiment labels, and aggregate counts from natural-language search requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and related parameters are sent to Qingbo's external API. <br>
Mitigation: Use the skill only for queries appropriate to Qingbo Open Platform and avoid sensitive queries on untrusted networks. <br>
Risk: Qingbo API credentials are required in config.json. <br>
Mitigation: Use only your own Qingbo credentials, keep config.json out of source control and shared archives, and rotate credentials if exposed. <br>
Risk: Searches may consume Qingbo account quota or points. <br>
Mitigation: Set expectations for query volume and monitor Qingbo account usage when deploying the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangqiang327/qingbo-search) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text search summaries and article lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include article title, URL, publication time, media type, sentiment, or total result count.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
