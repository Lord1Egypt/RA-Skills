## Description:

Generates a personal WeRead reading timeline from books with notes, with an optional JSON export or full-page screenshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jes614753-sketch](https://clawhub.ai/user/jes614753-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

WeRead account holders use this skill to visualize their books with notes in a personal reading timeline, or regenerate it from a saved JSON export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser login state and exported reading data may expose account or personal information.

Mitigation: Keep the saved profile and JSON, HTML, and screenshot exports private; do not commit or sync them publicly.

Risk: Browser automation accesses a signed-in WeRead account.

Mitigation: Use only an account you control and run the automation only if you are comfortable with its account risks.

Risk: Unpinned dependencies can change across installations.

Mitigation: Consider pinning reviewed dependency versions before repeated or shared use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jes614753-sketch/skills/weread-timeline-wall)
- [WeRead](https://weread.qq.com)

## Skill Output:

**Output Type(s):** [HTML, JSON, Image]

**Output Format:** [Single HTML page; optional JSON export and PNG screenshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups books by recent activity; cover images require an internet connection.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
