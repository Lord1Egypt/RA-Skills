## Description:

Organizes US tax season documents and 1099 tracking into a dated checklist that flags missing W-9s and unmatched taxpayer IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External users—US small-business owners, bookkeepers, and CPA-firm administrative staff—use it to organize tax-season records, track W-9 and 1099 tasks, and prepare dated handoffs to a tax preparer. It does not file returns or choose tax positions.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Promised checks may miss missing tax forms or exposed taxpayer identifiers while reporting no problems.

Mitigation: Use redacted inputs, manually verify forms and taxpayer IDs, and do not rely on a 'No flags' result or assume reports mask identifiers.

Risk: The optional Windows app is outside the described Python workflow and has a separate security posture.

Mitigation: Assess the optional Windows app separately before use.

## Reference(s):

- [Tax Season 1099 Reference](references/tax-season-1099.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Dated organizer checklists, vendor tracking, calendar tasks, and Markdown compliance reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Taxpayer IDs should be masked; outputs are organizational aids, not tax advice or filing decisions.]

## Skill Version(s):

1.0.7 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
