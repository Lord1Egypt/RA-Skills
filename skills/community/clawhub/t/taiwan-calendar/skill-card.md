## Description: <br>
Taiwan calendar query for accurate working day and holiday information. Use when user asks about Taiwan dates, working days, holidays, make-up workdays, or needs date calculations. Solves Claude's knowledge cutoff issues with Taiwan's administrative calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pigfoot](https://clawhub.ai/user/pigfoot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to answer Taiwan-specific date, holiday, working-day, make-up workday, and deadline calculation questions with current public calendar data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public calendar data from the internet, so answers can fail or become stale when upstream APIs or network access are unavailable. <br>
Mitigation: Use the built-in fallback data source and cache behavior, and surface API or cache warnings to users when current data cannot be fetched. <br>
Risk: The skill runs a Python script and installs declared script dependencies through uv as needed. <br>
Mitigation: Review the script and dependency declarations before deployment, and run it in an environment where outbound network access and temporary-file caching are acceptable. <br>


## Reference(s): <br>
- [Taiwan Calendar Plugin on ClawHub](https://clawhub.ai/pigfoot/taiwan-calendar) <br>
- [Taiwan government calendar data via jsDelivr](https://cdn.jsdelivr.net/gh/ruyut/TaiwanCalendar/data/{year}.json) <br>
- [New Taipei City Open Data fallback](https://data.ntpc.gov.tw/api/datasets/308DCD75-6434-45BC-A95F-584DA4FED251/json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are Taiwan-timezone calendar answers, typically in Traditional Chinese, backed by live public data with a short local cache.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
