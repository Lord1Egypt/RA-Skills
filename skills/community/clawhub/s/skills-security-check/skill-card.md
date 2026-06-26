## Description: <br>
Scan a third-party Claude Code skill for security risks before enabling it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hezhijie](https://clawhub.ai/user/hezhijie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to pre-check third-party skills before execution and to run manual deep audits of specific skill directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill adds a local PreToolUse hook that runs before future Skill invocations. <br>
Mitigation: Review install.sh before installation, keep the settings.json backup, and remove the hook if always-on pre-checking is no longer desired. <br>
Risk: Manual deep audits inspect files under the provided skill directory path. <br>
Mitigation: Run manual audits on specific skill directories instead of broad private folders. <br>
Risk: The pre-check is pattern-based and is designed to block critical findings, while lower-severity warnings may still allow execution. <br>
Mitigation: Use the manual deep audit report and human review for unfamiliar or high-impact skills before enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hezhijie/skills-security-check) <br>
- [Artifact: English README](README_EN.md) <br>
- [Artifact: skill instructions](SKILL.md) <br>
- [Artifact: quick pre-check script](scripts/pre-check.sh) <br>
- [Artifact: full scan script](scripts/scan.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text security audit report with risk levels, findings, recommendations, and installation or hook configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual audits require a skill directory path; automatic protection installs a local PreToolUse hook for Skill invocations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
