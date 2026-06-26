## Description: <br>
Make your agent 'live beside you' with heartbeats, a mood system, relationship evolution, and independent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kitephp](https://clawhub.ai/user/kitephp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize and maintain a companion-style agent runtime with scheduled heartbeats, mood and relationship state, daily planning, and local memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent scheduled behavior can keep writing memory and state in the workspace. <br>
Mitigation: Review and intentionally enable any cron jobs; remove the cron jobs and soul/ data when the companion behavior is no longer wanted. <br>
Risk: The skill can change root agent instruction files through managed blocks. <br>
Mitigation: Review the managed blocks in SOUL.md, HEARTBEAT.md, and AGENTS.md after initialization and before using the skill in a shared or sensitive workspace. <br>
Risk: Personal profile, plan, memory, and diary context can be sent to Anthropic when an API key is configured. <br>
Mitigation: Use a dedicated Anthropic key only with informed consent, and unset or remove the key when external LLM processing is not acceptable. <br>
Risk: Personal life data may persist in workspace logs and memory files. <br>
Mitigation: Use a dedicated workspace for this skill, inspect the soul/ directory regularly, and delete stored data when retiring the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kitephp/soul-agent) <br>
- [soul Layout](references/soul-layout.md) <br>
- [Managed Block Policy](references/managed-blocks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON and configuration snippets plus shell commands; runtime scripts can produce JSON state files and Markdown logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create scheduled workspace behavior and write managed blocks plus soul/ state, log, plan, profile, and memory files after initialization.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
