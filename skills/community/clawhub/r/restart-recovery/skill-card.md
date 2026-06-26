## Description: <br>
Make OpenClaw agent workflows restart-safe with local checkpoint files, idempotent step tracking, wake/resume handoff, and stale-checkpoint monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanrails](https://clawhub.ai/user/stanrails) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to preserve progress across restart-prone operations such as config updates, service restarts, and long multi-step jobs, then resume unfinished work from validated checkpoint files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkpoint notes may expose sensitive workflow details if users place secrets or tokens in local checkpoint files. <br>
Mitigation: Do not store secrets in checkpoint notes, and keep checkpoint files in controlled workspace storage. <br>
Risk: Optional cron, systemd, or launchd setup can create recurring local stale-checkpoint checks. <br>
Mitigation: Review any scheduler configuration before enabling it and log alerts locally for audit. <br>
Risk: Unfinished checkpoints can cause duplicate side effects if resumed without idempotency controls. <br>
Mitigation: Use an idempotency key for each workflow and acquire a resume lock before continuing unfinished work. <br>


## Reference(s): <br>
- [Restart Recovery Skill Page](https://clawhub.ai/stanrails/restart-recovery) <br>
- [checkpoint-schema.json](references/checkpoint-schema.json) <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON checkpoint files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local memory/checkpoints JSON files; no network output is indicated.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
