## Description:

Security and due diligence layer for installing external skills from ClawHub. Performs DEEP content scanning for malicious patterns, security checks, integration analysis, and requires owner confirmation before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zendenho7](https://clawhub.ai/user/zendenho7)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill before installing external ClawHub skills to run security and integration checks, produce a review report, and require owner confirmation before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated checks can miss or misreport risky skills.

Mitigation: Treat this skill as a helper, manually inspect upstream security reports, and do not rely on its deep scan for final approval.

Risk: The skill relies on unpinned npx execution.

Mitigation: Pin or preinstall a trusted ClawHub CLI and run the check in a low-privilege environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zendenho7/skills/skill-install-guardian)
- [Publisher profile](https://clawhub.ai/user/zendenho7)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report with JSON output and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and manual owner confirmation before installation.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
