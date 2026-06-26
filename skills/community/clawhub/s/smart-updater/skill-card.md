## Description: <br>
Smart Updater helps OpenClaw users inventory installed skills, extensions, and core components, check available updates, assess changelog risk, and apply approved upgrades with backup and rollback gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanhui](https://clawhub.ai/user/yuanhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect installed OpenClaw assets, compare them with remote sources, summarize changelogs and risk, and execute only user-approved upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace installed OpenClaw skills, extensions, and core components from remote sources, including a SkillHub mirror fallback path. <br>
Mitigation: Use explicit manual invocations, review each proposed asset and changelog before approval, and keep the skill's backup and rollback gates enabled. <br>
Risk: Forced or unattended upgrades could introduce code changes without enough human review. <br>
Mitigation: Avoid cron or auto-upgrade modes unless the environment accepts unattended code changes; require explicit user selection before running upgrades. <br>
Risk: Incomplete changelog evidence can lead to incorrect risk classification for an update. <br>
Mitigation: Treat missing changelogs as manual-review items and do not generate an upgrade report until every candidate has a changelog source or an explicit unavailable note. <br>


## Reference(s): <br>
- [Smart Updater ClawHub Page](https://clawhub.ai/yuanhui/smart-updater) <br>
- [Product Requirements](docs/PRD.md) <br>
- [Three Gates](references/three-gates.md) <br>
- [Report Format](references/report-format.md) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with shell command execution and JSON inventory or scan files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill writes local inventory and scan-result JSON files under the user's OpenClaw directory and may run update commands after explicit user approval.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
