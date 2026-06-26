## Description: <br>
Captures errors, corrections, and feature requests so an OpenClaw agent can preserve recurring learnings and avoid repeating the same mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sam-k-migz](https://clawhub.ai/user/sam-k-migz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to record command failures, user corrections, feature requests, and useful workflow discoveries in durable Markdown logs. It also provides optional hook setup and skill-extraction guidance for teams that want recurring learnings promoted into agent memory or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable learning logs and memory promotion can preserve sensitive details or inaccurate guidance. <br>
Mitigation: Avoid storing secrets, raw transcripts, private keys, environment variables, or full command output; review and sanitize entries before promoting them into agent memory files. <br>
Risk: Broad always-on hooks can add persistent reminders and may inspect command output for error patterns. <br>
Mitigation: Prefer project-local, opt-in hook setup; review scripts before enabling them, start with the activator-only hook, and enable command-output error detection only when that behavior is intended. <br>
Risk: Skill extraction can turn a local learning into reusable agent instructions before it is mature. <br>
Mitigation: Require explicit user approval, use dry-run output first, and review generated skills before relying on or sharing them. <br>


## Reference(s): <br>
- [OpenClaw Learning Loop on ClawHub](https://clawhub.ai/sam-k-migz/self-improving-agent-openclaw) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional generated skill scaffolds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write .learnings Markdown logs, agent memory files, hook configuration, and new skill scaffolds when the user approves those actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
