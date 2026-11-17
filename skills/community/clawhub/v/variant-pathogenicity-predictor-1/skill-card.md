## Description:

Integrate REVEL, CADD, PolyPhen scores to predict variant pathogenicity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and genomics analysts use this skill to run a bounded pathogenicity scoring workflow that combines REVEL, CADD, and PolyPhen-style inputs into a classification and score breakdown. Its outputs should be reviewed as rough research heuristics, not clinical or diagnostic interpretations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents medically meaningful pathogenicity labels from a simple heuristic with unsupported capability claims.

Mitigation: Treat results as rough research heuristics only; require domain validation, explicit medical disclaimers, and documented data sources before any clinical or diagnostic use.

Risk: Weak input handling may make variant or file-based results unreliable when inputs are incomplete, malformed, or outside the documented score assumptions.

Mitigation: Validate input formats and score ranges before execution, review generated classifications manually, and report missing or unsupported evidence instead of relying on defaults.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or terminal text with score summaries and execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pathogenicity classification, composite score, individual score breakdown, assumptions, risks, and validation needs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
