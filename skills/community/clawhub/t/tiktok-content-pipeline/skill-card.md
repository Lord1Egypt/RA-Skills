## Description: <br>
Automates TikTok carousel content creation, smart scheduling, publishing through Postiz, and analytics-driven optimization for niche accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matttandy855](https://clawhub.ai/user/matttandy855) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, operators, and developers use this skill to generate TikTok carousel content, manage account-specific templates, schedule posts, publish through a connected Postiz/TikTok account, and review analytics for content improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected Postiz and TikTok accounts can publish or schedule real content. <br>
Mitigation: Use draft mode or a test account first, review generated content and account settings, and enable live posting only after confirming the target configuration. <br>
Risk: API keys and integration IDs are needed for publishing and analytics. <br>
Mitigation: Prefer the POSTIZ_API_KEY environment variable, avoid passing secrets in CLI arguments, and keep local account configuration private. <br>
Risk: Automation and auto-improve behavior can modify account configuration or posting behavior. <br>
Mitigation: Review analytics recommendations before enabling auto-improve or cron-based posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matttandy855/tiktok-content-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/matttandy855) <br>
- [README](README.md) <br>
- [Setup Guide](SETUP.md) <br>
- [Agent Reference](SKILL.md) <br>
- [Postiz](https://postiz.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown guidance, JSON configuration, generated image files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local account configuration, generated content assets, analytics reports, and Postiz publishing or scheduling actions.] <br>

## Skill Version(s): <br>
1.0.4 (source: evidence.json server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
