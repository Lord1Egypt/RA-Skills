## Description: <br>
Track movies and series with progress, watchlist, ratings, and proactive alerts for new releases and platform changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to help an agent track personal movie and series progress, watchlists, ratings, recommendations, family viewing status, and streaming-platform notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause the agent to keep entertainment and family viewing notes in ~/shows/, including preferences, progress, and child-related viewing reactions. <br>
Mitigation: Use explicit commands for saving progress or recommendations, and avoid recording sensitive family details unless local storage is intended. <br>
Risk: Streaming availability and release timing can become stale or vary by region. <br>
Mitigation: Treat platform availability as last-known information and re-verify with a current streaming source before acting on a recommendation. <br>
Risk: Broad trigger wording may lead the agent to log show-related mentions when the user intended only casual conversation. <br>
Mitigation: Confirm before creating or updating persistent watch records when intent is ambiguous. <br>


## Reference(s): <br>
- [ClawHub Shows Skill](https://clawhub.ai/ivangdavila/shows) <br>
- [Discovery & Recommendations](artifact/discovery.md) <br>
- [Family Viewing Mode](artifact/family.md) <br>
- [Streaming Platforms](artifact/platforms.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and plain text notes, watch-status summaries, recommendations, and local file updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entertainment tracking notes in local Markdown files under ~/shows/ when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
