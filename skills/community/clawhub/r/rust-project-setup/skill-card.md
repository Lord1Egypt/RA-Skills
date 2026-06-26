## Description: <br>
Guidance for scaffolding new Rust projects, including Cargo configuration, workspace organization, CI pipelines, feature flags, no_std development, clippy, rustfmt, and linting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold Rust crates and workspaces, configure Cargo manifests, add linting and formatting policy, and set up CI for checks, tests, MSRV validation, and release builds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested cargo install commands or GitHub Actions snippets can affect a developer's local toolchain or repository CI. <br>
Mitigation: Review and adapt proposed commands and workflow snippets before applying them to a project. <br>
Risk: Rust setup guidance can be misapplied when a project has a different MSRV, lockfile policy, target platform, or no_std requirement. <br>
Mitigation: Confirm project-specific constraints and run the documented gates such as cargo metadata, clippy, fmt, tests, and CI before treating setup as complete. <br>


## Reference(s): <br>
- [Rust Project Setup on ClawHub](https://clawhub.ai/anderskev/rust-project-setup) <br>
- [Cargo.toml Configuration](references/cargo-config.md) <br>
- [CI Setup](references/ci-setup.md) <br>
- [Features and Conditional Compilation](references/features-conditional.md) <br>
- [no_std Development](references/no-std.md) <br>
- [Workspace Layout](references/workspace-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, TOML, YAML, Rust, and text snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; the skill itself has no hidden executable behavior.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
