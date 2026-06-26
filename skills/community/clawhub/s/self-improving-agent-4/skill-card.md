## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marveldcdad-eng](https://clawhub.ai/user/marveldcdad-eng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture corrections, command failures, missing capabilities, outdated assumptions, and recurring best practices as project learning records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to persist conversation and error details into project memory files, which may capture sensitive data. <br>
Mitigation: Keep learning records local or reviewed before committing, and redact tokens, credentials, personal data, customer content, private prompts, and raw command output. <br>
Risk: Promoting unreviewed learnings into agent instruction files can introduce incorrect or misleading guidance. <br>
Mitigation: Require human approval before promoting entries into CLAUDE.md, AGENTS.md, .github/copilot-instructions.md, SOUL.md, or TOOLS.md. <br>


## Reference(s): <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces learning, error, and feature-request entries intended for project memory files.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
