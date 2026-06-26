## Description: <br>
This skill applies a deterministic, bilingual value-investing framework to user-provided US stock financial data and produces an A/B/C/D investment rating with rule-level reasons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyfree](https://clawhub.ai/user/spyfree) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Investors, analysts, and agent workflows use this skill to evaluate structured US stock financial inputs against explicit quality, leverage, cash-conversion, and moat rules. It is intended to support research and review rather than replace independent investment judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stock ratings could be treated as definitive investment advice. <br>
Mitigation: Use the ratings as analytical support and review the reasoning before making any investment decision. <br>
Risk: Incorrect or stale financial inputs can produce misleading valuation results. <br>
Mitigation: Verify the source financial data, JSON fields, and output paths before running the evaluator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spyfree/us-value-investing-framework) <br>
- [Framework guide](references/framework-guide.md) <br>
- [Input template](references/input-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [JSON result files and Markdown summaries with English reasons and a Chinese summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic local evaluation of user-provided financial data; no network access is described.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
