## Description:

Provides a Chinese-language framework for evaluating US tech stock, long-call, allocation, and buy-the-dip decisions through a quality-growth, patience-first investing lens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ting2tao](https://clawhub.ai/user/ting2tao)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to produce concise market commentary and position-framing guidance for US technology stocks, M7 rotation, AI infrastructure names, and long-call versus underlying-stock decisions. It is best suited for informational analysis that still requires independent suitability, price, and risk checks before any financial action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce broad actionable leveraged-trading guidance without enough risk and suitability guardrails.

Mitigation: Treat outputs as informational market analysis only, and independently check current prices, risk tolerance, time horizon, options experience, and position size before acting.

Risk: Long-call strategies can lose value quickly and may be inappropriate for users without options experience or a suitable time horizon.

Mitigation: Require explicit risk framing, avoid precise strike or expiration claims without option-chain data, and prefer staged sizing over concentrated leveraged exposure.

Risk: The README includes an unpinned npx installation example.

Mitigation: Prefer a pinned and verified install command before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ting2tao/skills/value-nvest-perspective)
- [Source Map](references/research/01-source-map.md)
- [Market Lens](references/research/02-market-lens.md)
- [Options Playbook](references/research/03-options-playbook.md)
- [Risk And Positioning](references/research/04-risk-and-positioning.md)
- [Expression DNA](references/research/05-expression-dna.md)
- [Boundaries And Open Questions](references/research/06-boundaries-and-open-questions.md)
- [Captured Longbridge Sources](references/sources/captured-links.md)
- [ValueNvest Longbridge Profile](https://longbridge.com/zh-CN/profiles/14581970/original)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text market commentary with concise recommendations and conditional risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current market and macro data checks before producing ticker-specific guidance; does not provide precise option strikes, expirations, or personalized financial advice.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
