## Description: <br>
Scans stock universes with technical pattern detectors such as cup-with-handle, VCP, high-tight flag, three-weeks-tight, and NR7, then calibrates scores and ranks candidates by confidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to screen market universes, draft ZVT-based quant strategy or backtest workflows, and inspect pattern-driven scan results. It is best used with human review before any credentialed, write-capable, or trading-adjacent action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a stock-pattern screener, but the security summary says its instructions also cover broader server, authentication, social-session, database, MCP, and write-capable finance workflows. <br>
Mitigation: Install only when that broader finance automation scope is intended, keep execution sandboxed, and require explicit approval before migrations, resets, watchlist writes, MCP actions, or order-related workflows. <br>
Risk: The capability metadata flags use cases that may require sensitive credentials, including broker, paid-provider, social-media, or server credentials. <br>
Mitigation: Grant credentials only after reviewing the exact flow, use least-privilege secrets, and avoid sharing broker or paid-provider credentials for exploratory screening. <br>
Risk: Generated finance code or backtest workflows can produce misleading results if market rules, data quality, or execution constraints are not reviewed. <br>
Mitigation: Validate outputs against the semantic locks and preconditions, especially next-bar execution, no look-ahead behavior, T+1 A-share rules, and data availability checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/stock-pattern-screener) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for target market, data provider, strategy type, date range, and entity IDs before producing executable guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
