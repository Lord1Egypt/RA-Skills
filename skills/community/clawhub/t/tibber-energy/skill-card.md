## Description: <br>
Use Tibber API data to fetch hourly spot prices, plan cheapest appliance or EV charging windows, detect consumption anomalies, and trigger smart-home actions from price thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pmagnomuller](https://clawhub.ai/user/pmagnomuller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Tibber electricity prices, choose low-cost operating windows, detect unusual consumption, and optionally automate trusted local smart-home commands from price thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Control mode can run arbitrary local shell commands when --execute is enabled. <br>
Mitigation: Keep control mode in dry-run until every command and threshold is verified, and use only trusted command strings. <br>
Risk: The skill requires a Tibber access token and may read credentials from environment variables or local configuration. <br>
Mitigation: Store credentials locally, avoid publishing .env or config files with real tokens, and use the minimum token access needed. <br>
Risk: Unattended automation may trigger smart-home actions from incorrect thresholds or untrusted command inputs. <br>
Mitigation: Avoid --execute in unattended agent workflows and prefer read-only price, optimization, and anomaly commands unless local automation is specifically required. <br>


## Reference(s): <br>
- [Tibber Developer Documentation](https://developer.tibber.com) <br>
- [Tibber GraphQL API Endpoint](https://api.tibber.com/v1-beta/gql) <br>
- [ClawHub Skill Page](https://clawhub.ai/pmagnomuller/tibber-energy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tibber access token and Python 3; control mode is dry-run unless --execute is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
