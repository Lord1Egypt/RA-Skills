## Description:

Recommends TokenLab model IDs for specific workloads using public catalog, model contract, and pricing information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hedging8563](https://clawhub.ai/user/hedging8563)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other TokenLab users use this skill to shortlist models for chat, coding, media, retrieval, translation, and decision workloads, with exact IDs and fallback choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned, non-interactive installation command may install a changed source or CLI version.

Mitigation: Verify or pin the skills CLI and repository source before installing.

Risk: Catalog lookups contact TokenLab's public API, and private data in query parameters could be disclosed.

Mitigation: Avoid placing sensitive prompts or private data in catalog query parameters.

Risk: Model availability, pricing, and benchmark signals may change after a recommendation.

Mitigation: Recheck the current public catalog, contract, and pricing before selecting a model.

## Reference(s):

- [TokenLab Model Picker on ClawHub](https://clawhub.ai/hedging8563/skills/tokenlab-model-picker)
- [TokenLab public model catalog](https://api.tokenlab.sh/v1/models)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown shortlist table with a catalog command and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workload assumptions, exact model IDs, and fallback options.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
