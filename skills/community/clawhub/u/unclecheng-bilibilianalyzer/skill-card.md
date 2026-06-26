## Description: <br>
Analyzes Bilibili video comments and danmaku by collecting public interaction data, extracting sentiment and keywords, and generating a structured Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unclecheng-li](https://clawhub.ai/user/unclecheng-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content reviewers use this skill to summarize audience response on Bilibili videos from comments and danmaku. It helps produce sentiment, keyword, interaction, and time-distribution analysis in a Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install Python dependencies or use setup helper scripts. <br>
Mitigation: Run it in a virtual environment and review dependency lists before installation. <br>
Risk: The skill may use Bilibili session cookies and save fetched media or comment data locally. <br>
Mitigation: Avoid primary session cookies, keep credential persistence off unless needed, and handle generated data according to local data policies. <br>
Risk: Bilibili automation and API access can be affected by platform rate limits or access controls. <br>
Mitigation: Throttle requests, use only authorized access, and review output before relying on conclusions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unclecheng-li/unclecheng-bilibilianalyzer) <br>
- [Bilibili video information API](https://api.bilibili.com/x/web-interface/view?bvid={bvid}) <br>
- [Bilibili danmaku API](https://api.bilibili.com/x/v1/dm/list.so?oid={cid}) <br>
- [Bilibili comment API](https://api.bilibili.com/x/v2/reply/main?next={page}&type=1&oid={bvid}&mode=3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sentiment summaries, keyword tables, interaction metrics, danmaku timing distribution, and top-comment excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _skillhub_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
