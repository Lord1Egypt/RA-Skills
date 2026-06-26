## Description: <br>
Production-safe Ubuntu maintenance orchestrator: runs daily apt security updates, tracks non-security updates across apt/npm/pnpm/brew with quarantine + auto-review, applies only approved updates, rotates logs/state, and generates clear 09:00 MSK Telegram reports (including what was actually installed). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Spiceman161](https://clawhub.ai/user/Spiceman161) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and system operators use this skill to automate conservative Ubuntu host maintenance, track non-security package updates across apt, npm, pnpm, brew, and OpenClaw skills, and generate daily operational reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change system packages and OpenClaw skills during scheduled maintenance. <br>
Mitigation: Install it only on hosts where unattended maintenance is intended, run it under a dedicated account, and review planned package and skill update behavior before enabling schedules. <br>
Risk: Broad sudo permissions could allow maintenance commands beyond the intended scope. <br>
Mitigation: Keep sudoers restricted to the documented apt-get update, apt-get -s upgrade, and unattended-upgrade commands, and avoid granting full sudo access for this skill. <br>
Risk: Some documented dry-run or report paths may still have side effects. <br>
Mitigation: Review or disable apt install/autoremove and report-time clawhub update paths, and test in an isolated environment before relying on dry-run output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Spiceman161/sys-updater) <br>
- [README](README.md) <br>
- [How sys-updater Works](docs/how-it-works.md) <br>
- [Sudoers Setup](docs/sudoers.md) <br>
- [Operations](docs/operations.md) <br>
- [Auto-Review System](docs/AUTO_REVIEW.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces host maintenance reports and command guidance; runtime scripts persist JSON state and rotated logs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
