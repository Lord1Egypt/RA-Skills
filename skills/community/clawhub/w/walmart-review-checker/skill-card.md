## Description:

Walmart review authenticity analyzer that checks review text and structured review data for suspicious patterns, rating manipulation, timing clusters, verified purchase signals, and incentivized-review indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace analysts, and developers use this skill to review Walmart product feedback for authenticity signals and produce a concise risk-oriented report. The results should be treated as heuristic guidance rather than a definitive fraud determination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is flagged suspicious because the Walmart-specific claims do not match the Amazon-oriented implementation.

Mitigation: Validate outputs against known Walmart review data and prefer a release that resolves the Walmart/Amazon mismatch before relying on the skill for business decisions.

Risk: Generated HTML reports may expose browser-scripting risk when built from untrusted review data.

Mitigation: Use the skill in an isolated local environment, avoid opening generated HTML from untrusted inputs, and prefer a release that escapes report content.

Risk: Installation dependencies are not pinned in the release evidence.

Mitigation: Review and pin dependencies before deployment in a shared or production environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phheng/skills/walmart-review-checker)
- [Publisher Profile](https://clawhub.ai/user/phheng)
- [Nexscope AI](https://www.nexscope.ai/)
- [Chart.js](https://cdn.jsdelivr.net/npm/chart.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report text with optional Python command examples and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces heuristic authenticity scores, risk levels, detection-dimension summaries, suspicious review snippets, and data-completeness hints.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
