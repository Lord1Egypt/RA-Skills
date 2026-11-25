## Description:

AI-powered pet grooming effect assessment detects mat residue area, dandruff coverage, and coat smoothness from post-grooming images, then outputs a 0–100 grooming score and targeted re-grooming suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and grooming professionals can review post-grooming cat or dog images and videos for visible mat residue, dandruff, and coat smoothness, then receive an assessment score and follow-up grooming suggestions. The skill also supports looking up previous reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet images, videos, or supplied URLs may be processed by an external service.

Mitigation: Before submitting media, confirm which service receives it and how it is handled; avoid sending sensitive media or untrusted URLs until clarified.

Risk: Account creation, token storage, and report-history access are flagged for clarification.

Mitigation: Review the identity and credential handling and the permissions used for report access before installation; avoid using sensitive accounts until these details are clear.

Risk: The purpose and effects of the export-only behavior are unclear.

Mitigation: Clarify what the export-only option does before running it, and avoid invoking it until its behavior is documented.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-grooming-effect-assessment-analysis)
- [API reference](references/api_doc.md)
- [Analysis API reference](skills/smyx_analysis/references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [Structured grooming assessment reports with findings, a 0–100 score, suggestions, and report links; history results may be returned as JSON or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual grooming assessment only; not a medical diagnosis or treatment recommendation.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
