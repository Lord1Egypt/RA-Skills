## Description: <br>
Provides StockToday market data tools for A-share, Hong Kong, U.S. equities, funds, futures, options, bonds, macro data, and related analysis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[usa2046](https://clawhub.ai/user/usa2046) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and AI agents use this skill to retrieve StockToday market, financial, fund, futures, options, bond, macro, Hong Kong, and U.S. market data, then produce concise summaries, comparisons, exports, or reusable analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API tokens and the security scan reports unsafe token-handling patterns. <br>
Mitigation: Use the least-privileged StockToday token that supports the needed interfaces, rotate exposed tokens, and review token-related behavior before installing. <br>
Risk: The release evidence reports credential-like admin details in documentation. <br>
Mitigation: Treat disclosed credential-like values as compromised, rotate them before relying on the release, and avoid granting administrative credentials to agent workflows. <br>
Risk: The security guidance calls out plaintext backup URLs. <br>
Mitigation: Prefer HTTPS service endpoints and override or disable plaintext backup URLs where deployment policy requires encrypted transport. <br>
Risk: The skill depends on the StockToday service and publisher for market data access. <br>
Mitigation: Install only when the StockToday service and publisher are trusted, and verify important financial outputs against authoritative market data before using them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/usa2046/stocktoday-skill) <br>
- [Publisher profile](https://clawhub.ai/user/usa2046) <br>
- [StockToday token application](https://stocktoday.cn) <br>
- [Interface schema documentation](https://github.com/stocktoday/stocktoday-skill/blob/main/INTERFACE.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact installation guide](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, compact tables, JSON tool data, shell commands, configuration snippets, and optional CSV, parquet, or Python script outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state data scope, source, date handling, missing-data caveats, and any local file paths produced.] <br>

## Skill Version(s): <br>
1.3.11 (source: server release metadata; artifact/package.json and artifact/_meta.json agree) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
