## Description:

Makes WorkBuddy built-in skills visible in the installed-skill list and helps check or restore the resulting copies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users can inspect missing built-in skills, make them appear in the installed-skill list, compare copies with originals, and restore the prior state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Syncing can copy or overwrite WorkBuddy skill directories.

Mitigation: Run list and status first, review the affected skills, and use --force only when an overwrite is intended.

Risk: Restoring can delete skill copies, including changed copies when forced.

Mitigation: Review restore --dry-run output and confirm target directories before deleting; avoid --force unless changes can be discarded.

Risk: An explicitly forced bundle patch can disrupt the WorkBuddy interface.

Mitigation: Prefer the default copy-based approach; only patch the bundle after verifying target paths and accepting the higher risk.

## Reference(s):

- [WorkBuddy Skill Visibility on ClawHub](https://clawhub.ai/wangjiaocheng/skills/workbuddy-skill-visibility)
- [Publisher profile on ClawHub](https://clawhub.ai/user/wangjiaocheng)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with diagnostic results and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports affected skills and verification results; changes take effect after restarting WorkBuddy.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
