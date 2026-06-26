## Description: <br>
Personal X (Twitter) analytics for timeline engagement, mentions, follower tracking, tweet and thread reading, bookmarks, and combined briefings through X API v2 with persistent local caching and daily budget guards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nevaaron](https://clawhub.ai/user/nevaaron) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent read and summarize X account activity, mentions, profiles, bookmarks, and selected tweets or threads while tracking API spend. It is suited for personal social-media analytics, morning briefings, follower tracking, and accountability checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires X API credentials and stores X content, mentions, bookmarks, usage, and follower history locally. <br>
Mitigation: Use least-privilege credentials where possible and protect ~/.openclaw/.env plus ~/.openclaw/skills-config/x-twitter/. <br>
Risk: Bookmark add and remove commands can change the user's X account state. <br>
Mitigation: Require explicit user approval before running bookmark-changing commands. <br>
Risk: Budget override flags can bypass normal API spend controls. <br>
Mitigation: Require explicit user approval before using --force or --no-budget. <br>
Risk: The setup guide includes installing uv through a remote shell script. <br>
Mitigation: Prefer a verified package-manager installation path for uv when available. <br>


## Reference(s): <br>
- [X Smart Read on ClawHub](https://clawhub.ai/nevaaron/x-smart-read) <br>
- [Setup Guide](SETUP.md) <br>
- [Agent Command Reference](AGENTS.md) <br>
- [X API Quick Reference](references/x-api-quickref.md) <br>
- [X Developer Platform](https://developer.x.com) <br>
- [uv](https://astral.sh/uv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with shell command examples and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cached X content, API spend summaries, engagement metrics, mentions, profile statistics, bookmark actions, and budget warnings.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
