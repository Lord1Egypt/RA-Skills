## Description: <br>
Monitor Steam game prices and alert when a game hits historical low or a user target price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G-zoe](https://clawhub.ai/user/G-zoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to watch Steam games, check current prices against observed lows or target prices, and produce alerts when a watched game reaches a configured trigger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores watched games, target prices, and observed lows locally. <br>
Mitigation: Use it only where local watchlist storage is acceptable and review the generated data files before sharing or publishing the workspace. <br>
Risk: Documentation may overstate verified all-time historical-low behavior. <br>
Mitigation: Treat alerts as Steam discount or target-price notifications unless the implementation is updated to verify all-time lows from an authoritative historical source. <br>
Risk: The skill contacts CheapShark and Steam APIs during normal use. <br>
Mitigation: Run it only in environments where outbound requests to those services are allowed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/G-zoe/steam-lowest-price-skill) <br>
- [CheapShark games API](https://www.cheapshark.com/api/1.0/games) <br>
- [Steam app details API](https://store.steampowered.com/api/appdetails) <br>
- [Steam store app page](https://store.steampowered.com/app/{appid}/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Alerts include game name, current price, observed low price, price difference, discount status, and Steam store link.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
