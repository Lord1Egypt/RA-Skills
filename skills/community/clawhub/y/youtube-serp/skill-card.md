## Description: <br>
Search YouTube videos, channels, rankings, and trends through AIsa for YouTube research, competitor scouting, content discovery, video discovery, and SERP-style analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, marketers, and research agents use this skill to search public YouTube results, identify top-ranking videos, review competitor channels, and scan trends while staying grounded in returned API results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AISA_API_KEY and sends YouTube research queries to AIsa. <br>
Mitigation: Use a scoped or revocable key when available, avoid unrelated sensitive data in search terms, and rotate the key if exposure is suspected. <br>
Risk: Returned YouTube titles, URLs, and metrics can be incomplete, stale, or absent. <br>
Mitigation: Ground summaries in returned results, avoid inventing missing fields, and state clearly when the upstream service returns no results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/youtube-serp) <br>
- [Publisher profile](https://clawhub.ai/user/bibaofeng) <br>
- [AIsa API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends YouTube search queries to AIsa.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
