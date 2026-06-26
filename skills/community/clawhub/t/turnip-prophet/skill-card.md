## Description: <br>
Predicts Animal Crossing: New Horizons turnip prices from weekly buy and sell data using the game's price-pattern algorithm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicholasjackson](https://clawhub.ai/user/nicholasjackson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and game-assistant agents use this skill to track Animal Crossing: New Horizons turnip prices, update weekly local price memory, generate predictions, and choose when to sell. Optional reminders can prompt missing price checks through the user's existing OpenClaw messaging setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores weekly turnip data and optional reminder configuration in local memory files. <br>
Mitigation: Use the core predictor only if local storage is acceptable, and delete the local memory or reminder configuration files when no longer needed. <br>
Risk: Dependency setup may run package-install commands, including sudo apt-get or brew for jq. <br>
Mitigation: Review each pip, brew, or sudo install command before running it and install dependencies through an approved local package-management process. <br>
Risk: Optional reminders can add cron entries that send messages through the user's existing OpenClaw messaging configuration. <br>
Mitigation: Enable reminders only after confirming the channel, target ID, OpenClaw path, skill directory, and exact crontab entries. <br>


## Reference(s): <br>
- [Turnip Prophet on ClawHub](https://clawhub.ai/nicholasjackson/turnip-prophet) <br>
- [Publisher profile](https://clawhub.ai/user/nicholasjackson) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples, shell commands, prediction summaries, and chart-generation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local skill memory and produce a chart image path when prediction visualization is requested.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
