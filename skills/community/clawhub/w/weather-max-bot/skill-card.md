## Description: <br>
Weather Max Bot is a ClawHub skill package identified as a weather trading agent, while its evidence also contains Simmer and Polymarket prediction-market trading materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pasichnuk969](https://clawhub.ai/user/pasichnuk969) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect weather-related prediction markets and, based on bundled materials, may configure or run Simmer or Polymarket trading workflows. Review the package identity mismatch and trading settings before any live use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package identity is inconsistent: server evidence identifies Weather Max Bot, while artifact metadata and content mix a weather bot, Simmer documentation, and a Polymarket BTC trading strategy. <br>
Mitigation: Confirm the exact skill intended before installation or execution; avoid cron, quiet mode, and live trading until the publisher resolves the mismatch. <br>
Risk: The bundled trading strategy can make real-money Polymarket trades and may use sensitive wallet credentials. <br>
Mitigation: Run dry-run mode first, provide wallet keys only when live trading is intended, and use a dedicated low-balance or managed wallet. <br>
Risk: Automated or quiet execution can make repeated trades harder to observe. <br>
Mitigation: Review configuration, budgets, and exit settings manually before unattended runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pasichnuk969/weather-max-bot) <br>
- [Publisher profile](https://clawhub.ai/user/pasichnuk969) <br>
- [Simmer homepage](https://simmer.markets) <br>
- [Simmer documentation](https://docs.simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, configuration examples, and runtime text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API market listings, dry-run output, position summaries, trade status, and configuration guidance when executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
