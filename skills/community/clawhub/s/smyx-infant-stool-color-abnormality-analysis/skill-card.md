## Description:

Analyzes images of infant stool to classify visible color patterns and provide directional risk alerts and next-step guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and pediatric care teams can use the skill to review infant diaper or stool images for visible color categories and receive structured screening results with suggested next steps. Results are visual guidance and do not provide a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious by ClawScan, which reports undeclared account, identity, and token handling, privacy risks around remote media analysis, and behavior that may not match the stated purpose.

Mitigation: Review whether account, identity, credential, and remote media handling are expected before use; only run it when those behaviors are understood and acceptable.

Risk: Security scanning was partial because a local reference was missing, so the available results do not establish that every referenced component was assessed.

Mitigation: Review the missing reference and relevant components before relying on the scan as a complete assessment.

Risk: Infant diaper and stool images are sensitive, and color assessment can be affected by lighting; results are not a medical diagnosis.

Mitigation: Obtain a guardian's informed consent before sharing images, use neutral white lighting, and seek pediatric care for concerning results rather than relying on the screening alone.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-stool-color-abnormality-analysis)
- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON screening report with color category, risk level, confidence, recommended action, and alert text; Markdown table for history results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image and lighting quality indicators and a report link when available.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
