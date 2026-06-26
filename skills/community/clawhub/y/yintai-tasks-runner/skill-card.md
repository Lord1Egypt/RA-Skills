## Description: <br>
Automatically polls for Yintai tasks, claims authorized tasks, updates task status, generates ZIP deliverables, and uploads results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bossandy123](https://clawhub.ai/user/bossandy123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing Yintai or OpenClaw task accounts use this skill to poll available tasks, claim tasks with configured credentials, update execution status, and package or upload task deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses provided credentials to claim Yintai tasks, update task status, create ZIP deliverables, and upload results. <br>
Mitigation: Install and run it only for accounts where the agent is authorized to act on Yintai tasks. <br>
Risk: API keys and secrets can be exposed if copied from local config files or passed directly on the command line. <br>
Mitigation: Prefer environment variables or a secret manager for YINTAI_APP_KEY and YINTAI_APP_SECRET. <br>
Risk: Continuous polling can claim tasks that do not match the operator's intent. <br>
Mitigation: Set category and bounty filters before continuous mode and use a reasonable polling interval. <br>
Risk: Generated ZIP deliverables may contain task details and execution metadata. <br>
Mitigation: Protect the output directory and periodically clean files that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bossandy123/yintai-tasks-runner) <br>
- [API Reference](references/api.md) <br>
- [CLI Usage](references/cli.md) <br>
- [Configuration Guide](references/config.md) <br>
- [Usage Guide](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown status updates plus ZIP deliverables containing JSON metadata and text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YINTAI_APP_KEY and YINTAI_APP_SECRET; may create local output files and upload ZIP deliverables to the configured Yintai task service.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
