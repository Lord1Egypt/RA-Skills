## Description: <br>
Turing Pyramid provides local, stateful action prioritization for AI agents using configurable needs, time-based decay, tension scoring, execution-gate tracking, optional continuity scripts, and an opt-in watchdog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tensusds](https://clawhub.ai/user/tensusds) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent stewards use Turing Pyramid to give an agent a local heartbeat action selector that proposes what to do next, tracks completion evidence, and maintains optional continuity state inside an isolated workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest public posting, messaging, web-search, or publishing actions that an auto-executing agent might carry out with its own tools. <br>
Mitigation: Review assets/needs-config.json before use, set unwanted external or social actions to weight 0, and require separate human approval for posting, messaging, deleting, reorganizing, purchasing, or publishing. <br>
Risk: The skill is stateful and reads or writes files under WORKSPACE, so a broad workspace can expose sensitive files to scans and state updates. <br>
Mitigation: Install it only in an isolated WORKSPACE that does not contain credentials, private material, home directories, or system folders. <br>
Risk: Continuity and watchdog deployment can create persistent background behavior, and opt-in watchdog settings can kill skill processes or clean temporary files. <br>
Mitigation: Start with interactive or heartbeat-only use, review daemon and watchdog scripts before cron deployment, run as a non-root user, and keep allow_kill and allow_cleanup disabled unless explicitly needed. <br>
Risk: Optional external-model scanning can call an inference API if enabled and configured with credentials. <br>
Mitigation: Leave external-model scanning disabled unless a steward has documented the credential source, endpoint, and approval path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tensusds/turing-pyramid) <br>
- [Tuning Guide](references/TUNING.md) <br>
- [Architecture](references/architecture.md) <br>
- [Deliberation Protocol](docs/DELIBERATION-PROTOCOL.md) <br>
- [Continuation Design](docs/CONTINUATION-DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/plain text guidance with shell commands and JSON-backed state/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces action suggestions, gate status, audit/state files, follow-up records, and optional MINDSTATE.md continuity snapshots inside WORKSPACE.] <br>

## Skill Version(s): <br>
1.34.10 (source: target metadata, release metadata, _meta.json, CHANGELOG, SKILL.md footer) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
