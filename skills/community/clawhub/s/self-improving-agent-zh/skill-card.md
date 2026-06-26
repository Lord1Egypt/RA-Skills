## Description: <br>
Captures agent learnings, errors, corrections, and feature requests as markdown notes so future sessions can improve workflows and promote stable guidance into project memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WuXian-upup](https://clawhub.ai/user/WuXian-upup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture non-obvious failures, user corrections, knowledge gaps, and recurring patterns as structured learning notes for later review and promotion into agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning notes can retain sensitive prompts, commands, error output, tokens, personal data, or customer information. <br>
Mitigation: Configure agents to log sanitized summaries only, and exclude secrets, raw transcripts, personal data, and customer information from learning files. <br>
Risk: Cross-session transcript sharing can spread sensitive information beyond the original task context. <br>
Mitigation: Disable cross-session transcript sharing unless it is explicitly needed and authorized for the workspace. <br>
Risk: Promoting learning entries into future instruction or memory files can preserve incorrect, outdated, or unsafe guidance. <br>
Mitigation: Require human approval before promoting any learning into persistent agent instructions or memory files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/WuXian-upup/self-improving-agent-zh) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured learning, error, and feature-request entry formats for agent-maintained markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
