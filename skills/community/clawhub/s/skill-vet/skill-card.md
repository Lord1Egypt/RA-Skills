## Description:

Scans skills before installation or execution for suspicious code, commands, network access, and other potential security threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luwinher](https://clawhub.ai/user/luwinher)

### License/Terms of Use:


## Use Case:

Developers and reviewers use Skill Vet before installing or running a ClawHub or OpenClaw skill to identify suspicious JavaScript, shell, filesystem, subprocess, network, and credential-access patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner results may be incomplete or associated with the wrong path.

Mitigation: Run the scan against the exact skill artifact being reviewed and manually inspect the reported file paths and findings.

Risk: A successful command exit can still include warnings and should not be treated as proof that a skill is safe.

Mitigation: Use Skill Vet as one review input, then perform human review and any required organizational security checks before installation or deployment.

## Reference(s):

- [ClawHub Skill Vet page](https://clawhub.ai/luwinher/skills/skill-vet)
- [ClawHub publisher profile](https://clawhub.ai/user/luwinher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and text scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return warnings even when the command exits successfully; review the exact target path and scan output before relying on the result.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
