## Description:

Scan a third-party Claude Code skill for security risks before enabling it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hezhijie](https://clawhub.ai/user/hezhijie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit third-party Claude Code skills before enabling them, either through manual deep audits or an installed pre-check hook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release persistently changes Claude's global hook configuration before future Skill calls.

Mitigation: Install only when that global pre-check behavior is intended, and review the settings.json hook change before use.

Risk: The pre-check can pass some unresolved, namespaced, or nested-script cases without full inspection.

Mitigation: Treat a passing pre-check as a starting signal, not proof of safety; run a manual audit and review the target skill before relying on it.

Risk: The installed scripts become part of the security boundary for future Skill calls.

Mitigation: Keep the installed scripts protected from tampering and remove the hook if the package is no longer trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hezhijie/skills/skills-security-check)
- [Publisher profile](https://clawhub.ai/user/hezhijie)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown security report with risk levels, findings, and a safety recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual audit output is based on a supplied skill directory; installed hook behavior can block critical findings before skill execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
