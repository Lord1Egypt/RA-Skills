## Description:

Proofreads copy against a provided brand voice specification or approved samples, flags inconsistencies in tone, wording, pronouns, and forbidden or required terms, and suggests rewrites without changing facts or commitments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, content, support, and brand teams use this skill to review Chinese-language copy against brand voice rules before publication. It produces a structured Markdown report with rule interpretation, inconsistency findings, fact-check reminders, a consistency summary, and a revised draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides risk-word hints but does not perform legal, advertising, or platform compliance review.

Mitigation: Treat risk-word hints as prompts for user or legal review rather than compliance conclusions.

Risk: Broad brand-voice trigger terms may activate the skill in environments where accidental activation matters.

Mitigation: Review trigger configuration before deployment and narrow activation language if the environment requires stricter routing.

Risk: Rewrite suggestions could accidentally strengthen claims or alter business commitments if not reviewed.

Mitigation: Review suggested rewrites against the original copy and keep numbers, dates, prices, scope, and service commitments unchanged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-brand-voice-check)
- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-brand-voice-check)
- [Voice dimensions reference](artifact/references/voice-dimensions.md)
- [Report template](artifact/templates/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes categorized inconsistency findings, rewrite suggestions, risk-word hints, fact-confirmation notes, a consistency score, and a unified revised draft.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
