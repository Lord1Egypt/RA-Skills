## Description: <br>
Provides self-reflection, correction logging, and local self-improvement memory so an agent can learn from explicit feedback and reusable lessons over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpjump11](https://clawhub.ai/user/jpjump11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add persistent, local improvement memory for explicit corrections, self-reflection, and scoped preferences. It is intended for agents that should cite learned behavior, avoid learning from silence, and support inspection or deletion of stored memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package identity mismatch between server metadata and artifact frontmatter. <br>
Mitigation: Verify the publisher, package slug, displayed name, and intended artifact before installation. <br>
Risk: Persistent memory can change later agent behavior across sessions. <br>
Mitigation: Install only when persistent local memory is desired, keep entries inspectable, and use the documented forget or export flows when needed. <br>
Risk: Memory files may capture sensitive or inappropriate information if used carelessly. <br>
Mitigation: Do not store credentials, financial data, medical data, biometric data, location patterns, access patterns, or third-party personal information. <br>
Risk: Workspace steering edits may affect normal agent operation. <br>
Mitigation: Review proposed edits to AGENTS.md, SOUL.md, and HEARTBEAT.md before accepting them. <br>
Risk: The optional Proactivity companion may require separate network-enabled installation. <br>
Mitigation: Decline the optional Proactivity install until it has been reviewed separately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpjump11/root) <br>
- [Publisher profile](https://clawhub.ai/user/jpjump11) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory operations](artifact/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files under ~/self-improving/ and optional workspace steering files when installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
