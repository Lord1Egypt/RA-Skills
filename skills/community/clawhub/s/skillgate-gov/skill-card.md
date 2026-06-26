## Description: <br>
Supply-chain governance for OpenClaw skills: scan, assess, quarantine/restore. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyecom](https://clawhub.ai/user/liyecom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill maintainers use this skill to run SkillGate governance checks on OpenClaw skills, generate evidence, and quarantine or restore risky skills when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a pinned npm package, so package metadata and integrity should be checked before first use. <br>
Mitigation: Verify the pinned npm package metadata and integrity with the documented npm commands before installing or running it. <br>
Risk: Quarantine and restore actions can move or mark files inside the target skills directory. <br>
Mitigation: Run scans first, review the generated evidence, and use quarantine or restore only against an intended skills directory. <br>


## Reference(s): <br>
- [ClawHub SkillGate Governance release](https://clawhub.ai/liyecom/skillgate-gov) <br>
- [OpenClaw SkillGate project homepage](https://github.com/skillgatesecurity/openclaw-skillgate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and governance guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local evidence generation and optional quarantine or restore actions against a user-specified skills directory.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
