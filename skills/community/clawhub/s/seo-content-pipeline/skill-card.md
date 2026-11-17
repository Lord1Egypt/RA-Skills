## Description:

SEO automated content pipeline skill. Automates the entire workflow from competitor research and keyword mining to article generation and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External SEO content strategists use this skill to move from product and audience inputs through competitor analysis, keyword research, topic planning, article drafting, and CMS publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SEO content may contain factual errors, misleading claims, or off-brand language.

Mitigation: Manually review article drafts for accuracy, brand fit, and source quality before publishing.

Risk: The workflow can auto-publish to a CMS without a clear approval gate.

Mitigation: Run in draft-only mode or require explicit approval before CMS writes, and use scoped CMS credentials.

Risk: High publishing frequency or keyword stuffing may create spam risk.

Mitigation: Control daily publishing volume and keep keyword usage natural according to the artifact's SEO guidance.

## Reference(s):

- [SEO Data Models and Output Formats](references/schemas.md)
- [SEO Content Template Reference](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [JSON topic lists and Markdown article drafts, with CMS publishing guidance or actions when configured]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires product and target customer inputs; generated content should be reviewed before publishing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
