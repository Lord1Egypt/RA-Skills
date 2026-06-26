## Description: <br>
Analyze Claude Code session history to generate self-observation journals, detect goal drift, and surface hidden behavioral patterns. Outputs to Obsidian Vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuiooo1102-droid](https://clawhub.ai/user/yuiooo1102-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to sync local session history into an Obsidian Vault and generate concise reflection, goal-drift, and pattern-discovery reports from their own notes and conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes local Claude Code history and Obsidian notes, which may contain sensitive personal, client, health, credential, or business information. <br>
Mitigation: Use it only on vaults whose contents are appropriate for reflection reports; review generated files and delete unwanted digests or profiles. <br>
Risk: Reflection outputs can consolidate personal observations and behavioral patterns into durable Markdown files. <br>
Mitigation: Avoid shared or synced vaults for sensitive material, and keep memory updates subject to explicit user consent. <br>
Risk: Credential redaction is pattern based and may not catch every secret or sensitive detail. <br>
Mitigation: Review synced session digests and generated reports before sharing or retaining them. <br>


## Reference(s): <br>
- [Session Reflect on ClawHub](https://clawhub.ai/yuiooo1102-droid/session-reflect) <br>
- [Daily Reflection Command](commands/reflect/default.md) <br>
- [Goal Drift Command](commands/reflect/drift.md) <br>
- [Hidden Patterns Command](commands/reflect/emerge.md) <br>
- [Obsidian + Claude Code Codebook](https://www.youtube.com/watch?v=6MBq1paspVU) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and local configuration files with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local Obsidian Vault reports and session digests; generated reports are concise and intended for user review.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
