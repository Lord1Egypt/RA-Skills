## Description: <br>
小红书低粉爆款笔记 helps agents find Xiaohongshu posts from accounts with fewer than 5,000 followers and more than 500 likes, then summarize ranking data and viral content patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content operators, brands, MCNs, and content strategy analysts use this skill to monitor low-follower, high-engagement Xiaohongshu notes by category and date, study title and topic patterns, and export findings for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and may read shell profile files to find credentials. <br>
Mitigation: Provide the key explicitly for the current session or through a secret manager, and avoid allowing the skill to scan or edit shell profile files. <br>
Risk: Generated cache, report, and export files may contain retrieved Xiaohongshu data or operational context. <br>
Mitigation: Review generated files after use and remove any outputs that should not be retained or shared. <br>
Risk: The release includes a daily subscription workflow that creates recurring outputs. <br>
Mitigation: Use subscription behavior only after confirming how to pause or cancel it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/xhs-breaking-rankings) <br>
- [API specification](references/api-spec.md) <br>
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown reports with ranking tables and analysis, plus optional JSON cache files and HTML exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RedFox API key. Security review flagged this release as suspicious because it handles API credentials and recurring outputs; use explicit session-scoped secrets, avoid scanning or editing shell profile files, review generated cache/report files, and confirm cancellation behavior before using subscriptions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
