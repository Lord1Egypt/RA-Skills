## Description: <br>
Generates a structured Weibo hot-search daily report by fetching public trending topics, categorizing them, and formatting a segmented summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renyuzhuo](https://clawhub.ai/user/renyuzhuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to fetch current Weibo hot-search topics, group them by topic area, and generate a daily report for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a disclosed third-party Weibo hot-search mirror for live public content. <br>
Mitigation: Use only in environments where this outbound request is acceptable; review or replace the data source for stricter deployments. <br>
Risk: Returned topics are dynamic third-party content and may be incomplete, sensitive, or unsuitable for all audiences. <br>
Mitigation: Review generated reports before sharing and apply local content policies to the output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/renyuzhuo/weibo-hot-daily-skill) <br>
- [Weibo Hot-Search Source](https://weibo.g.renyuzhuo.cn/) <br>
- [README-listed Open Source Link](https://github.com/renyuzhuo/WeiboHotSkills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Segmented markdown-style daily report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches up to 50 hot-search items and prints up to five items per category; no persistence or automatic posting.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and artifact changelog, released 2026-03-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
