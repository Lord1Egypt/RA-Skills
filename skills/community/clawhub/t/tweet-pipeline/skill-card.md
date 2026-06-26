## Description: <br>
Notion-to-Twitter automation that pulls approved tweets from a Notion database, schedules one-shot jobs for exact post times, and posts via the X/Twitter API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content operators and developers use this skill to automate scheduled X/Twitter posts from a Notion content calendar. It reads approved Notion entries, schedules or posts them at the intended time, and updates Notion status after posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live posts to X/Twitter and modify Notion using local credentials. <br>
Mitigation: Run with --dry-run first, confirm the target X account and Notion database, and only enable posting on a machine intended for this workflow. <br>
Risk: The skill can create persistent one-shot OpenClaw cron jobs for later execution. <br>
Mitigation: Inspect scheduled OpenClaw crons after use and remove any unintended jobs before leaving the workflow unattended. <br>
Risk: Hard-coded local paths and account assumptions may point to the wrong binaries, scripts, or profile in another environment. <br>
Mitigation: Replace local paths and account-specific values with environment-appropriate configuration before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nissan/tweet-pipeline) <br>
- [Notion API](https://api.notion.com) <br>
- [X API](https://api.x.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, Notion access, X/Twitter credentials, outbound network access, and review of scheduled jobs before unattended use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
