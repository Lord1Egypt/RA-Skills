## Description: <br>
盘前简报Pro is an offline educational OpenClaw skill that generates simulated pre-market stock briefings, technical-analysis examples, and local Markdown logs without network calls. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[luckjackyer](https://clawhub.ai/user/luckjackyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and learners use this skill to study OpenClaw skill structure, local configuration, report logging, and simulated stock-analysis strategy code. It is not a source of real market data or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio-style fields in config.json and generated logs could expose sensitive position information if a user replaces the sample holdings with real holdings. <br>
Mitigation: Keep the sample values for demonstrations, or protect and delete config.json and logs before sharing the workspace. <br>
Risk: The cron example uses a /root path, which can encourage running the script with unnecessary privileges. <br>
Mitigation: Run the script as a normal user and schedule it from a user-owned OpenClaw workspace. <br>
Risk: Simulated market reports and strategy examples could be mistaken for real recommendations. <br>
Mitigation: Keep the educational and simulated-data notices visible, and do not use generated briefings for trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/luckjackyer/stock-briefing) <br>
- [Publisher profile](https://clawhub.ai/user/luckjackyer) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Artifact README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Sample generated briefing](logs/briefing-2026-03-15.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefing files and console text, with JSON configuration inputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local logs/briefing-YYYY-MM-DD.md reports and may create config.json with sample holdings if it is missing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
