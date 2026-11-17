## Description:

Provides TypeScript package-management guidance across npm, yarn, pnpm, bun, and deno, including configuration, dependency workflows, workspaces, conflict resolution, and package.json optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose, configure, and troubleshoot TypeScript package managers, manage dependency and workspace workflows, and prepare package.json scripts and build-tool integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste workflows can run unverified remote installers or unpinned downloaded tools.

Mitigation: Inspect commands first, avoid pipe-to-shell installers, and prefer pinned OS or package-manager installation methods.

Risk: Bundled helper scripts shell out to local package manager tools when renamed and executed.

Mitigation: Read helper scripts before use, run them only in trusted project directories, and require explicit approval before execution.

Risk: Dependency installs, audit fixes, and lockfile regeneration can mutate project state.

Mitigation: Show the exact command and expected package.json or lockfile diff before executing mutating actions.

## Reference(s):

- [Package Management](references/package-management.md)
- [Integration with Build Tools](references/integration-with-build-tools.md)
- [Package Manager Comparison Chart](assets/package-manager-comparison.md)
- [Package.json Template for TypeScript Projects](assets/package-json-template.md)
- [npm Documentation](https://docs.npmjs.com/)
- [TypeScript: Integrating with Build Tools](https://www.typescriptlang.org/docs/handbook/integrating-with-build-tools.html)
- [pnpm Documentation](https://pnpm.io/)
- [Semantic Versioning](https://semver.org/)
- [Bun](https://github.com/oven-sh/bun)
- [Deno](https://github.com/denoland/deno)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, JSON snippets, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutating dependency, installer, lockfile, and helper-script actions require explicit user approval and diff review before execution.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
