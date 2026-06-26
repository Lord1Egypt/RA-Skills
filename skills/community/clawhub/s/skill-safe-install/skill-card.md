## Description: <br>
Skill Safe Install helps agents install ClawHub skills after a three-layer security check using Skill-Vetter review, ClawHub rating checks, and ThreatBook sandbox scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CHJ0w0](https://clawhub.ai/user/CHJ0w0) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to check a ClawHub skill before installation, review risk signals, and either install, stop, or request confirmation based on the decision matrix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted skill names can reach local shell commands. <br>
Mitigation: Use only ordinary registry-style skill names and review or patch the installer before relying on it as a safety gate. <br>
Risk: Auto or bypass options can reduce or skip confirmation and scan safeguards. <br>
Mitigation: Avoid --auto, --yes, --force, --no-vetter, and --no-scan unless the operator explicitly accepts the risk. <br>
Risk: ThreatBook sandbox scanning may share uploaded skill contents with an external service. <br>
Mitigation: Do not scan private or proprietary skills unless sharing their contents with ThreatBook is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CHJ0w0/skill-safe-install) <br>
- [ThreatBook cloud sandbox](https://s.threatbook.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text with command output and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, curl, tar, zip, and THREATBOOK_API_KEY; can run in dry-run mode before installation.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
