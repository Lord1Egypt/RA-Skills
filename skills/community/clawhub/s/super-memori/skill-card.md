## Description:

Local-first hybrid memory skill for OpenClaw agents that helps find, recall, search, and reuse past episodic, semantic, procedural, and learning memory while reporting degraded host state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to give agents a local memory workflow for querying prior work, saving reusable lessons, refreshing indexes, and checking memory health before relying on results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive agent history and index memory into local services.

Mitigation: Install only in environments where local memory persistence is acceptable, and keep Qdrant and the semantic daemon bound to loopback.

Risk: Remote SUPER_MEMORI_* endpoint settings could expose memory data if configured without separate protection.

Mitigation: Avoid remote endpoint settings unless the transport, authentication, and host controls are separately secured.

Risk: The startup hook and maintenance workflows can run local checks and host metadata scans.

Mitigation: Review hook configuration before enabling it, and treat auto-learning and system-hygiene features as opt-in workflows for sensitive environments.

## Reference(s):

- [Architecture](references/architecture.md)
- [Command Contracts](references/command-contracts.md)
- [Retrieval Pipeline](references/retrieval-pipeline.md)
- [Health Model](references/health-model.md)
- [Maintenance Reference](references/maintenance.md)
- [Verification Evidence](references/verification-evidence.md)
- [Release Status](references/release-status.md)
- [OpenClaw Hooks Documentation](https://docs.openclaw.ai/automation/hooks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-aware command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Host state must be read from live command JSON; semantic and hybrid paths may degrade to lexical mode when local prerequisites are unavailable.]

## Skill Version(s):

4.0.23 (source: server evidence, _meta.json, CHANGELOG 2026-04-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
