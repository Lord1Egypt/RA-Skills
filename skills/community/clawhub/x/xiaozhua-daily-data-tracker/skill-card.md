## Description: <br>
Tracks daily KPI history for revenue, gross adds, subscribers, product splits, week-over-week changes, and trend warnings in a Markdown memory file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirowangl-ops](https://clawhub.ai/user/mirowangl-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and operators use this skill to append daily business KPI rows, maintain historical tracking, calculate week-over-week movement, and identify sustained performance declines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily revenue and subscriber metrics may be stored in the agent's memory file. <br>
Mitigation: Use the skill only where storing those metrics in memory/powerbi-daily-track.md is acceptable. <br>
Risk: The skill records and analyzes provided values but does not verify the source data. <br>
Mitigation: Validate source metrics separately before relying on the resulting trends or warnings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirowangl-ops/xiaozhua-daily-data-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown table rows with concise trend-analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates memory/powerbi-daily-track.md with daily KPI history when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
