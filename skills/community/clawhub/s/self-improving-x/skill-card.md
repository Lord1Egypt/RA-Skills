## Description: <br>
Captures agent learnings, errors, corrections, and feature requests in structured Markdown logs so future agent sessions can review, promote, or extract reusable guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seepine](https://clawhub.ai/user/seepine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to record non-obvious fixes, user corrections, tool failures, and requested capabilities as durable workspace notes. The notes can later be reviewed, promoted into agent guidance, or used as source material for reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace learning logs may capture sensitive conversation details, command output, paths, or customer data. <br>
Mitigation: Require review before writing learning entries and redact secrets, tokens, customer data, internal URLs, sensitive paths, and full command output unless the user explicitly approves. <br>
Risk: Promoting entries into agent guidance can alter future agent behavior without clear consent. <br>
Mitigation: Require explicit review before changing AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, copilot instructions, or .agents/skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seepine/self-improving-x) <br>
- [Skill instructions](SKILL.md) <br>
- [README](README.md) <br>
- [Learning log template](assets/LEARNINGS.md) <br>
- [Error log template](assets/ERRORS.md) <br>
- [Feature request log template](assets/FEATURE_REQUESTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with structured log templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace-local learning, error, and feature-request records for later human or agent review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
