## Description: <br>
Secretary Memory provides an OpenClaw memory system for partitioned recall, session summaries, preference extraction, conflict checks, archiving, and full-text search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wgj24](https://clawhub.ai/user/wgj24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain a long-term local memory workspace, search prior sessions, summarize conversations, manage user preferences and projects, and surface conflicts or follow-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses conversation-derived data that may include sensitive information. <br>
Mitigation: Configure the memory directory deliberately, avoid recording secrets or sensitive third-party data, and review stored memories before reuse. <br>
Risk: External LLM summarization may expose memory content outside the local workspace if enabled. <br>
Mitigation: Disable external summarization or route it only through approved providers and data-handling controls. <br>
Risk: Daemon, cron, and generated-skill workflows can change memory or future skill behavior with weak approval boundaries. <br>
Mitigation: Enable scheduled or generated-skill workflows only after manual review, and inspect generated skills and triggers before use. <br>


## Reference(s): <br>
- [Secretary Memory ClawHub release](https://clawhub.ai/wgj24/secretary-memory) <br>
- [OpenClaw secretary memory specification](references/SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code references, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local memory files, SQLite FTS indexes, summaries, user profile data, and generated skills when invoked.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
