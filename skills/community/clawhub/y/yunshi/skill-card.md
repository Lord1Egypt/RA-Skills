## Description: <br>
Yunshi helps agents provide Chinese astrology and divination readings across BaZi, ZiWei DouShu, QiMen DunJia, I Ching, feng shui, marriage compatibility, and daily fortune push workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Yunshi to generate Chinese fortune-telling guidance, manage local birth-profile data, and prepare daily horoscope push content. It supports birth-chart analysis, divination, feng shui recommendations, relationship compatibility, and recurring daily fortune summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store sensitive birth time, birthplace, family, preference, and push-log data locally, and command output may reveal that data. <br>
Mitigation: Use it only with explicit consent, restrict profile file permissions, avoid sharing dry-run/list/status output, and delete local profiles when they are no longer needed. <br>
Risk: Scheduled daily push messages could send fortune content without clear opt-in or to an unintended channel. <br>
Mitigation: Enable push delivery only after explicit opt-in and review the target user, channel, and schedule before activating recurring delivery. <br>
Risk: The optional knowledge-directory setting could point the skill at unintended sensitive files. <br>
Mitigation: Set OPENCLAW_KNOWLEDGE_DIR only to an intended directory of non-sensitive Markdown knowledge files. <br>


## Reference(s): <br>
- [ClawHub Yunshi skill page](https://clawhub.ai/jiajiaoy/yunshi) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Related ClawHub skill: lucky-today](https://clawhub.ai/skills/lucky-today) <br>
- [User registration flow](docs/注册流程.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local JSON profile data and generate scheduled push-message content when those workflows are enabled.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
