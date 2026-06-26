## Description: <br>
Tokenguard Pro analyzes OpenClaw usage patterns to identify token waste and provide cost-saving recommendations for high-volume AI API users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sammy-the-bot](https://clawhub.ai/user/sammy-the-bot) <br>

### License/Terms of Use: <br>
Commercial <br>


## Use Case: <br>
External OpenClaw users, teams, and developers use this skill to review historical token usage, find waste patterns such as oversized context or repeated queries, and generate recommendations for lowering AI API spend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to install and run a tokenguard-analyze command, but server security evidence reports that the command source is missing. <br>
Mitigation: Review the version before installing and ask the publisher to include the missing source for the command before operational use. <br>
Risk: The skill analyzes OpenClaw session logs, which may contain sensitive prompts, workflow details, token usage, or cost data. <br>
Mitigation: Run analysis only on minimized or redacted logs, confirm whether processing stays local, and protect generated reports as sensitive artifacts. <br>
Risk: Cost savings are estimates based on historical patterns and standard pricing assumptions. <br>
Mitigation: Validate recommendations against provider dashboards, current pricing, and application quality requirements before applying changes. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sammy-the-bot/tokenguard-pro) <br>
- [TokenGuard Pro README](artifact/README.md) <br>
- [Support repository listed by artifact](https://github.com/appincubator/tokenguard-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance, Shell commands] <br>
**Output Format:** [Human-readable analysis report or JSON export with optimization recommendations and projected savings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from historical OpenClaw logs and may include sensitive usage, cost, or workflow details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, clawhub.yaml, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
