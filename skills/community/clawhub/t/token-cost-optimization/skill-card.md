## Description:

Helps estimate and reduce API token costs with a calculator, prompt compression, cache reuse, model routing, configuration guidance, and quantified savings examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to estimate model API costs and plan phased token-reduction work across prompt compression, caching, and model routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caching user documents, source code, contracts, or customer data can expose private or regulated information if implemented without safeguards.

Mitigation: Require explicit consent, minimize or redact stored content, apply access controls, define retention limits, and provide a deletion path before enabling document or vector-database caching.

Risk: Over-compression, overly low token limits, or one-size-fits-all model downgrades can reduce answer quality or cause incomplete outputs.

Mitigation: Measure a baseline, validate each optimization phase, keep task-appropriate token buffers, and use fallback routing when cheaper models do not meet quality requirements.

## Reference(s):

- [Three-Tier Optimization Strategies Explained](references/tier-strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python snippets; the calculator prints terminal cost estimates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estimated monthly before/after costs and savings percentages based on user-entered usage assumptions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
