## Description:

Interactive project scaffolding tool that generates complete project structures for Node.js, Python, Go, and Rust with .gitignore, README, CI/CD configuration, Docker files, linting, testing, and license files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to scaffold new Node.js, Python, Go, or Rust projects with common repository structure, build files, CI configuration, Docker support, and starter documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffolder writes a new project tree, and the available security summary says its file-writing scope is not well contained or safely validated.

Mitigation: Run with --dry-run first, choose a trusted output directory, and avoid untrusted project names or metadata.

Risk: The skill initializes a git repository and creates an initial commit by default.

Mitigation: Use --no-git-init until the generated files have been reviewed.

Risk: Generated CI and Docker files may reference third-party actions, images, and tools.

Mitigation: Review generated workflows, Dockerfiles, and dependency installation commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-project-setup-wizard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Generated project files plus terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates language-specific project trees and may initialize a git repository unless disabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
