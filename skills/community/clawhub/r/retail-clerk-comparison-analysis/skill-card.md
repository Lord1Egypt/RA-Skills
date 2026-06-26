## Description: <br>
导购对比分析工具，基于 clerk-performance-analysis 扩展导购业绩的时间对比、横向排名、标杆差距和绩效对标分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail store managers and operations teams use this skill to compare sales clerk performance across time periods, rank multiple clerks, identify benchmark gaps, and prepare coaching or performance-review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive employee performance data and may be used to generate reports for store management. <br>
Mitigation: Use only approved employee-performance data and review generated findings before sharing or using them for coaching or evaluation. <br>
Risk: The artifact describes sending morning-meeting reports to enterprise WeChat without recipient safeguards. <br>
Mitigation: Verify the exact recipients and authorization path before sending any report outside the analysis environment. <br>
Risk: The skill imports a dependency from ~/.openclaw/skills/clerk-performance-analysis, so local skill files influence the analysis behavior. <br>
Mitigation: Install only trusted dependencies and avoid running it where unrelated or untrusted files under ~/.openclaw/skills could be modified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-clerk-comparison-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Python dictionaries and printed Chinese performance reports with rankings, findings, recommendations, and action plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on clerk-performance-analysis data and the requested store, clerk names, date ranges, and comparison focus.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
