## Description: <br>
Monitors Simmer positions for resolved Polymarket outcomes, updates trade journals, sends Discord alerts, and redeems winning positions on-chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DjDyll](https://clawhub.ai/user/DjDyll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators running Simmer agents use this skill to monitor resolved Polymarket positions, record outcomes and PnL, notify private Discord destinations, and redeem winning positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform recurring live wallet transactions using local credentials. <br>
Mitigation: Run POLY_MODE=sim before live use, review the planned behavior, and use a dedicated low-balance wallet. <br>
Risk: Local environment loading can pick up credentials from .env files. <br>
Mitigation: Review or remove implicit .env loading and keep wallet and API credentials scoped to this skill's runtime. <br>
Risk: Bundled and generated state files influence what resolutions and redemptions are considered already processed. <br>
Mitigation: Inspect bundled state files before first run and keep DATA_DIR in an app-owned directory. <br>
Risk: Discord webhook notifications may expose trading outcomes or PnL to the configured destination. <br>
Mitigation: Use Discord webhooks only for private destinations that are intended to receive this trading information. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/DjDyll/simmer-resolution-tracker) <br>
- [Simmer](https://www.simmer.markets/) <br>
- [Simmer API endpoint](https://api.simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, API calls] <br>
**Output Format:** [Console text, JSON status output, JSONL audit records, JSON state files, and Discord webhook messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on a 5-minute cron when installed; live mode can redeem on-chain positions, while POLY_MODE=sim skips redemptions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
