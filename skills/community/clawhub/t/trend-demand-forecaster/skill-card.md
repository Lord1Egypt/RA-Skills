## Description: <br>
Turns sales notes, trend signals, seasonal context, promo plans, and inventory constraints into a practical demand forecast brief for planners, ecommerce operators, founders, and consultants working without live ERP, BI, ads, or marketplace APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External planners, ecommerce operators, founders, and consultants use this skill to turn rough demand signals and planning constraints into a markdown forecast brief with base, upside, and downside scenarios. It is best suited for short-term replenishment, promo lift, recovery, slowdown, and seasonal planning where a human will review the assumptions before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the forecast brief as guaranteed or live-data backed even though the skill is heuristic. <br>
Mitigation: Keep the no-live-data and heuristic caveats visible, validate assumptions against source data, and require human approval before inventory, budget, or purchase decisions. <br>
Risk: Examples reference outside trend and marketplace tools, which can blur the boundary between optional research inputs and data the skill actually fetches. <br>
Mitigation: Treat those tools as optional user-supplied research sources and do not claim the skill accessed external feeds unless the user provides the data. <br>
Risk: Promo distortion, stockouts, weak data quality, or seasonality shifts can make recent demand signals misleading. <br>
Mitigation: Separate distorted periods from baseline demand, downgrade confidence when inputs are thin, and monitor leading indicators before scaling commitments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/trend-demand-forecaster) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown forecast brief] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a demand narrative, scenario view, leading indicators, inventory and commercial implications, risk watchlist, assumptions, confidence notes, and limits.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub server release metadata; artifact frontmatter reports v1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
