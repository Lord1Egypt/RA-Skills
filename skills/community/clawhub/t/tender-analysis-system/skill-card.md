## Description: <br>
Automates tender monitoring and generates structured analyses of bid documents across contract, payment, technical, evaluation, and risk dimensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylbwjf](https://clawhub.ai/user/ylbwjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, sales, and bid teams use this skill to monitor tender sources, summarize new opportunities, and produce structured tender analysis reports for review before bidding. <br>

### Deployment Geography for Use: <br>
Global, with configured tender data sources focused on China. <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can install recurring background cron jobs for hourly and two-hour runs. <br>
Mitigation: Inspect the crontab entries before running cron_setup.sh, confirm the schedule is acceptable, create required log directories, and document how to remove only these entries. <br>
Risk: Configured email credentials, Feishu webhooks, and LLM API keys are sensitive. <br>
Mitigation: Keep secrets out of shared files, use protected local configuration or a secret manager, and rotate any exposed credentials. <br>
Risk: Automated tender summaries and analysis reports can be incomplete or misleading. <br>
Mitigation: Review generated reports against the original tender documents before making bid or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ylbwjf/tender-analysis-system) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact configuration](artifact/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and concise operational guidance with YAML and shell snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local SQLite data and Markdown report files when the bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
