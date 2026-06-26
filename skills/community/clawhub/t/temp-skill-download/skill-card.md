## Description: <br>
Captures agent learnings, errors, corrections, and feature requests in durable markdown logs so future sessions can review and promote useful patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BoBoinCN](https://clawhub.ai/user/BoBoinCN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, missing capabilities, and reusable discoveries in `.learnings/` logs, then promote broadly applicable lessons into project or agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable learning logs and promoted memory can retain secrets, credentials, private transcripts, customer data, or proprietary details. <br>
Mitigation: Require explicit approval and redact sensitive material before storing or promoting any learning. <br>
Risk: Broad hook activation can inject reminders into many sessions and increase persistence of unwanted context. <br>
Mitigation: Prefer project-local setup, avoid global always-on hooks, and review hook scripts before enabling them. <br>
Risk: Incorrect or low-quality learnings can be promoted into shared agent memory or instruction files. <br>
Mitigation: Review entries before promotion and keep promoted guidance concise, sourced, and task-relevant. <br>


## Reference(s): <br>
- [Temp Skill Download release page](https://clawhub.ai/BoBoinCN/temp-skill-download) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hooks Setup](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update `.learnings/` markdown logs, project memory files, hook configuration, or reusable skill scaffolds when approved by the user or agent workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
