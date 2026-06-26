## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Buradly](https://clawhub.ai/user/Buradly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to capture corrections, command failures, knowledge gaps, feature requests, and reusable practices as structured markdown logs for later review and promotion into project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files can retain sensitive or incorrect information if entries are copied from command output or conversation context without review. <br>
Mitigation: Do not log secrets, credentials, or raw sensitive output; review and redact every entry before keeping it or promoting it into agent instruction files. <br>
Risk: Broad hook configuration can inject reminders into more sessions than intended and add recurring prompt context. <br>
Mitigation: Keep hooks project-local, prefer narrow matchers where available, and enable only the activator or error detector that is needed for the workspace. <br>
Risk: Cross-session sharing and memory promotion can spread unverified guidance. <br>
Mitigation: Manually validate entries before sending them to another session or promoting them to AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or similar instruction files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Buradly/self-improving-agent-3) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured log templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local learning, error, and feature-request records; optional hooks emit short reminder messages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
