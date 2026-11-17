## Description:

Policy benchmarking runner for MCP security policies that runs attack suites against protect-mcp policy packs and produces signed receipts and badges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomjwxf](https://clawhub.ai/user/tomjwxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run deterministic red-team attack suites against protect-mcp policy files and benchmark whether policies block or allow expected behaviors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs mutable npm packages and mixes scoped and unscoped package names.

Mitigation: Verify the npm package publisher and intended binary name, pin exact package versions, and prefer a project-local install with a lockfile.

Risk: Benchmark commands execute security testing tooling against local policy files.

Mitigation: Run the commands in an isolated environment with minimal secrets and constrained filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomjwxf/skills/scopeblind-red-team)
- [ScopeBlind Red Team npm package](https://npmjs.com/package/@scopeblind/red-team)
- [ScopeBlind Red Team documentation](https://scopeblind.com/docs/red-team)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
