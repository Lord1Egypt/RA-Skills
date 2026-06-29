## Description: <br>
Fetches top-level Xiaohongshu note comments by note link or ID, supports cursor-based pagination, analyzes sentiment across positive, negative, demand, and competitor dimensions, and can generate an HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brand operators, analysts, MCNs, and social-commerce teams use this skill to inspect Xiaohongshu note comments, summarize audience sentiment, identify user needs, and review competitor mentions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and sends Xiaohongshu note IDs and cursors to redfox.hk. <br>
Mitigation: Use a key with an appropriate scope, keep it in environment configuration, rotate or revoke it when needed, and avoid exposing it in prompts, screenshots, logs, or repositories. <br>
Risk: Generated HTML reports can contain fetched comment text and user metadata. <br>
Mitigation: Treat reports as shareable copies of comment data, store them in an appropriate local directory, remove them when no longer needed, and review before sharing outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/xiaohongshu-comment) <br>
- [RedFox publisher profile](https://clawhub.ai/user/redfox-data) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk?source=github) <br>
- [English README](artifact/README.en.md) <br>
- [Chinese README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, guidance] <br>
**Output Format:** [Markdown responses with JSON command output and an optional local HTML report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches one page per API call, normally up to 20 top-level comments per page, and can backfill AI analysis into the generated HTML report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
