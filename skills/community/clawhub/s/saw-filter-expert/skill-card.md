## Description:

Provides Chinese-language technical support for SAW filter design, equivalent circuit modeling, transverse-mode suppression, temperature compensation, and material selection using Hashimoto's SAW text and related literature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujie19941118-star](https://clawhub.ai/user/lujie19941118-star)

### License/Terms of Use:

MIT-0

## Use Case:

RF filter engineers and developers use this skill to get Chinese-language design guidance, formulas, reference notes, and troubleshooting support for SAW filters, BVD/MBVD models, COM theory, piston-mode suppression, TCSAW/IHPSAW structures, and substrate selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may rely on a local SAW knowledge base path, so unintended documents in that path could affect answers.

Mitigation: Confirm that /workspace/knowledge_base/saw/docs/ contains only the technical documents intended for this skill before deployment.

Risk: The skill provides specialized RF filter design guidance that can be misapplied if the user's device context or assumptions are incomplete.

Mitigation: Review calculations, formulas, and material recommendations against project requirements and authoritative engineering references before implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lujie19941118-star/skills/saw-filter-expert)
- [Publisher profile](https://clawhub.ai/user/lujie19941118-star)
- [SAW filter reference notes](artifact/references/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown with formulas, tables, and technical recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference a local SAW knowledge base when available; no code execution or credential use is indicated by security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
