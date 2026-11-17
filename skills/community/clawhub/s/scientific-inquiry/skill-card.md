## Description:

Rigorous evidence-based inquiry: decompose fuzzy questions, retrieve and grade evidence, cross-validate sources, and output conclusions with confidence intervals after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liwenyu2002](https://clawhub.ai/user/liwenyu2002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and conduct evidence-based fact-checking, data research, industry analysis, comparisons, and trend inquiries. It structures questions, grades sources, cross-validates findings, and returns confidence-labeled conclusions with source URLs and uncertainties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist feedback and update its own instructions when explicitly prompted, which may alter future behavior if untrusted text is accepted.

Mitigation: Require explicit confirmation with the exact proposed memory entry or patch contents, and avoid self-updates from untrusted or copied text.

Risk: Research outputs may be misleading if weak, stale, unavailable, or misgraded sources are treated as conclusive evidence.

Mitigation: Use the planned confirmation step, full source URLs, evidence grades, cross-validation, and uncertainty reporting before relying on conclusions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research plans, evidence tables, claim verification reports, and concise confidence summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before retrieval and includes source URLs, evidence grades, confidence labels, and uncertainties.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
