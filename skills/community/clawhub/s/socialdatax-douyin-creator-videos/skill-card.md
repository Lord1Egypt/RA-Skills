## Description: <br>
用于抖音达人数据、抖音达人作品、作品列表、图文列表、短剧/合集列表、近期发布、内容调研和创作者内容分析。覆盖 Douyin creator works and series，来自 SocialDataX 社媒数据助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, marketers, and developers use this skill to retrieve and summarize Douyin creator posts, image/text posts, short-drama series, and recent publishing activity through SocialDataX. It supports creator benchmarking, account tracking, and content research from a sec_user_id or profile URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the SocialDataX npm package with SOCIALDATAX_API_KEY for Douyin data queries. <br>
Mitigation: Install and run it only when SocialDataX is trusted, keep the API key in the environment, and avoid exposing the key in prompts, logs, or shared output. <br>
Risk: Unbounded pagination can fetch large creator histories and consume time or API quota. <br>
Mitigation: Prefer bounded requests with --since-days, --pages, or --max-items unless the user explicitly needs a full history. <br>


## Reference(s): <br>
- [SocialDataX homepage](https://socialdatax.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/socialdatax-douyin-creator-videos) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Douyin creator results may include paginated items, interaction counts, media links, publish times, and series metadata.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
