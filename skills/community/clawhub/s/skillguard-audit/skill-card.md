## Description: <br>
Audit OpenClaw skills for security risks before installation via the SkillGuard API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathanliu811026](https://clawhub.ai/user/jonathanliu811026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to audit OpenClaw skills or local skill files before installation. It helps them review verdicts, risk scores, and threat lists before deciding whether to proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auditing sends skill source or selected local files to api.agentsouls.io. <br>
Mitigation: Do not audit private code, secrets, or proprietary skills unless you trust the service and its retention claim; use manual review or self-hosting when external upload is not acceptable. <br>
Risk: The safe-install wrapper can install a target skill and includes a force mode that skips the audit. <br>
Mitigation: Treat safe-install.sh as an installer, avoid --force unless the target skill is already trusted, and review CAUTION or UNKNOWN audit results manually before installing. <br>


## Reference(s): <br>
- [ClawHub SkillGuard page](https://clawhub.ai/jonathanliu811026/skillguard-audit) <br>
- [SkillGuard API homepage](https://api.agentsouls.io) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Shell commands] <br>
**Output Format:** [JSON audit results with terminal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a verdict, risk score, and threat list; the installer wrapper may prompt before installation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
