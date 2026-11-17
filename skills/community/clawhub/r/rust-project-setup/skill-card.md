## Description:

Step-by-step guidance for setting up new Rust projects with proper configuration, linting, and CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold Rust binaries, libraries, and workspaces with Cargo configuration, linting, formatting, CI, feature flags, and no_std guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied CI examples can carry supply-chain risk if third-party actions, branch references, or installed tools are left unpinned.

Mitigation: Pin GitHub Actions to reviewed commit SHAs, avoid branch references such as @master, pin cargo-installed tools with --version and --locked, and set least-privilege workflow permissions.

## Reference(s):

- [Rust Project Setup Skill Page](https://clawhub.ai/anderskev/skills/rust-project-setup)
- [Cargo.toml Configuration](references/cargo-config.md)
- [Workspace Layout](references/workspace-layout.md)
- [CI Setup](references/ci-setup.md)
- [Features and Conditional Compilation](references/features-conditional.md)
- [no_std Development](references/no-std.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, TOML, YAML, Rust, and text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
