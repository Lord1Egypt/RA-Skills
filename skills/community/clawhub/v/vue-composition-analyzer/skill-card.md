## Description:

Analyzes Vue 3 Composition API usage to audit reactivity patterns, composable design, ref and reactive choices, computed properties, watcher usage, and lifecycle hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Vue 3 codebases, migrate Options API components, audit composable architecture, and enforce Composition API best practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests running vue-tsc through npx, which can execute a package version outside the reviewed project's lockfile.

Mitigation: Prefer the project's existing npm script or lockfile-backed package-manager command so vue-tsc is resolved from pinned project dependencies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/vue-composition-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis report with inline shell commands, severity-ranked findings, tables, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes component API style counts, Composition API anti-pattern findings, composable health notes, and remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
