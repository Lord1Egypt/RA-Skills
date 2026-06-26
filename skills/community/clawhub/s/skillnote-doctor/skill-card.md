## Description: <br>
A diagnostic tool for OpenClaw agents that checks skill registry connectivity, AGENTS.md setup, config file validity, and installed skill health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[latentloop07](https://clawhub.ai/user/latentloop07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose SkillNote setup problems, including registry reachability, local configuration validity, AGENTS.md markers, and resolver health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw and SkillNote setup files during diagnosis. <br>
Mitigation: Run it only when SkillNote/OpenClaw setup diagnostics are intended and review the reported findings before acting on remediation guidance. <br>
Risk: The skill makes limited health-check requests to the host configured in SkillNote. <br>
Mitigation: Confirm the local SkillNote config points to a trusted host before running the checks. <br>
Risk: Broad trigger phrases may activate the skill when a user asks for general debugging help. <br>
Mitigation: Use narrower invocation language or review activation behavior before deployment in shared agent environments. <br>


## Reference(s): <br>
- [SkillNote Doctor on ClawHub](https://clawhub.ai/latentloop07/skillnote-doctor) <br>
- [latentloop07 ClawHub profile](https://clawhub.ai/user/latentloop07) <br>
- [SkillNote self-host guide](https://github.com/luna-prompts/skillnote) <br>
- [SkillNote issues](https://github.com/luna-prompts/skillnote/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnostic report with pass/fail checks, remediation guidance, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports six read-only diagnostic checks and a summary count.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
