## Description:

Provides calibrated decision analysis using Charlie Munger-style multiple mental models, inversion, incentive mapping, circle-of-competence checks, misjudgment audits, second-order effects, and forecast updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to structure high-stakes decisions, investment cases, strategy reviews, premortems, incentive maps, and forecast registers with explicit assumptions, risks, confidence, and reversal conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision guidance can be misleading when legal, medical, financial, market, or other time-sensitive questions depend on fresh evidence or specialist judgment.

Mitigation: Require fresh evidence or specialist input for those decisions, and keep assumptions, uncertainty, and reversal conditions explicit.

Risk: Numeric helper outputs can be wrong or overtrusted if probabilities, weights, scores, or extreme values are malformed or poorly chosen.

Mitigation: Use clean JSON inputs, sanity-check probabilities and weights, inspect score ranges, and treat calculator results as advisory thinking aids.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tristanmanchester/skills/worldly-wisdom)
- [Decision Checklists](references/decision-checklists.md)
- [Evaluation Prompts](references/evaluation-prompts.md)
- [Misjudgment Playbook](references/misjudgment-playbook.md)
- [Model Latticework](references/model-latticework.md)
- [Oracle Operating System](references/oracle-operating-system.md)
- [Portability and Adaptation](references/portability-and-adaptation.md)
- [Use Cases and Examples](references/use-cases-and-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, text, JSON, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local templates and optional Python calculators for weighted decision matrices and expected-value scenarios.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
