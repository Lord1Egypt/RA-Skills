## Description: <br>
Packages, migrates, and clones OpenClaw agent team configuration, including identity files, team members, skills, and optional scheduled task configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao-zwl](https://clawhub.ai/user/zhao-zwl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to back up, migrate, or duplicate an agent team across machines or into a separate working copy while preserving configuration, team members, skills, and scheduled tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration packages can contain private memories, prompts, account details, API keys, and workspace configuration. <br>
Mitigation: Treat generated packages as secrets, avoid public sharing, and use encrypted transfer or storage. <br>
Risk: Imported cron tasks can persistently run agent actions or commands after migration. <br>
Mitigation: Inspect cron_tasks.json in full and use --no-cron until every scheduled payload is trusted. <br>
Risk: Configuration changes to ~/.qclaw/openclaw.json can affect agent spawning and team routing. <br>
Mitigation: Run migrate.py with --dry-run first and review the displayed diff before applying changes. <br>
Risk: Gateway restarts can interrupt active OpenClaw sessions. <br>
Mitigation: Use --no-restart when continuity matters, then restart manually during an acceptable maintenance window. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhao-zwl/team-resurrection) <br>
- [Publisher profile](https://clawhub.ai/user/zhao-zwl) <br>
- [README.md](README.md) <br>
- [MATERIAL_PACKING.md](MATERIAL_PACKING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate migration ZIP packages and propose OpenClaw configuration, cron task, and gateway restart actions.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and SKILL.md metadata.openclaw.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
