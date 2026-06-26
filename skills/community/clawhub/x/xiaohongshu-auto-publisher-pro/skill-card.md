## Description: <br>
小红书图文自动发布引擎，用于定时生成内容、自动排版并计划发布到小红书平台。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijinhao123-dot](https://clawhub.ai/user/lijinhao123-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, agencies, and brand marketing teams use this skill to generate Xiaohongshu post ideas, draft notes, manage a posting schedule, and review post-performance feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide scheduled posting and browser automation for a live Xiaohongshu account. <br>
Mitigation: Use draft-only behavior unless scheduled publishing is explicitly intended, confirm the active account, and manually approve each post before publication. <br>
Risk: Local schedule files or cron jobs may continue to trigger publishing actions after setup. <br>
Mitigation: Keep an inventory of created schedule files and cron jobs, review them regularly, and remove them when the campaign or test is finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijinhao123-dot/xiaohongshu-auto-publisher-pro) <br>
- [Publisher profile](https://clawhub.ai/user/lijinhao123-dot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and scheduled-publishing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local posting schedule file and guide browser automation for Xiaohongshu publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
