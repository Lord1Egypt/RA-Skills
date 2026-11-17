## Description:

Guides agents through building, securing, testing, and shipping Tauri v2 desktop and mobile applications with a Rust core and web frontend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when scaffolding, reviewing, debugging, or releasing Tauri v2 applications, especially work involving IPC commands, capabilities, plugins, sidecars, window management, CI/CD, and testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runnable IPC file-write examples could lead agents to generate writes outside an app-owned directory.

Mitigation: Require file writes to stay under an app-owned directory and validate filenames before using the example as an implementation source.

Risk: Release and E2E workflow examples could encourage weak CI workflows where signing secrets are available.

Mitigation: Pin CI actions, Node and Rust versions, npm dependencies, and test runners before adapting release or E2E workflow examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anjasta-tarigan/skills/tauri2-best-practice)
- [IPC commands reference](references/ipc-commands.md)
- [Security capabilities reference](references/security-capabilities.md)
- [State management reference](references/state-management.md)
- [Plugins and sidecars reference](references/plugins-sidecar.md)
- [Windowing and multi-window reference](references/windowing-multiwindow.md)
- [Bundling updater CI/CD reference](references/bundling-updater-cicd.md)
- [Testing reference](references/testing.md)
- [Tauri v2 security](https://v2.tauri.app/security/)
- [Tauri v2 IPC](https://v2.tauri.app/concept/inter-process-communication/)
- [Tauri v2 calling Rust](https://v2.tauri.app/develop/calling-rust/)
- [Tauri v2 state management](https://v2.tauri.app/develop/state-management/)
- [Tauri v2 updater plugin](https://v2.tauri.app/plugin/updater/)
- [Tauri v2 GitHub release pipeline](https://v2.tauri.app/distribute/pipelines/github/)
- [Tauri v2 testing](https://v2.tauri.app/develop/tests/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, configuration snippets, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill that may lead an agent to propose code, configuration, and release workflow changes]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
