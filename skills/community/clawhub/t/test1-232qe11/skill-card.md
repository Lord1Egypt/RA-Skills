## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for agents and coding assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a6191187](https://clawhub.ai/user/a6191187) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to log command failures, user corrections, feature requests, knowledge gaps, and recurring best practices into project learning files. It also provides optional hook and extraction workflows for promoting high-value learnings into durable agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive or noisy information in learning logs. <br>
Mitigation: Keep entries short and sanitized, and avoid storing secrets, raw transcripts, tokens, private keys, environment variables, or full source and configuration files. <br>
Risk: Promoted learnings can change future agent behavior through instruction files or memory. <br>
Mitigation: Require explicit approval before promoting entries into instruction files or workspace memory, and review proposed changes before deployment. <br>
Risk: Optional hooks and cross-session workflows can inspect command output or share session history. <br>
Mitigation: Enable hooks and cross-session sharing only in trusted environments and prefer sanitized summaries over raw transcripts. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hooks Setup](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and logging templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project-local .learnings markdown files and optional skill scaffold files when explicitly used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
