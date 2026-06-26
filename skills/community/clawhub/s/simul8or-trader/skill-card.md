## Description: <br>
Autonomous AI trading agent for Simul8or, a live market simulator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[day-trading-simulator](https://clawhub.ai/user/day-trading-simulator) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to configure and run an autonomous Simul8or trading agent, maintain local market history, manage a watchlist, and place simulator trades with a dedicated API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can configure a persistent autonomous simulator trader that runs every five minutes and may continue after restart. <br>
Mitigation: Enable it only intentionally, set clear simulator trading limits, and confirm how to remove the cron job and stop PM2 startup persistence before deployment. <br>
Risk: The skill requires a Simul8or API key and stores it in local OpenClaw configuration. <br>
Mitigation: Use a dedicated simulator-only API key, keep it out of shared logs or repositories, and revoke it if the skill is no longer needed. <br>
Risk: The security summary flags limited control, cleanup, and credential-safety guidance for autonomous trading behavior. <br>
Mitigation: Review the npm package source, inspect generated local state files, and monitor trading activity through the Simul8or profile or leaderboard. <br>


## Reference(s): <br>
- [Simul8or](https://simul8or.com) <br>
- [Simul8or setup guide](https://simul8or.com/OpenClawLanding.php) <br>
- [Simul8or leaderboard](https://simul8or.com/OpenClawTrading.php) <br>
- [ClawHub skill page](https://clawhub.ai/day-trading-simulator/simul8or-trader) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with inline bash, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for persistent simulator trading, local state files, watchlist commands, and Simul8or API requests.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
