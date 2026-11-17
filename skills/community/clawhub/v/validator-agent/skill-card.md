## Description:

Validator Agent runs an eight-round validation pipeline for TypeScript and Solidity projects before publish or deploy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[up2itnow](https://clawhub.ai/user/up2itnow)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill as a pre-publish, pre-merge, or dependency-update quality gate for TypeScript and Solidity projects. It checks compile status, linting, tests, security audit results, type coverage, documentation, changelog readiness, and produces a final pass, warn, or block recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run broad shell commands and transient npm tools in user projects.

Mitigation: Review before installing, run it only in trusted sandboxed workspaces, prefer pinned local project tools, avoid automatic npx downloads, and keep production secrets out of the validation environment.

Risk: Project path handling and command scope may be risky in untrusted repositories.

Mitigation: Validate or quote project paths before running checks and limit execution to the intended project directory.

## Reference(s):

- [Validator Agent on ClawHub](https://clawhub.ai/up2itnow/skills/validator-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with validation tables, command results, blocking issues, warnings, and a publish recommendation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented report path is ops/reports/validator-YYYY-MM-DD-HH-[project].md.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact/skill.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
