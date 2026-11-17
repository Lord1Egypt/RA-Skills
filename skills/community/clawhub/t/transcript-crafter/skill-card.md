## Description:

Transforms interview or meeting transcripts into WeChat-ready long-form articles through structured extraction, persona selection, outline planning, web research, fact-checking, and Markdown rewriting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and content teams use this skill to turn transcripts into source-aware Chinese WeChat articles with clear speaker attribution, added context, and publication-oriented formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may process confidential interviews, meeting notes, personal data, or unpublished business material.

Mitigation: Review inputs before use and avoid sensitive material unless the user is comfortable with web research, local output files, and possible cloud upload.

Risk: Transcript-derived output may be copied to the Desktop or uploaded to Feishu cloud storage under the user's account without clear per-run consent.

Mitigation: Explicitly decline Feishu upload for sensitive work and confirm file destinations before delivery.

Risk: The workflow performs web research and fact-checking, so sourced claims can be wrong or weakly supported.

Mitigation: Verify cited claims, use the source-quality gate, and pay extra attention to preprints and other lower-confidence sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/transcript-crafter)
- [Source Quality Gate](references/source-quality-gate.md)
- [Pipeline Detail](references/pipeline-detail.md)
- [Extraction Guide](references/extraction-guide.md)
- [Fact-Check Guide](references/fact-check-guide.md)
- [Tool Router](references/tool-router.md)
- [WeChat Format Guide](references/wechat-format-guide.md)
- [Title Strategist](references/title-strategist.md)
- [Interview Personas](references/interview-personas.yaml)
- [Quality Checklist](references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown articles, structured extraction notes, source-check tables, and delivery paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final articles are intended for WeChat/rico-md formatting and may be saved locally or uploaded to Feishu when enabled.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
