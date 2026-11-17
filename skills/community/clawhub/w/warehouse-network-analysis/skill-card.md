## Description:

Analyzes customer store data against an existing warehouse and distribution network to support store distribution statistics, city positioning, delivery distance estimates, regional allocation, replenishment cycle planning, and trunk-line shipping plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinqianfei](https://clawhub.ai/user/jinqianfei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, logistics analysts, and operations planners use this skill to analyze Excel-based store distribution data and draft warehouse placement, delivery allocation, replenishment-cycle, and trunk-shipping recommendations. Recommendations should be reviewed against current operational constraints before business decisions are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Warehouse selection, coverage, replenishment, and trunk-shipping recommendations may be incomplete or misleading because the security review notes contradictory examples and a bundled script that implements only basic statistics and distance calculations.

Mitigation: Validate recommendations independently with operational warehouse data, route distance or traffic data, cost models, and planner review before using them for business decisions.

Risk: Straight-line delivery distances and simplified city coordinates may understate actual delivery time or cost.

Mitigation: Compare outputs with real route, service-level, and carrier data before finalizing network or cycle plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinqianfei/skills/warehouse-network-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; the bundled script emits console text from Excel input analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated Excel analysis workbooks when the full documented workflow is implemented by the agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
