## Description:

Audit third-party or custom skills for permission risk, unsafe commands, and integration safety before adoption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit third-party or custom OpenClaw skills for permission, install, shell command, environment, and source-trust risks before adoption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit output may be conservative or incomplete when source trust, permissions, commands, environment usage, or install steps are missing.

Mitigation: Provide complete skill metadata and review the resulting recommendation manually before installation or permission changes.

Risk: The skill flags risky patterns but does not itself enforce sandboxing or block installation.

Mitigation: Use its findings as review guidance and apply sandboxing, scanner results, and human review before adopting high-privilege skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunbinnju-star/skills/skill-security-auditor-jack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown audit report with schema-style fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk level, suspicious actions, over-privileged points, install recommendation, sandbox recommendation, and audit summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
