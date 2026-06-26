## Description: <br>
Trade Polymarket weather markets using NOAA forecasts via Simmer API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnjerry8749](https://clawhub.ai/user/johnjerry8749) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect and automate Polymarket temperature-market trades based on NOAA forecasts, Simmer market data, and configurable thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades when run with live execution enabled. <br>
Mitigation: Start in dry-run mode, use small max-position and max-trades settings, and enable live execution only after reviewing the financial risk. <br>
Risk: The skill requires SIMMER_API_KEY, which may expose Simmer account data and possible trading authority. <br>
Mitigation: Store the key securely, avoid sharing logs or environments that expose it, and rotate it if it may have been disclosed. <br>
Risk: Disabling safeguards or running quiet scheduled executions can increase exposure to unintended trades. <br>
Mitigation: Keep safeguards enabled, review thresholds and location settings before scheduling, and use quiet or cron-style runs only after observing dry-run behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/johnjerry8749/weather-py) <br>
- [Simmer API](https://api.simmer.markets) <br>
- [Simmer Dashboard](https://simmer.markets/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run output unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
1.7.2 (source: artifact frontmatter and _meta.json); ClawHub release version 0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
