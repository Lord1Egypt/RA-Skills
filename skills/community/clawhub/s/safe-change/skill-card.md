## Description:

Map blast radius before shipping — run when editing a service, controller, hook, or shared utility to surface all importers, affected API routes, test gaps, ENV vars, and recent migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brasco05](https://clawhub.ai/user/brasco05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use Safe Change before modifying shared TypeScript, NestJS, or Next.js code to map affected importers, API routes, tests, environment variables, and recent migrations. The skill presents a risk score and checkpoint before edits proceed, then runs the repository verification gate after changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verify gate can execute repository-defined typecheck, lint, test, and build scripts.

Mitigation: Review scripts/verify-gate.sh and the target repository's package scripts before running the gate, and use a workspace without secrets or untrusted package scripts.

Risk: Regex-based static analysis can miss dynamic imports, barrel re-exports, decorator aliases, path aliases, and non-TypeScript files.

Mitigation: Treat low risk scores as advisory and manually check the known blind spots listed in references/limitations.md before approving high-impact changes.

## Reference(s):

- [Usage Guide](references/usage.md)
- [Limitations](references/limitations.md)
- [Example Impact Report](references/example-impact-report.md)
- [Safe Change on ClawHub](https://clawhub.ai/brasco05/skills/safe-change)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with risk score, affected files, API routes, test coverage, environment variables, migrations, and a go/no-go checkpoint.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner emits JSON for agent interpretation; the verify gate returns shell output and exits non-zero on the first failed check.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
