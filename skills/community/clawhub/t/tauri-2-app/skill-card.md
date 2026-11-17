## Description:

Scaffold or extend Tauri 2 desktop apps with a Rust backend, TypeScript/React frontend, modular command and storage patterns, optional encrypted secrets, updater support, and CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold new Tauri 2 desktop apps or add command and module slices with Rust backend logic and typed frontend integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source templates can generate unsafe file access and overly broad desktop permissions.

Mitigation: Review and tighten generated templates before production; constrain generic write_file behavior, validate storage filenames against app_data_dir containment, and generate only the Tauri plugins and capabilities the app actually needs.

Risk: Dependency resolution and updater setup depend on user-controlled external inputs.

Mitigation: Pin resolved dependency versions at scaffold time and require user-owned signing keys and endpoints before enabling updater behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/tauri-2-app)
- [Tauri 2 App - Canonical Folder Layout](references/folder-layout.md)
- [Good Patterns](references/good-patterns.md)
- [Anti-patterns](references/anti-patterns.md)
- [Tauri configuration template](references/templates/tauri-conf.md)
- [Capability template](references/templates/capabilities.md)
- [Cargo template](references/templates/cargo-toml.md)
- [Storage module template](references/templates/storage-mod.md)
- [Encryption module template](references/templates/encryption-mod.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, shell commands, configuration snippets, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce full project scaffolds or focused command/module additions depending on the selected mode.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
