## Description:

帮助企业围绕中国专精特新梯度培育申报进行资格自评，并生成申请书、佐证材料清单和交互式 HTML 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and consultants use this skill to prepare Chinese SRDI application materials, check tier eligibility, and assemble filing checklists and narrative drafts for review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute untrusted report data or remote third-party JavaScript while displaying sensitive business information.

Mitigation: Use only trusted enterprise data, avoid opening generated HTML from untrusted inputs, and HTML-escape user-provided fields before sensitive use.

Risk: The generated report depends on Chart.js loaded from a remote CDN.

Mitigation: Bundle Chart.js locally or use an integrity-pinned approved copy before using the report workflow for sensitive filings.

Risk: Generated filing material may contain outdated or incomplete policy guidance if official requirements change.

Mitigation: Review outputs against current MIIT and local filing notices, and have final submissions checked by responsible business or legal reviewers.

## Reference(s):

- [2026 SRDI policy reference](artifact/references/policy_2026.md)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/srdi-application)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown-style application drafts, plain text, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled generator can write an HTML report and a plain-text application draft from user-provided enterprise data.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
