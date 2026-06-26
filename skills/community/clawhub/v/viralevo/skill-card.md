## Description: <br>
Self-evolving viral content trend advisor that monitors public trend signals, predicts what to post and when, and improves its own accuracy over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xF69](https://clawhub.ai/user/0xF69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and operators use ViralEvo with an agent to collect public trend signals, generate posting guidance, log post outcomes, and adjust trend-scoring weights over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tavily API key and makes outbound trend-search requests. <br>
Mitigation: Install only when external public trend searches are acceptable, and provide a scoped Tavily key through the documented environment or OpenClaw configuration path. <br>
Risk: Optional cron setup can run recurring background collection, verification, and weekly configuration changes. <br>
Mitigation: Enable scheduled jobs only when recurring reports and weekly model-weight updates are desired, and review the cron commands before adding them. <br>
Risk: Uninstall instructions include an optional data-deletion command for the ViralEvo workspace directory. <br>
Mitigation: Back up the local ViralEvo data directory before running the optional deletion step. <br>
Risk: Trend predictions are probabilistic and may be incorrect or misleading for business decisions. <br>
Mitigation: Treat reports as directional guidance, compare them with current platform context, and avoid relying on them as the sole basis for posting or revenue decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xF69/viralevo) <br>
- [OpenClaw cron jobs documentation](https://docs.openclaw.ai/automation/cron-jobs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with command and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English and Chinese operation; may create local configuration, SQLite trend data, logs, and Markdown reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence; artifact frontmatter states 0.6.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
