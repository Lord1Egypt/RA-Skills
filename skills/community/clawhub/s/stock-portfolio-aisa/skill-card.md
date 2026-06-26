## Description: <br>
Create and manage stock and crypto portfolios with live AISA pricing and profit-and-loss tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, update, list, rename, delete, and review local stock or crypto portfolios with live AISA price lookups and current P&L calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings and P&L data may be sensitive and are stored locally in a mismatched stock-analysis state namespace. <br>
Mitigation: Use a dedicated state directory with CLAWDBOT_STATE_DIR, limit access to the local state file, and consider moving data to a stock-portfolio-specific path before relying on it. <br>
Risk: Portfolio deletion is immediate and not recoverable from this skill. <br>
Mitigation: Only run delete actions after an explicit user request and keep a backup of the local portfolios JSON when the data matters. <br>
Risk: The skill requires an AISA API key and allows overriding the AISA base URL. <br>
Mitigation: Use a dedicated AISA API key, avoid sharing it in prompts or logs, and do not override AISA_BASE_URL unless the endpoint is trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/stock-portfolio-aisa) <br>
- [AISA API Endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Plain-text CLI output with portfolio summaries, P&L tables, setup commands, and local JSON state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; portfolio data is stored locally unless CLAWDBOT_STATE_DIR is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
