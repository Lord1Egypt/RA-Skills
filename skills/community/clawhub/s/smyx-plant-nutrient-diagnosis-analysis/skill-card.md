## Description:

Analyzes plant leaf images for visual nutrient deficiency symptoms and returns likely deficient nutrients with confidence scores and general fertilization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Home gardeners, greenhouse growers, and plant-factory operators use the skill to examine leaf images for possible nutrient deficiencies, review likely nutrients and confidence scores, and get general fertilization guidance. Treat results as advisory and consult an agricultural specialist for precise fertilizer amounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create an account and handle a token.

Mitigation: Use it only if you are comfortable with the reported account and token handling.

Risk: Images or videos may be processed by an external service.

Mitigation: Submit media only when you are comfortable with external processing.

Risk: The export-only option may still trigger analysis.

Mitigation: Do not rely on export-only mode to prevent analysis; avoid using it when you do not want analysis to run.

Risk: The available security assessment is incomplete because a local reference was missing.

Mitigation: Review the skill and its associated references before installation.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-nutrient-diagnosis-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured diagnosis report with likely nutrient deficiencies, confidence information, guidance, and report links; history results may be presented in a Markdown table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory results; does not provide fertilizer concentrations or quantities. Similar symptoms and multiple deficiencies can make diagnosis uncertain.]

## Skill Version(s):

1.0.18 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
