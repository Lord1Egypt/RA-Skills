## Description:

Codes open-ended survey responses into themes, sentiment labels, and tags, then produces a reviewable coding manual.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Survey researchers, user researchers, and analysts use this skill to turn CSV or text responses into reviewable qualitative coding summaries, including sample overview, themes, sentiment distribution, coding rules, difficult samples, and next-step analysis suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Survey responses may include personal or sensitive information.

Mitigation: Give the skill only the files intended for analysis, redact respondent identifiers where possible, and review outputs before sharing.

Risk: Qualitative coding summaries can overstate conclusions from small or unrepresentative samples.

Mitigation: Treat outputs as reviewable drafts, validate themes against the source responses, and avoid presenting small samples as population-level findings.

Risk: The shipped script contains inactive audit modes that are broader than the advertised survey workflow.

Mitigation: Use the documented survey-response workflow for normal operation and review script behavior before enabling broader audit modes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/survey-response-coder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report, with optional JSON wrapper when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a reviewable draft, a file-backed report, or stdout output; expected sections include sample overview, theme coding, sentiment distribution, coding rules, difficult samples, and follow-up analysis suggestions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
