## Description: <br>
Skill Trend Analysis helps agents query and interpret ClawHub Skills growth trends, rankings, search results, statistics, tags, authors, time ranges, and export data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingdingdemao](https://clawhub.ai/user/dingdingdemao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect ClawHub Skills trend data, compare leaderboards across time windows, search and filter skills, and turn API responses into concise trend conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to a disclosed third-party API endpoint. <br>
Mitigation: Avoid sensitive text in search parameters and use a trusted HTTPS BASE_URL when confidentiality matters. <br>
Risk: Trend conclusions can be misleading if the selected metric, rank limit, or time window is too narrow. <br>
Mitigation: State the metric, date range, rank limit, and sample size with each conclusion, and note when data is insufficient. <br>
Risk: The API rate limit can return HTTP 429 responses during repeated analysis. <br>
Mitigation: Wait at least three seconds before retrying the same endpoint. <br>


## Reference(s): <br>
- [API Endpoints Reference](references/api-endpoints.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dingdingdemao/skill-trend-analysis) <br>
- [ClawHub Skills API](http://skills.easytoken.cc/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise analysis, supporting data, and optional curl or jq command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected JSON fields from read-only API responses; avoids presenting raw JSON without interpretation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
