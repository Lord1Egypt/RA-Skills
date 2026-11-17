## Description:

Rubicon Sentinel v2 is an opinionated geopolitical analysis skill that uses web research to produce eight-pillar sovereignty scans, forecasts, comparisons, claim rebuttals, short social posts, and optional meme prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgmnemesis](https://clawhub.ai/user/lgmnemesis)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to generate sourced geopolitical sovereignty briefings, country comparisons, forecasts, and short-form summaries from current web results using its eight-pillar rubric.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents politically loaded sovereignty scores and framing that can appear more objective than the underlying rubric supports.

Mitigation: Label outputs as opinionated analysis, require citations for factual claims, and review scores before relying on them for decisions.

Risk: Optional Twitter/API use, memory use, image generation, and arbitrary web fetching can expand data exposure or produce unexpected external interactions.

Mitigation: Require user confirmation before enabling Twitter/API access, persistent memory, image generation, or fetching arbitrary pages.

Risk: Current-event claims, social sentiment, and quote selections may become outdated or insufficiently sourced.

Mitigation: Prefer recent sources, show source URLs for deep scans, and distinguish artifact-provided quotes from independently verified public records.

## Reference(s):

- [Rubicon Sentinel v2 ClawHub Skill Page](https://clawhub.ai/lgmnemesis/skills/rubicon)
- [Scoring Rubric](artifact/references/scoring.md)
- [Smart Query Templates](artifact/references/queries.md)
- [Quote Library](artifact/references/quotes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown briefings, tables, source lists, forecasts, rebuttals, tweet drafts, and text meme prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scans depend on current web evidence; deep scans may include full source URLs, and meme mode may produce image prompts when image generation is available.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
