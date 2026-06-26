## Description: <br>
Quark Lazy Cli helps agents use the qslazy CLI to inspect, repair, and update QAS-backed Quark cloud-drive media subscriptions with user authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesustoachild](https://clawhub.ai/user/jesustoachild) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill with an agent to check QAS subscription status, choose candidate media resources, configure scheduled reports, and run authorized qslazy update commands for Quark cloud-drive subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires QAS connection details and tokens that can grant access to subscription state. <br>
Mitigation: Use a limited QAS token where possible, keep the .env file local, and avoid exposing real tokens in prompts, logs, reports, or scheduled task text. <br>
Risk: Update and cron commands can change Quark/QAS subscription configuration and transfer files. <br>
Mitigation: Run status or list commands first, require explicit user authorization before update or cron changes, and prefer reviewing stdout before taking further action. <br>
Risk: LLM advisor mode sends resource-selection context to the configured OpenAI-compatible endpoint. <br>
Mitigation: Use code, human, or agent advisor mode unless the endpoint is trusted, and configure LLM credentials only for sessions that need that mode. <br>
Risk: The bundle includes an unrelated local agent permission file. <br>
Mitigation: Remove or ignore .claude/settings.local.json unless it is intentionally needed in the target agent environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jesustoachild/quark-lazy-cli) <br>
- [Publisher Profile](https://clawhub.ai/user/jesustoachild) <br>
- [Environment Variables](references/环境变量.md) <br>
- [Advisor Modes](references/顾问模式.md) <br>
- [OpenClaw Scheduled Tasks](references/OpenClaw定时任务.md) <br>
- [Daily Reports](references/每日汇报.md) <br>
- [Subscription Time Estimation](references/订阅时间估算.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, environment variable templates, and JSON decision snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or edit local configuration, report, cron, and advisor decision files when the user authorizes those actions.] <br>

## Skill Version(s): <br>
0.1.22 (source: pyproject.toml and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
