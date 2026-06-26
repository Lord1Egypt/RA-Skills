## Description: <br>
Helps OpenClaw agents capture errors, user corrections, missing capabilities, and better practices into learning files, then review and promote recurring patterns into durable memory or rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw agents use this skill to preserve lessons from failures, corrections, missing capabilities, and better approaches so future sessions can avoid repeated mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can preserve user or project context in durable learning and memory files. <br>
Mitigation: Use it only when durable agent memory is intended, keep activation project-scoped, and review or redact entries before promotion into long-term files. <br>
Risk: Broad automatic reminders can encourage unnecessary logging on routine prompts or transient tool failures. <br>
Mitigation: Prefer narrow hook matchers and avoid global every-prompt activation; log only non-obvious, recurring, or useful lessons. <br>
Risk: Incorrect or low-value lessons could be promoted into persistent operating rules. <br>
Mitigation: Promote only reviewed and concrete patterns, especially recurring patterns, into MEMORY.md, AGENTS.md, SOUL.md, or TOOLS.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovensky1992-wk/self-improving-learner) <br>
- [Publisher profile](https://clawhub.ai/user/lovensky1992-wk) <br>
- [OpenClaw integration reference](references/openclaw-integration.md) <br>
- [Hooks setup reference](references/hooks-setup.md) <br>
- [Learning entry examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file templates, and hook configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reminders and structured learning records for files such as .learnings/ERRORS.md, .learnings/LEARNINGS.md, .learnings/FEATURE_REQUESTS.md, MEMORY.md, AGENTS.md, SOUL.md, and TOOLS.md.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
