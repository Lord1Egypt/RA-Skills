## Description:

Evaluates SKILL.md files or skill folders against an 8-dimension rubric and produces bilingual quality reports with scores, issues, and actionable improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this agent skill to review, score, and improve SKILL.md files or complete skill folders before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad skill-review phrasing.

Mitigation: Use it for explicit skill audit, review, score, lint, or improvement requests, and confirm the intended target when the user's request is ambiguous.

Risk: The skill reads the skill files or folders it is asked to review, including referenced files inside the target.

Mitigation: Point it only at artifacts intended for review and avoid including unrelated sensitive files in the target folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/skill-scorer)
- [README](README.md)
- [Scoring rubric](references/rubric.md)
- [Anti-pattern checklist](references/anti-patterns.md)
- [Report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Bilingual Markdown quality report with score tables, severity-ranked findings, quick wins, and an optimization roadmap]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese report first and English report second, with identical scores, issues, and recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
