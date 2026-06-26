## Description: <br>
Auto-fetches recent X/Twitter posts from followed accounts and helps generate structured AI digests for configurable time ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaima2022](https://clawhub.ai/user/kaima2022) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to fetch recent posts from their X/Twitter followings and turn them into daily or weekly intelligence digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires X/Twitter session cookie values AUTH_TOKEN and CT0, which can expose account access if shared or logged. <br>
Mitigation: Treat AUTH_TOKEN and CT0 like passwords; use a trusted machine and CLI, and keep the values out of shell history, logs, screenshots, and shared environments. <br>
Risk: Scheduled use can repeatedly fetch authenticated X/Twitter data from followed accounts. <br>
Mitigation: Configure recurring jobs only when that behavior is intended, and review where fetched tweet JSON and generated digests are stored or shared. <br>


## Reference(s): <br>
- [AI Digest Analyst Prompt Template](references/analyst_prompt_template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kaima2022/x-followings-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [JSON tweet data and Markdown digest guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable tweet limits and lookback windows of 1, 3, 7, or custom days.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
