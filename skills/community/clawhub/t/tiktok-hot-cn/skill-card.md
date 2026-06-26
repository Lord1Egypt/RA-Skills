## Description: <br>
Fetches the top 50 Douyin hot-search entries with heat scores and structured ranking data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangjinghua0127](https://clawhub.ai/user/yangjinghua0127) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users use this skill to retrieve current Douyin hot-search rankings, heat values, labels, and descriptions for reporting or trend-monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Douyin to fetch public hot-search data. <br>
Mitigation: Use it only in environments where outbound requests to Douyin are acceptable. <br>
Risk: The skill saves a local JSON copy of the fetched hot-search results. <br>
Mitigation: Delete workspace/scripts/douyin-hot-clean.json if retained search-result data is not desired. <br>
Risk: The Douyin API endpoint or response shape may change. <br>
Mitigation: Review failures and update the fetch or parsing logic before relying on the output. <br>


## Reference(s): <br>
- [Douyin Hot Search](https://www.douyin.com/hot/) <br>
- [ClawHub skill page](https://clawhub.ai/yangjinghua0127/tiktok-hot-cn) <br>
- [Publisher profile](https://clawhub.ai/user/yangjinghua0127) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [Console text plus a saved JSON file containing ranked Douyin hot-search entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves results to workspace/scripts/douyin-hot-clean.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
