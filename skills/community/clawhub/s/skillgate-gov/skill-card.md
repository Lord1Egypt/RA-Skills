## Description:

Supply-chain governance for OpenClaw skills: scan, assess, quarantine/restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyecom](https://clawhub.ai/user/liyecom)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to run SkillGate governance checks against OpenClaw skill directories, review evidence, and quarantine or restore risky skills when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs downloaded npm code when using npx on first use.

Mitigation: Verify the npm package metadata and integrity before installation, and prefer a sandbox or clean environment for scans.

Risk: The evidence states it is unclear when scan workflows may disable or quarantine skills.

Mitigation: Confirm command behavior before use, start with read-only scans, and run quarantine or restore only when persistent changes to OpenClaw skills are acceptable.

## Reference(s):

- [SkillGate homepage](https://github.com/skillgatesecurity/openclaw-skillgate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and command descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce local evidence files; quarantine and restore actions can persistently change the target skills directory.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
