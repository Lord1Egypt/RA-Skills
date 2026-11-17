## Description:

Xborder Ecom Guard checks Chinese cross-border e-commerce copy for six categories of US/EU compliance risk and returns severity-ranked remediation guidance before publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, e-commerce teams, and compliance reviewers use this skill to screen product details, ads, live-commerce scripts, shop descriptions, and customer-service copy aimed at US and EU markets before publishing.

### Deployment Geography for Use:

Global use for content aimed at United States and European Union markets

## Known Risks and Mitigations:

Risk: Users may treat heuristic flags as legal advice, certification, or a complete compliance determination.

Mitigation: Use the skill as pre-publication screening only; verify current US/EU obligations and obtain qualified review before relying on results in formal workflows.

Risk: Term-based Chinese-language checks can miss context, non-listed phrases, product-specific duties, or regulatory changes.

Mitigation: Supplement findings with current official requirements, platform policies, product documentation, and human compliance review.

Risk: The security guidance notes stray finance wording and a PRC-law disclaimer that may confuse a formal cross-border e-commerce workflow.

Mitigation: Review and align documentation and disclaimers with the intended workflow before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wwumit/skills/xborder-ecom-guard)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON risk findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local rule-based findings include decision, risk level, matched term, category, severity, character offsets, and remediation suggestion.]

## Skill Version(s):

1.0.0 (source: server release metadata, frontmatter, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
