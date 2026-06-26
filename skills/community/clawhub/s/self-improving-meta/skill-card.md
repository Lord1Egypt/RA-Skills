## Description: <br>
Improves agent infrastructure including prompt files, skill definitions, hooks, rules, extensions, and memory management when agents misread instructions, hooks fail, skills do not activate, rules conflict, context is bloated, memory is stale, or templates are unclear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to capture recurring infrastructure learnings, log hook or skill activation issues, and propose reviewed improvements to shared prompt, memory, hook, rule, and skill files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently steer or change agent prompts, hooks, memory, rules, and skill files. <br>
Mitigation: Require an explicit reviewed diff before edits to shared infrastructure, and keep changes scoped to the identified issue. <br>
Risk: Hook reminders and learning logs may capture sensitive context if raw outputs or secrets are copied into markdown files. <br>
Mitigation: Do not log secrets, environment variables, tokens, private keys, raw command output, or full transcripts; prefer short redacted summaries. <br>
Risk: Broad or global hook activation could add unwanted persistent behavior across workspaces. <br>
Mitigation: Keep hooks project-scoped, avoid empty or global matchers, and enable the optional OpenClaw hook only where the reminder workflow is intended. <br>


## Reference(s): <br>
- [Self-Improving Meta ClawHub Page](https://clawhub.ai/jose-compu/self-improving-meta) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hooks Setup](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional hook reminder text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .learnings markdown logs and may propose reviewed changes to shared agent infrastructure files.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
