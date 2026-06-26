## Description: <br>
Scans sports odds from traditional bookmakers through The Odds API or demo data, detects arbitrage opportunities above a configurable profit threshold, calculates stake splits, and writes local JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can run this managed scanner to monitor selected sports markets for cross-bookmaker arbitrage opportunities and inspect the resulting stake calculations. The output is informational and should be reviewed before relying on it for betting or financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner runs on a schedule and may consume The Odds API quota while polling configured sports. <br>
Mitigation: Use a limited-purpose Odds API key, tune the SPORTS list if needed, and monitor quota usage. <br>
Risk: RESULTS_FILE is configurable and could write results to an unintended local path. <br>
Mitigation: Leave RESULTS_FILE at the default path or set it only to a dedicated non-sensitive output file. <br>


## Reference(s): <br>
- [The Odds API](https://the-odds-api.com) <br>
- [The Odds API Sports API Documentation](https://the-odds-api.com/sports-odds-data/sports-apis.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Files] <br>
**Output Format:** [Log text and JSON results file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a managed automaton every 30 minutes; results are written to the configured RESULTS_FILE path and capped to the latest 500 entries.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence, clawhub.json, and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
