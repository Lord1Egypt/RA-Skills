## Description: <br>
Safe OpenClaw upgrade workflow with pre-flight config checks, automatic backup, post-upgrade migration, and rollback guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w-sss](https://clawhub.ai/user/w-sss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when upgrading OpenClaw installations, especially before version jumps or when configuration changes may prevent the gateway from starting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual upgrade commands can modify OpenClaw configuration, install global packages, and restart the gateway. <br>
Mitigation: Review each command before execution, create the documented backup first, and verify gateway health before and after upgrade steps. <br>
Risk: OpenClaw configuration backups may contain sensitive settings. <br>
Mitigation: Treat files under ~/.openclaw/openclaw.json and ~/.openclaw/upgrade-guard as sensitive and protect or remove backups according to local policy. <br>
Risk: The old-backup pruning command removes backup directories. <br>
Mitigation: Review or replace the pruning command before running it, especially on systems where backup retention requirements apply. <br>


## Reference(s): <br>
- [Upgrade Guard Chinese Usage Reference](references/zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides backup, verification, migration, and rollback steps for OpenClaw upgrades.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
