## Description:

Supports clinical trial data statistics for pharmaceutical research by computing descriptive endpoint summaries, group comparisons, and AI-assisted interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical analytics teams use this skill to prepare clinical trial records, calculate per-group descriptive statistics for endpoint fields, and generate a Markdown interpretation for review. It is intended as analysis support and does not replace a statistical analysis plan, registered statistician review, or regulatory submission analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trial-derived data is sent to a remote medical-model endpoint for interpretation.

Mitigation: Use only when authorized to transmit the data, minimize or de-identify sensitive trial records before use, and trust the endpoint and credential handling.

Risk: AI-generated clinical interpretation may be incomplete or misleading for regulated clinical decisions.

Mitigation: Have a qualified statistician review the generated interpretation and rely on approved statistical analysis plans for formal analyses.

Risk: Office, PDF, and image inputs require optional parsers or external tools and may expand the processing surface for untrusted files.

Mitigation: Prefer JSON, CSV, or XLSX inputs from trusted sources and run preprocessing in a contained environment when handling documents or images.

Risk: The skill can fall back to an external shared preprocessor when local preprocessing fails.

Mitigation: Review the runtime environment and available shared preprocessor before deployment, or disable unsupported input types.

## Reference(s):

- [Source reference: Statistical Analysis skill](https://agent-skills.md/skills/Jst-Well-Dan/Skill-Box/statistical-analysis)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Analysis, Files]

**Output Format:** [UTF-8 JSON containing structured statistics data and Markdown natural-language interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an app key for a remote medical model endpoint; optional preprocessing supports JSON, CSV, XLSX, XLS, TXT, Markdown, PDF, DOC, DOCX, and image inputs when dependencies are available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
