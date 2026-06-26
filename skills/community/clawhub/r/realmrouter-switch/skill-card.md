## Description: <br>
Zero-friction RealmRouter model manager for OpenClaw. Chat-first workflow for setting API key, guided model picking, switching with availability check, rollback, connectivity testing, and short rr commands on both Unix and Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vegetable1bird](https://clawhub.ai/user/vegetable1bird) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure RealmRouter as an OpenClaw provider, set or update the RealmRouter API key, choose a default model, test connectivity, and roll back configuration changes when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes OpenClaw provider, default model, API key, backup, and gateway state. <br>
Mitigation: Install and run it only when those local configuration changes are intended, and review the generated backup before relying on rollback. <br>
Risk: RealmRouter API keys may be exposed through shared chat, shell history, configuration files, or backups. <br>
Mitigation: Treat the API key as a secret, avoid pasting real keys into shared contexts, and protect ~/.openclaw/openclaw.json and ~/.openclaw/backups. <br>
Risk: The artifact documentation references Windows PowerShell scripts that are not present in the artifact. <br>
Mitigation: Use the bundled Python Windows installer and wrapper when installing on Windows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vegetable1bird/realmrouter-switch) <br>
- [RealmRouter API endpoint](https://realmrouter.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify local OpenClaw configuration, write backups, update a RealmRouter API key, and restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
