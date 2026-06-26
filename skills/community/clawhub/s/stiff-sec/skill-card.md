## Description: <br>
Audits and hardens OpenClaw configurations by checking common security weaknesses, backing up config files, and applying stricter local proxy and tool policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sf-dev-systems](https://clawhub.ai/user/sf-dev-systems) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit local OpenClaw config state, identify likely plaintext credentials, and apply backup-first hardening to proxy and tool-execution settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hardening routine changes persistent OpenClaw configuration and offers limited user control before writes or restores. <br>
Mitigation: Review the exact changes before running apply, run the audit first, and keep the generated backup available for restore. <br>
Risk: Backups may contain tokens or other sensitive values copied from the OpenClaw configuration. <br>
Mitigation: Keep the backup directory private, restrict local access to it, and remove stale backups when they are no longer needed. <br>
Risk: The release overstates checksum, signed lockfile, permission hardening, and tamper detection protections. <br>
Mitigation: Do not rely on those claims unless the scripts have been independently verified and patched for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sf-dev-systems/stiff-sec) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [audit.py](scripts/audit.py) <br>
- [stiffen.py](scripts/stiffen.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python shell commands and plain-text audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Apply and restore commands may modify ~/.openclaw/openclaw.json and create local backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
