## Description:

Build a cost-efficient LLM evaluation ensemble with sampling, tiebreakers, and deterministic validators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:


## Use Case:

Developers and evaluation engineers use this skill to design LLM-as-judge workflows for comparing generative AI outputs at scale with deterministic validators, heuristic scoring, sampled judges, and tiebreakers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sampled evaluation artifacts may be sent to external Anthropic or OpenAI judge models.

Mitigation: Use the skill only when external judge API calls are acceptable, and redact sensitive prompts, customer data, source text, ground truth, and model outputs before judging.

Risk: Raw judge responses may retain sensitive evaluation content in logs.

Mitigation: Avoid storing raw judge responses unless necessary, and apply the same retention and access controls used for sensitive evaluation data.

Risk: Judge disagreement or model-version drift can affect evaluation decisions.

Mitigation: Calibrate judge scores against manual review, pin judge model versions, and use tiebreakers or full judging coverage for promotion gates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/reddi-llm-judge)
- [Publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scoring dimensions, sampling guidance, tiebreaker guidance, and environment prerequisites.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
