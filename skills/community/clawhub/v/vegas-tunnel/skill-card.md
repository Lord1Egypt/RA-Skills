## Description:

维加斯通道交易 helps agents support A-share market analysis using Vegas tunnel concepts, EMA, Fibonacci retracement levels, resonance scoring, risk controls, and structured trading-signal guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for A-share technical-analysis workflows, including EMA calculations, Fibonacci levels, resonance scoring, trading-signal interpretation, and risk-control guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and market-data API access while execution boundaries are unclear.

Mitigation: Install with read-only or least-privilege API keys and allow only explicitly approved commands in a sandboxed agent environment.

Risk: Trading guidance or generated signals may be incorrect, incomplete, or unsuitable for live financial decisions.

Mitigation: Require human review and explicit confirmation before any live-trading, order-placement, or file-writing step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/vegas-tunnel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured JSON-style examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading-signal analysis, parameter suggestions, troubleshooting steps, and risk-control recommendations; require review before live trading.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
