## Description: <br>
Local-first hybrid memory skill for OpenClaw agents that helps find, recall, search, and reuse past knowledge across episodic, semantic, procedural, and learning memory while surfacing host health and degraded-mode guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciklopentan](https://clawhub.ai/user/ciklopentan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to query, write, index, audit, and maintain local agent memory while keeping semantic readiness, degraded retrieval, and rollback expectations explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write durable local memory files. <br>
Mitigation: Review memory-write intent before using memorize or maintenance commands, and keep destructive auto-actions disabled unless an operator explicitly chooses otherwise. <br>
Risk: Maintenance behavior can inventory parts of the local workspace or cache. <br>
Mitigation: Review hygiene scan roots and maintenance commands before installation or scheduled use, especially on shared or sensitive hosts. <br>
Risk: Semantic retrieval depends on a local loopback semantic helper and Qdrant configuration. <br>
Mitigation: Verify the Qdrant URL and keep it local unless the operator intentionally wants memory content sent elsewhere. <br>
Risk: Host state can be degraded even when the packaged skill version is current. <br>
Mitigation: Run health-check.sh --json and honor the returned status, degraded flags, warnings, and authority fields before trusting retrieval or write operations. <br>


## Reference(s): <br>
- [Super Memori ClawHub listing](https://clawhub.ai/ciklopentan/super-memori) <br>
- [Architecture](references/architecture.md) <br>
- [Command Contracts](references/command-contracts.md) <br>
- [Retrieval Pipeline](references/retrieval-pipeline.md) <br>
- [Health Model](references/health-model.md) <br>
- [Maintenance Reference](references/maintenance.md) <br>
- [Verification Evidence](references/verification-evidence.md) <br>
- [OpenClaw Hooks Documentation](https://docs.openclaw.ai/automation/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-producing command surfaces] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include health, retrieval, indexing, audit, and maintenance guidance; runtime commands may emit JSON status and warning fields.] <br>

## Skill Version(s): <br>
4.0.23 (source: server release evidence and artifact changelog, released 2026-04-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
