## Description:

Helps agents explain foundational financial chart reading and plotting, including chart types, time scales, arithmetic and logarithmic scales, volume, and open interest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to help an agent answer beginner chart-literacy questions for financial or futures markets, such as how to read or draw charts, choose time scales, select arithmetic or logarithmic scales, and interpret volume or open interest. It should not be used as authority for buy or sell decisions or pure fundamental analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat chart-literacy explanations as investment advice or automated trading authority.

Mitigation: Present outputs as educational chart-reading guidance and ask users to apply their own investment, legal, and compliance review before making financial decisions.

Risk: The skill boundaries exclude buy or sell decisions and pure fundamental analysis.

Mitigation: Redirect decision, trading-signal, or fundamental-analysis requests to a more appropriate skill or workflow instead of extending this skill beyond chart basics.

Risk: Long-term charts may be overused for precise trade timing.

Mitigation: Keep the skill's sequencing discipline: use monthly or weekly charts for broad direction and shorter time scales only when the user asks for timing context.

## Reference(s):

- [Server-resolved GitHub import source](https://github.com/bianchunhui/murphy-ta-skills/tree/main/ta-chart-basics)
- [ClawHub skill page](https://clawhub.ai/bianchunhui/skills/ta-chart-basics)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text explanations with structured steps when helpful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational chart-literacy guidance only; not investment advice or automated trading authority.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
