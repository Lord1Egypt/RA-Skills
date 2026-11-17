## Description:

Write and run quantum circuits using Quantinuum's Guppy language on the Selene emulator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantum application engineers use this skill to write Guppy circuits, run Selene emulator jobs, manage parameter sweeps, validate quantum results, and plan Nexus workflows with cost and evidence controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents through authenticated Nexus or hardware-backed jobs that can spend credits and leave auth or job state behind.

Mitigation: Require explicit live-mode confirmation, target device, max_cost, total budget, account or group choice, and a cleanup plan before any Nexus or hardware-backed run.

Risk: Generated Python or temporary files may be run as part of circuit construction and execution workflows.

Mitigation: Review generated files before execution and prefer pinned dependency versions for Guppy, Selene, pytket, and qnexus workflows.

## Reference(s):

- [Skill source listing](https://arunquantum.lovable.app/skills)
- [Guppy language](references/guppy-language.md)
- [Guppy v1 migration](references/guppy-v1-migration.md)
- [Selene runtime](references/selene-runtime.md)
- [Driver pattern: parameterized kernels](references/driver-pattern.md)
- [Parameter sweeps: SweepSpec and SweepRunner](references/sweep-runner.md)
- [Quantinuum Nexus: submitting real jobs](references/nexus-jobs.md)
- [Nexus accounts, quotas and access control](references/nexus-admin.md)
- [Evidence integrity: making a number defensible](references/evidence-integrity.md)
- [Cross-platform validation and error mitigation hierarchies](references/cross-platform-validation.md)
- [pytket / TKET compile lane](references/pytket.md)
- [selene_run v1 schema](references/selene-run-schema.md)
- [Unified stack cheat sheet](references/stack-cheatsheet.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Python files, JSON result artifacts, and credential-free execution specifications when used by an agent.]

## Skill Version(s):

1.0.0 (source: target metadata; artifact README notes OpenClaw edition v0.4.11 built 2026-08-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
