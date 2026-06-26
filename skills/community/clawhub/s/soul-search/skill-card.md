## Description: <br>
Browse categories, preview, apply, and restore OpenClaw SOUL.md personas from a curated remote catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexleach](https://clawhub.ai/user/alexleach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to browse, preview, apply, and restore workspace SOUL.md personas from a curated catalog while keeping backups and local provenance metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying or restoring a SOUL.md can change future agent behavior in the workspace. <br>
Mitigation: Preview persona source content when possible, apply only catalog entries the user trusts, keep backups, and start a new session after apply or restore. <br>
Risk: Remote catalog content can influence which persona file is fetched and applied. <br>
Mitigation: Use the configured catalog and raw content sources only, validate SOUL.md-like content before writing, and avoid applying untrusted catalog entries. <br>


## Reference(s): <br>
- [Sources](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/alexleach/soul-search) <br>
- [Default catalog](https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json) <br>
- [Baseline OpenClaw SOUL.md template](https://docs.openclaw.ai/reference/templates/SOUL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown command output from the Node.js helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read remote catalog entries, write SOUL.md, create backups under soul-data/backups, and record state in soul-data/state.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
