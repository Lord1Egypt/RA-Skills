## Description: <br>
Quickly configures OpenClaw's hierarchical memory system with structured writing, retrieval, weekly maintenance, and metadata tagging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueylee-dotcom](https://clawhub.ai/user/xueylee-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install a ready-made memory workspace with user, project, daily log, tool, and heartbeat templates. It is intended to make session continuity and memory maintenance easier for new or reset OpenClaw instances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed memory templates can cause the agent to retain sensitive personal, project, or environment context over time. <br>
Mitigation: Review the installed memory files regularly, keep secrets out of MEMORY.md, TOOLS.md, USER.md, and daily logs, and remove retained details that are no longer needed. <br>
Risk: The templates include proactive checks for email, calendar, social mentions, weather, and code repository work that may exceed the user's intended authority. <br>
Mitigation: Remove or narrow proactive account checks and commit or push authority unless the user explicitly wants those behaviors. <br>
Risk: The templates include deletion and pruning behavior for BOOTSTRAP.md and long-term memory files. <br>
Mitigation: Require confirmation or backups before deleting bootstrap material or pruning memory entries. <br>
Risk: The generated TOOLS.md template encourages storing API keys and environment details in plaintext. <br>
Mitigation: Store secrets in a dedicated secret manager or environment variables instead of memory or tool markdown files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xueylee-dotcom/rick-memory-setup) <br>
- [Publisher profile](https://clawhub.ai/user/xueylee-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown templates with shell setup output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs OpenClaw workspace memory templates for user context, long-term memory, daily logs, tool configuration, and heartbeat maintenance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
