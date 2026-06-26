## Description: <br>
Automatically detect, backup, and update OpenClaw skills using caching, retry logic, dry-run mode, and detailed upgrade reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thunder1743](https://clawhub.ai/user/thunder1743) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to scan installed skills, compare local versions with ClawHub releases, preview updates, apply upgrades, and keep rollback backups and upgrade reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic updates can change installed skills and affect future agent behavior. <br>
Mitigation: Run with --dry-run before --auto, review the ClawHub source and detected version changes, and keep backups until the updated skills are verified. <br>
Risk: The skill writes backups to Desktop and upgrade reports to OpenClaw memory, which may retain update history or local path information. <br>
Mitigation: Review, retain, or delete backup folders and memory reports according to local privacy and retention needs. <br>
Risk: Version checks and downloads depend on network access to ClawHub and can fail because of connectivity, rate limits, or unavailable releases. <br>
Mitigation: Use --cache-only when working offline, review warnings and errors, and retry later if registry calls are rate-limited or unavailable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thunder1743/skills-updater) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [check-skill-updates.py](scripts/check-skill-updates.py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown instructions with shell commands and generated upgrade reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in cache-only, dry-run, interactive, or auto-update modes; real updates create timestamped backups before replacing skills.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
