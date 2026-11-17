## Description:

Collects TikTok videos, creators, hashtags, and profiles through the user's own browser session with the MonsterGet extension, then exports collected data to CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosstzc](https://clawhub.ai/user/rosstzc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect TikTok search, creator, hashtag, profile, and creator-video data for social media research, marketing research, or content monitoring. It guides setup, opens the user's selected browser, orchestrates collection, and saves CSV results locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's real logged-in browser session to collect TikTok data through MonsterGet.

Mitigation: Install and run it only when the user accepts use of their own TikTok and MonsterGet sessions, and remind users to keep account, platform, and data-use responsibilities in mind before collection.

Risk: The skill can download CSV files locally and persist browser, download, and task state under the user's MonsterGet state directory.

Mitigation: Tell users where CSV files are saved, avoid sharing collected files unintentionally, and review local state if the browser choice or download directory should change.

Risk: The skill includes auto-update behavior and installation guidance that can keep client rules pointing at this skill in future agent sessions.

Mitigation: Review the update behavior before use, disable or skip auto-updates when change control is required, and inspect client rule files if the skill should no longer load automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rosstzc/skills/tiktok-collector)
- [MonsterGet homepage](https://monsterget.com)
- [MonsterGet extension install](https://monsterget.com/install)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, CSV files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON status objects, and locally downloaded CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's logged-in browser session and persists browser and download settings under the user's local MonsterGet state directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and VERSION.json report 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
