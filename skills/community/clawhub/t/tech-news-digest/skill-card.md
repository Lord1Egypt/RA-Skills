## Description: <br>
Generates configurable technology news digests from RSS, Twitter/X, GitHub, Reddit, web search, and YouTube-over-RSS sources using quality scoring, deduplication, and multi-format delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinstein](https://clawhub.ai/user/dinstein) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to collect, score, deduplicate, summarize, archive, and deliver daily or weekly technology news digests across configured topics and channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches many external sources and can use configured credentials for Twitter/X, web search, GitHub, and delivery channels. <br>
Mitigation: Review configured sources and tokens before installation, use least-privilege credentials, and disable optional sources or credentials that are not needed. <br>
Risk: Email, Discord, and PDF delivery can send generated digest content to third-party channels or recipients. <br>
Mitigation: Confirm channel IDs, recipient addresses, templates, and schedules before enabling automated delivery. <br>
Risk: Archived digests are written under the workspace and may retain prior report content for deduplication. <br>
Mitigation: Verify archive retention and cleanup behavior match local data-handling expectations before scheduling recurring runs. <br>
Risk: GitHub access can fall back to local gh CLI credentials when other GitHub credentials are unavailable. <br>
Mitigation: Avoid enabling gh CLI fallback if the skill should not use the local GitHub session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinstein/tech-news-digest) <br>
- [Digest prompt template](artifact/references/digest-prompt.md) <br>
- [Configuration schema](artifact/config/schema.json) <br>
- [Discord output template](artifact/references/templates/discord.md) <br>
- [Email output template](artifact/references/templates/email.md) <br>
- [PDF output template](artifact/references/templates/pdf.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digests, JSON pipeline outputs, optional HTML email and PDF report files, and shell command/configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Discord, email, Markdown, and PDF delivery paths; archives generated digests for deduplication.] <br>

## Skill Version(s): <br>
3.16.0 (source: server release metadata, SKILL.md frontmatter, and changelog released 2026-03-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
