## Description:

Audits a ClawHub publisher's skill portfolio using registry metrics, search results, and repository evidence to guide portfolio decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

ClawHub publishers use this skill to compare their published skills, assess search competition and adoption signals, and identify one evidence-backed next step. Portfolio changes require comparable historical snapshots; otherwise the skill recommends continued observation or better data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete or incomparable snapshots could lead to misleading growth conclusions or premature portfolio changes.

Mitigation: Require the documented decision-readiness checks and comparable snapshots at least seven days apart; otherwise recommend only observation or data-quality improvements.

Risk: Recommendations to merge, discontinue, or create skills may not fit the publisher's business goals.

Mitigation: Treat portfolio recommendations as advisory and review the supporting evidence before acting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bonniegeng-max/skills/skill-portfolio-growth-audit)
- [Publisher homepage (release metadata)](https://github.com/bonniegeng-max/openclaw-publisher)
- [Growth evidence rules](references/evidence_rules.md)
- [Search competition review](references/competition_review.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown portfolio audit report with metrics, decision-readiness checks, a decision matrix, and one prioritized next action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese-language reporting; distinguishes observed metrics from unverified growth claims.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release; bundled frontmatter and changelog say 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
