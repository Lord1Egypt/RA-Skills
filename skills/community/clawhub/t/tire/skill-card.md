## Description:

Your personal Tire assistant. Use when you need tire.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Tire as a command-line local activity logger for home-management notes, status checks, searches, statistics, and data export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save arbitrary text passed to Tire commands under ~/.local/share/tire.

Mitigation: Avoid entering secrets or sensitive personal data; review or delete ~/.local/share/tire when no longer using the skill.

Risk: Security evidence marks the release suspicious because Tire branding does not match its generic local activity logger behavior.

Mitigation: Review the skill behavior before installation and limit use to non-sensitive local notes.

## Reference(s):

- [ClawHub Tire skill page](https://clawhub.ai/bytesagain3/skills/tire)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text CLI output and local JSON, CSV, or text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores logs and exported files under ~/.local/share/tire.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
