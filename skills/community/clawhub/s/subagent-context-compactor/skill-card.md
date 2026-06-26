## Description: <br>
A context-compaction agent that monitors conversation context, applies HOT/WARM/COLD layered compression, and helps reduce token use while preserving important session information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoshan](https://clawhub.ai/user/geoshan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage long-running OpenClaw sessions by monitoring context growth, compacting conversation history, and retaining decisions, tasks, and preferences for later use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a local background context-management service that reads and stores OpenClaw workspace memory. <br>
Mitigation: Install only when a local background service is intended, review scripts before use, and back up context_compactor.db before cleanup or maintenance commands. <br>
Risk: The localhost API and monitor scripts can expose or modify compaction state if access is not controlled. <br>
Mitigation: Keep the API bound to localhost, restrict local access, and avoid auto-start or cron deployment until the service behavior has been reviewed. <br>
Risk: Notification examples or external integrations could disclose context-management information if enabled without review. <br>
Mitigation: Remove or replace external notification examples before use and confirm any integration destinations are approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/geoshan/subagent-context-compactor) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw context management](https://docs.openclaw.ai/context-management) <br>
- [OpenClaw token optimization](https://docs.openclaw.ai/token-optimization) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, JSON configuration, and local service status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local context summaries, compaction reports, monitoring status, and API responses when its scripts or service are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
