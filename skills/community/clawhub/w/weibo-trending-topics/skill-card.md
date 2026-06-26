## Description: <br>
Track Weibo hot search trends in real time, including live trending topics, categories, and historical trend data with no required configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzxiatian-crypto](https://clawhub.ai/user/dzxiatian-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch public Weibo hot-search topics, filter broad trend categories, and compare saved trend snapshots over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests to weibo.com may expose request metadata such as IP address and user agent. <br>
Mitigation: Use the skill only where access to Weibo public endpoints is acceptable, and avoid excessive polling. <br>
Risk: Saved trend snapshots are collected data that may reflect time-sensitive public social-media activity. <br>
Mitigation: Handle stored snapshots according to applicable data-retention and sharing policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dzxiatian-crypto/weibo-trending-topics) <br>
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Python code examples and trend comparison guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request examples and summaries derived from public Weibo trend data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
