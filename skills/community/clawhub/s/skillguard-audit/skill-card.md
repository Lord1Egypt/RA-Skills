## Description:

Audit OpenClaw skills for security risks before installation via SkillGuard API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanliu811026](https://clawhub.ai/user/jonathanliu811026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security-conscious OpenClaw users use this skill to audit skills before installation and to gate ClawHub installs based on returned risk verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audited source code is transmitted to the external SkillGuard API.

Mitigation: Audit only code that is acceptable to share externally; avoid submitting proprietary code, secrets, or sensitive files.

Risk: The safe-install wrapper can skip the audit and does not prove the installed artifact exactly matches the audited artifact.

Mitigation: Avoid force mode for routine installs and verify the artifact source or hash separately before installation.

Risk: Remote audit verdicts are incomplete pre-install guarantees.

Mitigation: Treat the returned verdict as one review signal and inspect relevant source and threats before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonathanliu811026/skills/skillguard-audit)
- [Publisher profile](https://clawhub.ai/user/jonathanliu811026)
- [SkillGuard API homepage](https://api.agentsouls.io)
- [SkillGuard audit API](https://api.agentsouls.io/api/audit)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON audit verdicts and terminal install prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and clawhub; submits audited source code to the SkillGuard API.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
