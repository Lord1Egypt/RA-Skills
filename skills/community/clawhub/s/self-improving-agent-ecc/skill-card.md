## Description: <br>
Instinct-based continuous learning system that captures atomic learnings with confidence scoring, supports project and global scope, and evolves instincts into reusable skills, commands, or agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huamu668](https://clawhub.ai/user/huamu668) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, tool failures, and recurring workflow patterns as instincts or learning logs, then review or evolve them into reusable commands, skills, or agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local hooks can observe broad agent activity and persist raw tool activity or session-derived learnings. <br>
Mitigation: Prefer project-level hook setup, avoid wildcard or global hooks for sensitive work, and review hook scripts before enabling them. <br>
Risk: Observation logs and learning files may contain secrets, private project details, or sensitive tool inputs and outputs. <br>
Mitigation: Keep raw observations out of synced or committed folders, and periodically delete or redact logs that may contain secrets or private data. <br>
Risk: Promoted instincts, generated commands, or evolved skills can encode incorrect or misleading guidance. <br>
Mitigation: Manually review and scan proposed learnings before promotion or deployment. <br>


## Reference(s): <br>
- [Self Improving Agent on ClawHub](https://clawhub.ai/huamu668/self-improving-agent-ecc) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or suggest local learning files, hook configuration, instincts, commands, skills, and agents.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release metadata; skill frontmatter lists 2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
