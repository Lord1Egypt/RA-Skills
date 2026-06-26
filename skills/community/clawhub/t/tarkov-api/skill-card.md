## Description: <br>
Security-focused Tarkov.dev and optional EFT Wiki operations for hardcore Escape from Tarkov players who need reliable game-data lookups, stash valuation snapshots, trader flip detection, and map-risk or raid-kit recommendations with controlled wiki validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cole-Z](https://clawhub.ai/user/Cole-Z) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External players and agent users use this skill to query Tarkov.dev data, optionally validate selected details against the EFT Wiki, and turn game data into raid, market, task, stash, and kit decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to game-data and wiki endpoints. <br>
Mitigation: Use the default Tarkov.dev and official EFT Wiki endpoints, keep wiki checks conditional, and disclose uncertainty when data is patch-sensitive. <br>
Risk: Raw query mode, query files, custom endpoints, or --allow-unsafe-endpoint can expand the request scope. <br>
Mitigation: Prefer preset commands; use raw mode or custom endpoints only after reviewing the query and trusting the destination. <br>
Risk: Local stash JSON or CSV files are user-directed inputs. <br>
Mitigation: Provide only minimal files intended for valuation and avoid including unrelated personal or sensitive data. <br>
Risk: Market prices, spawn chances, wiki edits, and flip or risk scores can drift or be heuristic. <br>
Mitigation: Treat outputs as snapshots, cross-check unusual values, and verify important decisions in game after patches. <br>


## Reference(s): <br>
- [Query Cookbook](references/query-cookbook.md) <br>
- [Security Model](references/security-model.md) <br>
- [Tarkov.dev GraphQL API](https://api.tarkov.dev/graphql) <br>
- [Escape from Tarkov Wiki](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki) <br>
- [ClawHub skill page](https://clawhub.ai/Cole-Z/tarkov-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should lead with an actionable summary, then cite key API values and risk notes for volatility, spawn uncertainty, or version drift.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
