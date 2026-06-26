## Description: <br>
Fetch and format Wenxuecity News rankings from https://www.wenxuecity.com/news/, specifically the two 24-hour lists: hot ranking and discussion ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonyguo2010](https://clawhub.ai/user/tonyguo2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and automation builders use this skill to collect, summarize, monitor, or diff Wenxuecity 24-hour hot and discussion ranking entries for daily digests or downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Wenxuecity when rankings are requested. <br>
Mitigation: Use the default source URL unless you intentionally want the agent to fetch another page. <br>
Risk: The optional output path can create or overwrite a local file. <br>
Mitigation: Choose the --output destination deliberately and review it before running the script in automated workflows. <br>
Risk: Ranking extraction depends on Wenxuecity page structure and may return fewer or missing entries if the site changes. <br>
Mitigation: Validate results against the live source page when ranking completeness matters. <br>


## Reference(s): <br>
- [Wenxuecity News source page](https://www.wenxuecity.com/news/) <br>
- [ClawHub skill page](https://clawhub.ai/tonyguo2010/wenxuecity-news-rankings) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON ranking output, optionally written to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes fetched timestamp, source URL, requested top count, hot_24h and discussion_24h groups, rank, title, URL, and optional image_url.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
