## Description:

Provides automated classification, severity rating, scoring, photo-evidence analysis, and report drafting for supplier on-site audit findings across multiple industry standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxp0125-rgb](https://clawhub.ai/user/mxp0125-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, supplier-management, and compliance teams use this Chinese-language skill to classify audit observations, assess severity, map issues to quality or regulatory frameworks, calculate scores, and draft supplier audit reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence identifies this as a very large Chinese-language quality and compliance reference skill with packaging hygiene issues.

Mitigation: Review the source before deployment, clean NUL bytes, remove the stray embedded Python fragment, and split the corpus into smaller reviewed modules for easier maintenance.

Risk: Audit, quality, and regulatory guidance can be market-specific and may change over time.

Mitigation: Validate generated findings, severity ratings, and report language against the current standards and local requirements that apply to the audited supplier.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mxp0125-rgb/skills/quality-director-skill)
- [APQP 产品质量先期策划快速参考指南](references/APQP-PPAP-quickref.md)
- [食品接触材料（FCM）合规快速参考指南](references/FCM-quickref.md)
- [FMEA 快速参考指南](references/FMEA-quickref.md)
- [SPC 统计过程控制快速参考指南](references/SPC-quickref.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown audit classifications, severity ratings, scoring guidance, photo-evidence summaries, and report drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided audit notes, supplier details, scoring data, and photos or photo descriptions when available.]

## Skill Version(s):

2.11.0 (source: release evidence and SKILL.md version line)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
