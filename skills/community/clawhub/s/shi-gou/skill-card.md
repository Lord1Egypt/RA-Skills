## Description:

Shi Gou monitors permission-denial events, scans text for prompt injection, path traversal, and dangerous-command patterns, and produces security reports with potential threat alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lt8899789](https://clawhub.ai/user/lt8899789)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security-focused agent operators use Shi Gou to screen user input or command text for common unsafe patterns, generate short security posture reports, and sanitize commands before logging or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command sanitizer can expose original secrets in removed_patterns when sanitizer results are logged or shared.

Mitigation: Review sanitizer output before use and avoid logging or sharing removed_patterns until that behavior is fixed.

## Reference(s):

- [Shi Gou ClawHub Skill Page](https://clawhub.ai/lt8899789/skills/shi-gou)
- [Artifact README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON objects and concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Security checks return safety status, detected threats, severity labels, matched patterns, and summaries; reports include period statistics and recommendations.]

## Skill Version(s):

2.0.24 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
