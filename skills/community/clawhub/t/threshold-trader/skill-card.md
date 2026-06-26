## Description: <br>
Automatically trades prediction markets when prices deviate beyond a configured probability threshold, using Kelly Criterion sizing and safety checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skybinjf](https://clawhub.ai/user/skybinjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prediction-market operators use this skill to configure and run threshold-based trading automation for Simmer venues, with paper trading by default and live trading only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform prediction-market account actions and may use real venues when configured for polymarket, kalshi, or live mode. <br>
Mitigation: Start with a limited or test Simmer API key, keep SIMMER_VENUE set to sim during evaluation, and enable live trading only after reviewing the configuration and expected financial exposure. <br>
Risk: The automaton configuration can run scans and redemption checks every 15 minutes. <br>
Mitigation: Disable the scheduled automaton or run the script manually when unattended market scans or account checks are not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skybinjf/threshold-trader) <br>
- [Simmer Dashboard](https://simmer.markets/dashboard) <br>
- [Simmer Skills Documentation](https://docs.simmer.markets/skills/building) <br>
- [Simmer Skills Registry](https://simmer.markets/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Console text, environment-variable configuration, and Simmer SDK trading or redemption actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading on the sim venue and may run on a 15-minute automaton schedule.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
