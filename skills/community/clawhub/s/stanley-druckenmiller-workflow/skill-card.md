## Description:

Thesis-driven macro-to-execution market workflow in natural Chinese or English for A-share and U.S. equity morning briefs, intraday alerts, close reviews, weekly regime resets, and pre-trade sanity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckycatl](https://clawhub.ai/user/luckycatl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-focused agents use this skill to turn public macro, liquidity, rates, credit, FX, sector, and breadth evidence into concise market research memos with regimes, best expressions, position bias, kill-switches, and watchlists. It is intended for research framing and workflow standardization, not investment advice or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for investment advice or trading instructions.

Mitigation: Treat outputs as research framing only; the skill requires no explicit trade orders, human-owned execution decisions, and an investment-advice disclaimer.

Risk: Optional financial-data dependencies can introduce dependency-supply-chain or compatibility risk.

Mitigation: Use a virtual environment, pin finshare and akshare versions, and disable finshare with FINSHARE_MODE=off when it is not needed.

Risk: Public market data can be incomplete, stale, unavailable, or served through fallbacks and proxies.

Mitigation: Review evidence anchors, timestamps, field status labels, and DATA LIMITED downgrades before relying on the memo.

Risk: Setting FRED_API_KEY sends the configured API key to FRED's API.

Mitigation: Set FRED_API_KEY only when the user is comfortable using FRED's service, and omit it when public CSV fallback is sufficient.

Risk: Runtime snapshots are written to local storage.

Mitigation: Keep the default skill-local runtime directory or set STANLEY_RUNTIME_DIR to an explicit approved cache location.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luckycatl/skills/stanley-druckenmiller-workflow)
- [README](README.md)
- [Core Panels and Sources](references/core-panels-and-sources.md)
- [A-share Tape V1.1](references/a-share-tape-v1_1.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown narrative memos with optional shell commands, configuration snippets, and JSON data-panel files when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include evidence anchors, ISO8601 data timestamps, data-limited downgrades when coverage is incomplete, and a disclaimer that the content is research framework information rather than investment advice or trading instructions.]

## Skill Version(s):

1.1.11 (source: server release evidence and artifact published version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
