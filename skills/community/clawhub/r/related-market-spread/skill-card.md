## Description: <br>
Use when two Polymarket markets imply different probabilities for a linked outcome. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-strategy researchers use this skill to compare linked Polymarket markets, identify relative-value spreads, and shape a backtested NautilusTrader strategy archetype before any reviewed deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide financial trading strategy development, including live-trading decisions if the user applies its output directly. <br>
Mitigation: Use it for research or backtesting unless live trading is explicitly authorized, and review generated trading code and order sizes before deployment. <br>
Risk: Linked markets may have different resolution logic or outcome mappings, making an apparent spread structural rather than an inefficiency. <br>
Mitigation: Verify exact market slugs and compare resolution rules before treating a spread as actionable. <br>
Risk: Filled TradeTick backtests cannot guarantee simultaneous fills or cross-book liquidity for both legs. <br>
Mitigation: Check current liquidity, stale-state handling, and entry or exit feasibility before deploying any two-leg strategy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superior-ai/related-market-spread) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with JSON configuration examples and strategy guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review generated strategy code, market comparability, liquidity assumptions, and order sizes before deployment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
