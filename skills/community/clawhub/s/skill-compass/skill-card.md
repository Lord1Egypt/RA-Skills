## Description: <br>
Evaluate skill quality, find the weakest dimension, and apply directed improvements while tracking usage to spot idle or risky skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishna-505](https://clawhub.ai/user/krishna-505) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams maintaining Claude Code or OpenClaw skills use SkillCompass to evaluate skill quality, identify the weakest evaluation dimension, apply guided improvements, and monitor installed-skill usage for stale or risky skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hooks can auto-run local Node.js scripts during session and tool-use events. <br>
Mitigation: Review hooks/hooks.json and the referenced hook scripts before enabling the skill, and install only in environments where local hook execution is acceptable. <br>
Risk: Write-capable flows can modify skills, snapshots, logs, configuration, or local .skill-compass state. <br>
Mitigation: Use read-only evaluation first, back up important skills and ~/.claude/settings.json, and rely on explicit opt-in write, rollback, merge, or update flows only after reviewing the proposed action. <br>
Risk: Custom security tool commands from .skill-compass/config.json can execute local shell commands. <br>
Mitigation: Do not trust custom security tool configuration from untrusted workspaces; inspect .skill-compass/config.json before running security scans. <br>
Risk: The statusLine setup path referenced by the security guidance may be incomplete until hud-extra.js is resolved. <br>
Mitigation: Avoid enabling the statusLine option until the referenced script path is present and reviewed. <br>


## Reference(s): <br>
- [SkillCompass homepage](https://github.com/Evol-ai/SkillCompass) <br>
- [ClawHub SkillCompass page](https://clawhub.ai/krishna-505/skill-compass) <br>
- [README](README.md) <br>
- [Security and trust model](SECURITY.md) <br>
- [Evaluation result schema](schemas/eval-result.json) <br>
- [Feedback signal schema](schemas/feedback-signal.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, JSON evaluation results, shell commands, and local configuration or skill-file changes when explicitly requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only evaluation is the default; write, update, merge, rollback, and multi-round improvement flows require explicit user action and may write local .skill-compass state, snapshots, reports, or skill changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
