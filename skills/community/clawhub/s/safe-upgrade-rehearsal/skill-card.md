## Description:

Rehearse an OpenClaw update with exact package evidence, installation coverage, and existing Kova reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pdurlej](https://clawhub.ai/user/pdurlej)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill before an OpenClaw upgrade to inventory required surfaces, fetch exact package evidence, rehearse compatibility, and prepare migration, rollback, and post-start verification plans while leaving production unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operator inputs may accidentally include secrets, private conversations, live configuration values, or production logs.

Mitigation: Use public-safe coverage, customization, observation, and advisory inputs; do not provide secrets or raw production logs.

Risk: Package evidence collection calls npm against the public registry and downloads package archives.

Mitigation: Use exact versions, fresh output directories, and the intended read-only rehearsal commands only when public npm package lookup is acceptable.

Risk: A ready rehearsal result could be mistaken for permission to mutate production.

Mitigation: Treat ready output only as operator planning input; require separate approval, rollback evidence, a maintenance window, and scoped live commands before any production change.

Risk: The optional benchmark advisory adapter runs a local command selected by the operator.

Mitigation: Use the advisory adapter only with a local command that is fully trusted, and treat advisory output as non-authoritative review material.

## Reference(s):

- [OpenClaw Safe Upgrade Rehearsal Kit on ClawHub](https://clawhub.ai/pdurlej/skills/safe-upgrade-rehearsal)
- [OpenClaw Safe Update Homepage](https://github.com/pdurlej/openclaw-skill-safe-update)
- [Evidence Contract](references/evidence-contract.md)
- [Stateful Upgrades with Kova and OpenClaw](references/kova-upgrade-rehearsal.md)
- [Installation Contract](references/installation-contract.md)
- [Safe-update Phase Handoffs](references/phase-handoffs.md)
- [Benchmark Scoring Protocol](references/benchmark-scoring-protocol.md)
- [Benchmark Runner and Reporting](references/benchmark-runner.md)
- [Field Report: OpenClaw 2026.9.1-2026.9.3](references/field-report-2026-09.md)
- [Shadow Runs Index](references/shadow-runs-index.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON or Markdown artifact outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only rehearsal evidence, reports, cache files, and operator planning material; it does not approve or apply a production update.]

## Skill Version(s):

1.3.2 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
