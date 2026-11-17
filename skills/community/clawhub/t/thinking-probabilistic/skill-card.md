## Description:

Use when forecasting, estimating, or sizing risk: anchor on base rates, give ranges, update prior to likelihood to posterior on evidence, and factor unmeasured quantities into order-of-magnitude bounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and other agent users apply this skill when they need calibrated forecasts, uncertainty ranges, risk sizing, or order-of-magnitude estimates instead of unsupported single-point guesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make uncertain estimates look more structured than the available evidence supports.

Mitigation: Ask the agent to name the base rate, assumptions, uncertainty range, and falsifying observation, and treat unsupported estimates as guesses.

Risk: The skill can encourage probabilistic framing for facts that are directly measurable or look-up-able.

Mitigation: Verify checkable facts against real measurements or authoritative sources before relying on an estimate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-probabilistic)
- [Publisher profile](https://clawhub.ai/user/tjboudreaux)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text with claims, priors, ranges, updates, Fermi bounds when used, and decision implications.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reasoning guidance only; it does not add executable code, tool access, or system actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
