## Description:

Analyzes retail store assortment performance from pallet and display perspectives, including intent-generating SKUs, trial depth, customer intent dispersion, and conversion efficiency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operators and analysts use this skill to compare display, behavior, and customer funnels for a store over a selected date range. It produces diagnostic findings and action guidance for assortment attractiveness, trial depth, customer intent concentration, and conversion efficiency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill loads unreviewed local code from a hardcoded personal workspace path before running.

Mitigation: Replace the local path dependency with a packaged, pinned, reviewable API client, or run only in an environment where that path is strictly controlled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gwyang7/skills/retail-store-assortment-analysis)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain-text analysis report with structured Chinese sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires store ID, date range, and optional store name; calls the store dashboard BI endpoint through a local API client.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
