## Description: <br>
reddi.tech fork of self-improving-agent that captures learnings, errors, and corrections so agents can review and promote durable guidance before future work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to log command failures, corrections, feature requests, knowledge gaps, and reusable best practices into local learning files. It is intended to help future agent sessions review and promote useful lessons into project or workspace guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local learning logs may capture secrets, private transcripts, customer data, sensitive stack traces, or other context that should not be persisted. <br>
Mitigation: Review entries before saving or promoting them, redact sensitive values, and keep learning files local when they contain private project context. <br>
Risk: Optional hooks can create broad recurring reminders and may read command output for error detection. <br>
Mitigation: Prefer project-level or matcher-scoped hook configuration, avoid global always-on setup unless needed, and verify hook scope before enabling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/reddi-self-improving-agent) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Entry Examples](artifact/references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local learning-entry formats and optional hook setup guidance; the release metadata reports no outbound network requirement.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact frontmatter and changelog show 1.0.12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
