## Description: <br>
Provides calibrated decision analysis using Charlie Munger-style mental models, inversion, incentive mapping, circle-of-competence checks, misjudgment audits, second-order effects, and forecast updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to structure high-stakes decisions, strategy reviews, investment cases, premortems, decision memos, incentive maps, and forecast registers. It is best suited for disciplined tradeoff analysis rather than simple factual lookup or professional legal, medical, financial, or market advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Python scripts read JSON inputs and may write output files when requested. <br>
Mitigation: Review JSON input files and any requested output path before allowing script execution. <br>
Risk: Decision analysis can become misleading when the question is underspecified or depends on stale, specialist, or time-sensitive facts. <br>
Mitigation: Clarify objectives, constraints, assumptions, and missing facts; use fresh evidence for time-sensitive claims. <br>
Risk: Legal, medical, financial, or market-sensitive topics may require professional judgment beyond the skill's framework. <br>
Mitigation: Use the skill for tradeoff framing and questions, and route professional advice or regulated decisions to qualified experts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/worldly-wisdom) <br>
- [Oracle Operating System](references/oracle-operating-system.md) <br>
- [Model Latticework](references/model-latticework.md) <br>
- [Misjudgment Playbook](references/misjudgment-playbook.md) <br>
- [Decision Checklists](references/decision-checklists.md) <br>
- [Use Cases and Examples](references/use-cases-and-examples.md) <br>
- [Evaluation Prompts](references/evaluation-prompts.md) <br>
- [Portability and Adaptation](references/portability-and-adaptation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown decision analysis, optional JSON calculator output, and optional shell commands for local scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured decision memos, premortems, forecast ledgers, incentive maps, weighted decision matrices, and scenario expected-value summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
