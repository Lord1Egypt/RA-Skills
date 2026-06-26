## Description: <br>
Thesis-driven macro-to-execution market workflow in natural Chinese or English. Generate A-share and U.S. equity Morning Briefs, Intraday Alerts, Close Reviews, Weekly Regime Resets, and pre-trade sanity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckycatl](https://clawhub.ai/user/luckycatl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market analysts use this skill to produce public-data macro and equity-market research memos for A-share and U.S. equity workflows. It helps translate liquidity, rates, credit, FX, internal structure, sector expression, and fundamentals into regime, best-expression, position-bias, kill-switch, and watchlist language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public market data from third-party sources may be stale, unavailable, incomplete, or cached. <br>
Mitigation: Review data timestamps, evidence anchors, missing-evidence labels, and DATA LIMITED downgrades before relying on the analysis. <br>
Risk: Market research output may be mistaken for investment advice or automated trading instructions. <br>
Mitigation: Treat outputs as research context only; keep exact asset choice, entry, stop, target, size, and risk budget under human control. <br>
Risk: The helper can fetch public financial data, optionally read a FRED-specific API key, and store local market-data cache files. <br>
Mitigation: Install only if those behaviors are acceptable, use a purpose-specific FRED API key when needed, and set an explicit runtime/cache directory if the default skill-local cache is not appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luckycatl/stanley-druckenmiller-workflow) <br>
- [Core Panels and Sources](references/core-panels-and-sources.md) <br>
- [A-share Tape V1.1](references/a-share-tape-v1_1.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown narrative memos, alerts, reviews, and sanity checks with occasional shell commands for optional data-panel setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are decision-oriented research context with evidence anchors, timestamps, falsification conditions, and explicit data-limited downgrades when evidence is incomplete.] <br>

## Skill Version(s): <br>
1.1.11 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
