## Description:

Helps quality and certification engineers compare products against type approval or certification baselines and generate product conformance confirmation reports with dimension-by-dimension comparison tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers and certification or compliance engineers use this skill to structure product conformance checks for type approval, 3C/CCC, COP tracking, marking compliance, and supplier-change impact review. It helps assemble comparison tables, deviation lists, risk alerts, and corrective-action suggestions from user-provided product and certification records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce compliance-looking conclusions from incomplete or unverified baseline data.

Mitigation: Require citations to enterprise or certification documents and review generated conclusions before using them for audits or regulatory submissions.

Risk: The artifact references a report-building script that is not bundled with the release.

Mitigation: Use the release as a guidance/template skill unless a separately vetted report generator is supplied.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duding-engicool/skills/skill-product-conformance-confirm)
- [Server-Resolved GitHub Source](https://github.com/duding-engicool/skill-product-conformance-confirm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text and Markdown report guidance with product conformance comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided product identifiers, confirmation type, and authoritative enterprise or certification baseline documents.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
