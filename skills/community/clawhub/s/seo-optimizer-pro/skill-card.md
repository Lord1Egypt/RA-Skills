## Description:

SEO Optimizer Pro analyzes HTML or plain text for readability, keyword density, technical SEO structure, and AI search optimization, then generates model-backed recommendations through the user's chosen AI provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vedantsingh60](https://clawhub.ai/user/vedantsingh60)

### License/Terms of Use:

MIT-0

## Use Case:

Content marketers, SEO professionals, documentation teams, and ecommerce publishers use this skill to audit existing content and generate SEO and AEO recommendations for search ranking and AI-answer visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analyzed content excerpts are sent to the selected third-party AI provider, and the artifact contains conflicting privacy statements.

Mitigation: Use non-sensitive content unless the privacy wording is corrected and the selected provider's data handling terms have been reviewed.

Risk: Installing every listed provider SDK increases dependency surface beyond what most users need.

Mitigation: Install only the SDK required for the chosen model provider.

Risk: SEO and AEO recommendations may be inaccurate or may not improve rankings.

Mitigation: Review recommendations before publishing and validate changes against the user's SEO strategy and analytics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vedantsingh60/skills/seo-optimizer-pro)
- [Publisher profile](https://clawhub.ai/user/vedantsingh60)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown-style text reports and structured Python or JSON-compatible analysis objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses content excerpts with the selected AI provider and returns SEO metrics, optimization suggestions, AEO recommendations, and estimated impact.]

## Skill Version(s):

1.0.8 (source: server release metadata, manifest.yaml, seo_optimizer.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
