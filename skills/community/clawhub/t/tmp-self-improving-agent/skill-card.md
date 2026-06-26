## Description: <br>
Captures learnings, errors, and corrections so coding agents can log failures, user corrections, missing capabilities, outdated knowledge, and reusable improvements for later review and promotion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiongyj625](https://clawhub.ai/user/xiongyj625) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture recurring corrections, command failures, knowledge gaps, and feature requests as structured learning notes that can later be reviewed, resolved, or promoted into project memory or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning notes can retain sensitive session details, including secrets, personal data, customer content, raw transcripts, tokens, or proprietary information. <br>
Mitigation: Redact sensitive material before writing entries and review learning logs before sharing, committing, or promoting them. <br>
Risk: Optional hooks and cross-session workflows can broaden where learning reminders and session context appear. <br>
Mitigation: Inspect hook scripts before enabling them, prefer project-scoped setup, and require confirmation before promoting entries or sharing them across sessions. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Learning Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiongyj625/tmp-self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and learning-log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings markdown files and may inject reminder text when optional hooks are enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
