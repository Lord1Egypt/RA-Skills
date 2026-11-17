## Description:

Skill Privacy Guard scans skill files for sensitive information and sanitizes paths, credentials, personal data, network identifiers, and other confidential details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanggroot7](https://clawhub.ai/user/zhanggroot7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to review and sanitize skill files before release so examples, paths, credentials, personal data, and infrastructure details remain generic and shareable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run during skill editing and rewrite files automatically.

Mitigation: Use dry-run or review mode and require explicit user approval before applying file changes.

Risk: Broad sanitization patterns may remove legitimate examples, identifiers, dates, hashes, or configuration details.

Mitigation: Review proposed replacements against the intended skill behavior before committing sanitized content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhanggroot7/skills/skill-privacy-guard)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown security scan summary with sanitization counts and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or report replacements for sensitive values in skill files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
