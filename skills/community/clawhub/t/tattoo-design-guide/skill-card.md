## Description:

AI纹身设计指南 helps agents collect tattoo preferences and produce Chinese-localized guidance on styles, body placement, artist selection, hygiene, aftercare, cover-ups, and interactive HTML consultation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistants use this skill to structure tattoo design consultations, compare styles and body placements, screen hygiene and aftercare considerations, and generate a Chinese-localized interactive HTML advisory report.

### Deployment Geography for Use:

Global, with China-localized pricing, legal, hygiene, and studio-selection assumptions.

## Known Risks and Mitigations:

Risk: Generated HTML reports can expose embedded personal consultation details to unverified third-party JavaScript.

Mitigation: Avoid sensitive medical, identity, or workplace details in generated reports, or bundle Chart.js locally with a restrictive CSP and SRI-protected assets.

Risk: Tattoo hygiene, contraindication, infection, and aftercare content may be mistaken for professional medical advice.

Mitigation: Use the skill as planning guidance only and consult qualified health professionals for infection, allergy, pregnancy, diabetes, immune-system, or wound-healing concerns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/tattoo-design-guide)
- [纹身风格百科全书](artifact/references/tattoo-styles.md)
- [身体部位纹身匹配指南](artifact/references/body-parts.md)
- [纹身卫生安全、护理与遮盖修改指南](artifact/references/safety-care.md)
- [Interactive report template](artifact/assets/report-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance and interactive HTML report code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Chart.js from a CDN unless the dependency is bundled locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
