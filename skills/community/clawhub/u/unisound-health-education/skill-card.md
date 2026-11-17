## Description:

Patient-facing health education skill that matches health topics and keywords to provided article content, then uses a remote medical model to produce Markdown summaries with source references and a medical disclaimer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External patient-facing applications and developers use this skill to turn a health topic, keywords, and article list into general health education summaries. It is limited to education and source-oriented summaries, not diagnosis or individualized treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health-related topics and matched article content are sent to a fixed remote model API.

Mitigation: Use only when that data sharing is acceptable, avoid sensitive patient information unless separately approved, and disclose remote processing in the deployment context.

Risk: The required API key can be exposed through shell history or process logs when passed directly on the command line.

Mitigation: Protect the key outside shell history and logs, rotate it if exposed, and prefer a secret-management mechanism in production wrappers.

Risk: Document parsing handles multiple file formats and may invoke local converters or OCR tools.

Mitigation: Run preprocessing in a constrained environment and process only trusted or scanned files.

Risk: The script can fall back to external shared Python code outside the skill package.

Mitigation: Remove the fallback or integrity-pin and review the shared module before using the skill in production or with sensitive patient information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/unisound-llm/skills/unisound-health-education)
- [WellAlly health skill reference](https://agent-skills.md/skills/huifer/WellAlly-health/wellally-tech)
- [Remote medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [UTF-8 JSON with structured data and a Markdown text field]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes matched articles, source URLs when present, and a disclaimer that education content does not replace clinical care.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
