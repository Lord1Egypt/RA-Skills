## Description: <br>
Provides TypeScript and JavaScript package-manager guidance for npm, yarn, pnpm, bun, and deno, including configuration, dependency management, workspaces, troubleshooting, and migration with approval required before mutating actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose, configure, and troubleshoot TypeScript package managers, manage dependencies and lockfiles, optimize package.json files, and plan workspace or migration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled .js.txt helper scripts can execute local shell commands if renamed and run. <br>
Mitigation: Inspect each helper before renaming it, run it only in a trusted project directory, and execute only after explicit user approval. <br>
Risk: Remote installer one-liners may execute code served from the network at run time. <br>
Mitigation: Confirm the installer URL, prefer official downloaded installers or an OS package manager, and pin versions when stricter review is required. <br>
Risk: Dependency installs, audit fixes, lockfile regeneration, and clean commands can mutate project files or remove local state. <br>
Mitigation: Confirm the working directory, propose exact commands first, and review package.json and lockfile diffs before approving changes. <br>


## Reference(s): <br>
- [Package Management](references/package-management.md) <br>
- [Integration with Build Tools](references/integration-with-build-tools.md) <br>
- [Package Manager Comparison Chart](assets/package-manager-comparison.md) <br>
- [Package.json Template for TypeScript Projects](assets/package-json-template.md) <br>
- [TypeScript: Integrating with Build Tools](https://www.typescriptlang.org/docs/handbook/integrating-with-build-tools.html) <br>
- [pnpm](https://pnpm.io/) <br>
- [Semantic Versioning](https://semver.org/) <br>
- [TypeScript Package Manager on ClawHub](https://clawhub.ai/jhauga/typescript-package-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mutating dependency, installer, and helper-script actions require explicit user approval and package.json or lockfile diff review.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
