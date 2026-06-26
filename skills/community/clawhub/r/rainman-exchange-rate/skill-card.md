## Description: <br>
exchange-rate helps agents convert currencies and query latest, historical, and trend exchange rates using Frankfurter API data sourced from the European Central Bank. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deusyu](https://clawhub.ai/user/deusyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to convert currency amounts, look up latest or historical exchange rates, list supported currencies, and inspect exchange-rate trends from a local Bun CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends currency codes, amounts, and dates to the disclosed Frankfurter exchange-rate API. <br>
Mitigation: Avoid entering sensitive transaction details as amounts or dates unless those query parameters are acceptable to share with the Frankfurter service. <br>
Risk: Accidental activation could run a local Bun script and make an external exchange-rate query. <br>
Mitigation: Use clear activation phrases and review the generated command before execution. <br>
Risk: Exchange-rate data is updated once per working day and may not reflect intraday market movement. <br>
Mitigation: Treat results as reference exchange-rate data and confirm time-sensitive financial decisions with an authoritative source. <br>


## Reference(s): <br>
- [Command Map](references/command-map.md) <br>
- [Frankfurter API](https://api.frankfurter.dev/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/deusyu/rainman-exchange-rate) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Text guidance with Bun shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ISO 4217 currency codes, optional dates in YYYY-MM-DD format, positive numeric amounts, and comma-separated target currency lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
