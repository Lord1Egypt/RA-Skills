## Description: <br>
Manage multiple social media platforms to automate posting, scheduling, draft and template management, timeline viewing, interactions, and analytics via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HiroFumiko](https://clawhub.ai/user/HiroFumiko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and operators use this skill to manage social media workflows from a CLI, including posting to X/Twitter, scheduling content, managing drafts and templates, and reviewing timelines and interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can perform real actions on connected social-media accounts, including public posts and interactions. <br>
Mitigation: Use a test account first and review immediate, scheduled, and recurring posts before enabling automation. <br>
Risk: API tokens and account credentials may be stored locally in environment variables or a .env file. <br>
Mitigation: Keep .env out of source control and backups, restrict local file permissions, and rotate tokens if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/HiroFumiko/social-media-automation) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in local configuration files, SQLite records, and social-media API actions when the CLI commands are executed.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata, created 2026-03-14T19:30:05Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
