## Description: <br>
Skill Discoverer scans the ClawHub Skill marketplace, recommends relevant skills from user context, classifies candidates by installation risk, and can set scheduled digest scans after confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dr23334444](https://clawhub.ai/user/dr23334444) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to discover newly released marketplace skills, evaluate whether they fit current work, and decide whether to install, transform, or skip each candidate. It also supports scheduled marketplace scans and digest-style reporting when the user confirms automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read USER.md and recent memory to personalize recommendations. <br>
Mitigation: Use manual keyword searches when personal context should not be used, and review the inferred search terms before continuing. <br>
Risk: The skill can save chat routing identifiers and maintain local scan configuration, logs, and known-skill caches. <br>
Mitigation: Review the generated configuration and delete or disable stored config and logs when scheduled digests are no longer desired. <br>
Risk: The skill can propose scheduled scans, skill installations, and persistent agent-rule changes. <br>
Mitigation: Require explicit confirmation before installation, cron creation, or MEMORY.md and SOUL.md changes, and review each proposed change before applying it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dr23334444/skill-discoverer) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>
- [ClawhHub Safety Rules](references/clawhhub-safety.md) <br>
- [Example Dialogues](references/examples.md) <br>
- [Install Decision Rules](references/install-decision.md) <br>
- [Search Commands](references/search-commands.md) <br>
- [Learn and Transform Flow](references/step6b-learn-transform.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with structured options, risk notes, and inline command or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local configuration files, scan logs, known-skill caches, scheduled scan jobs, and skill installation choices that require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata, changelog released 2026-03-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
