## Description:

Ptengine Heatmap Analyze helps agents fetch Ptengine heatmap metrics through the user-installed ptengine-cli tool and produce CRO behavior analysis reports using a four-stage psychology model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaichen](https://clawhub.ai/user/zhaichen)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing practitioners, CRO specialists, and site operators use this skill to analyze Ptengine heatmap data, compare audience segments, validate A/B tests, evaluate ad channels, and identify conversion barriers or opportunities on webpages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ptengine API credentials are required for the external ptengine-cli tool.

Mitigation: Configure ptengine-cli in a trusted terminal instead of pasting API keys into chat, and use the CLI's masked configuration display for checks.

Risk: Shell-style ptengine-cli command templates include user-provided URL, date range, filter, and profile inputs.

Mitigation: Validate parameters and invoke ptengine-cli without shell interpolation before operational use.

Risk: Attacker-supplied URLs could lead to misleading or unsafe analysis requests.

Mitigation: Use the skill on trusted or owned URLs and keep data collection bounded to Ptengine CLI results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaichen/skills/ptengine-heatmap-analyze)
- [ptengine-cli upstream repository](https://github.com/Kocoro-lab/ptengine-cli)
- [ptengine-cli releases](https://github.com/Kocoro-lab/ptengine-cli/releases)
- [ptengine-cli command reference](references/ptengine-cli.md)
- [Data transformation reference](references/data-transform.md)
- [Page classification](references/page-classification.md)
- [Block content analysis and stage classification](references/block-analysis.md)
- [Quality constraints](references/quality-constraints.md)
- [Single page analysis task](references/single-page-task.md)
- [Compare task](references/compare-task.md)
- [A/B test task](references/ab-test-task.md)
- [Ad performance analysis](references/ad-performance.md)
- [Audience analysis](references/audience-analysis.md)
- [Page type interpretation guide](references/page-types.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Human-readable Markdown report with inline ptengine-cli commands and JSON-oriented data handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-installed ptengine-cli and user-configured Ptengine credentials; analysis should use Ptengine CLI data only.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
