## Description: <br>
Monitor OpenClaw API costs in real time, set budget alerts, optimize model spending, track token usage by session and model, and prevent budget overruns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redwoo](https://clawhub.ai/user/redwoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review OpenClaw API spending, set cost thresholds, identify expensive usage patterns, and choose lower-cost model routing for routine work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cost and usage summaries can expose sensitive operational patterns if sent to notification channels. <br>
Mitigation: Confirm recipients before enabling Slack, Discord, or email examples, and share only the minimum cost detail needed. <br>
Risk: Webhook URLs or notification credentials can be exposed if pasted directly into scripts or chat transcripts. <br>
Mitigation: Store webhook URLs in a secret manager or environment variable and avoid committing them to skill files. <br>


## Reference(s): <br>
- [Token Cost Monitor on ClawHub](https://clawhub.ai/redwoo/token-cost-monitor) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/redwoo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local cost-monitoring guidance, budget alert examples, model routing recommendations, and a shell-based pricing reference.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
