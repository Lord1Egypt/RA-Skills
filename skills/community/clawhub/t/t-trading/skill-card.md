## Description:

T Trading is a Chinese-language prompt skill that guides agents to produce structured technical trading analysis for A-share and cryptocurrency markets using Vegas Tunnel EMA channels, Fibonacci levels, multi-timeframe scoring, and signal synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can load this skill when they want a Chinese-language assistant to answer explicit short-term market-analysis requests with a standardized technical-analysis report. It is intended for technical reference workflows and should not be treated as personalized financial advice or automated trading authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce entry, stop-loss, take-profit, and position-sizing language that users may mistake for personalized financial advice.

Mitigation: Present outputs as technical reference only, retain the artifact disclaimer, and require the user to make independent trading decisions.

Risk: Market analysis can be misleading if the agent lacks current prices, EMA values, Fibonacci anchors, or timeframe data.

Mitigation: Require current market data from the user or an independently verified data source before producing specific price-level guidance.

Risk: The security review notes no code execution or hidden data flow, but the prompt should only activate for explicit market-analysis requests.

Mitigation: Configure activation around clear trading-analysis intent and avoid using the skill for unrelated financial, legal, or personal-advice requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wscats/skills/t-trading)
- [Publisher Profile](https://clawhub.ai/user/wscats)
- [Artifact README](artifact/README.md)
- [Core Vegas Tunnel Resonance Skill](artifact/vegas-tunnel-resonance-skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown technical-analysis report with tables, scores, price levels, operation plan, risk notes, and disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include entry, stop-loss, take-profit, position-sizing, and observe-or-trade guidance; users should verify live market data independently.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
