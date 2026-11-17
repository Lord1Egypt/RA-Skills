## Description:

Quant Trading CN helps agents generate, review, and improve quantitative trading systems for Indian equity markets, with Zerodha workflows and China A-share adaptation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

External developers and trading-system builders use this skill to draft, review, and improve quantitative trading code, backtests, stock-universe workflows, and risk controls for Indian equity-market strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading guidance may affect real broker positions, including closing positions, canceling orders, or placing trades without enough safeguards.

Mitigation: Keep use to paper trading or read-only analysis unless explicit live-trading opt-in, dry-run previews, confirmation gates, order ownership checks, and strict trading limits are added.

Risk: Broker credentials and account access can expose real funds.

Mitigation: Store credentials outside prompts and repositories, use least-privilege or read-only access where possible, and review any generated code before connecting it to a live broker account.

Risk: Backtest results and strategy claims may not match live market performance.

Mitigation: Validate with backtest-live parity checks, paper trading, conservative position sizing, stop-loss controls, and independent review before risking capital.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/skills/quant-trading-cn)
- [AlgoTrader Reference README](artifact/references/README_en.md)
- [Trading Knowledge Base](artifact/references/KNOWLEDGE_en.md)
- [Trading Nuances and Precautions](artifact/references/NUANCES_en.md)
- [Zerodha Kite API](https://kite.trade/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce trading-system scaffolding, code review findings, backtest analysis, and broker workflow recommendations; ClawHub metadata lists python3 as a required binary.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
