## Description:

Guides agents to install, connect, and use Switchyard's read-only MCP runtime diagnostics for analyzing provider readiness and runtime boundaries safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to attach an agent to Switchyard's read-only MCP runtime diagnostics, inspect provider and runtime health, and separate internal from external blockers before taking action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup asks users to run unpinned code from an external Switchyard repository locally.

Mitigation: Use a known commit or signed release, review package scripts and dependencies, prefer a frozen lockfile or disabled lifecycle scripts, and run setup in a least-privilege sandbox without sensitive credentials.

Risk: Diagnostic results can be overstated beyond the skill's read-only and partial-support boundaries.

Mitigation: Keep conclusions tied to runtime health, provider status, support bundles, and catalog read-backs; do not claim live registry listing, package publication, or full host parity without fresh evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaojiou176/skills/switchyard-runtime-diagnostics)
- [Reference index](references/README.md)
- [Install and attach guide](references/INSTALL.md)
- [MCP capabilities](references/CAPABILITIES.md)
- [First-success demo](references/DEMO.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [OpenHands MCP configuration](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP configuration](references/OPENCLAW_MCP_CONFIG.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with bash command snippets and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic flow; no agent-side writes to external accounts.]

## Skill Version(s):

1.0.0 (source: server release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
